-- AptiSetu accounts: profiles, saved test history, AptiSetu Pass, Open Mock + leaderboard.
-- Applied by tools/deploy_supabase.sh (supabase db push). Every table has Row Level Security on.
-- Clients use the public anon key; the service-role key is used only inside Edge Functions.

-- ---------- profiles: the name shown on the leaderboard ----------
create table if not exists public.profiles (
  user_id      uuid primary key references auth.users (id) on delete cascade,
  display_name text not null default 'Aspirant' check (char_length(display_name) between 2 and 30),
  created_at   timestamptz not null default now()
);
alter table public.profiles enable row level security;
drop policy if exists "read own profile"   on public.profiles;
drop policy if exists "insert own profile" on public.profiles;
drop policy if exists "update own profile" on public.profiles;
create policy "read own profile"   on public.profiles for select to authenticated using ((select auth.uid()) = user_id);
create policy "insert own profile" on public.profiles for insert to authenticated with check ((select auth.uid()) = user_id);
create policy "update own profile" on public.profiles for update to authenticated using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);
grant select, insert, update on public.profiles to authenticated;
revoke all on public.profiles from anon;

-- ---------- test_attempts: saved history of every finished quiz / sectional ----------
create table if not exists public.test_attempts (
  id          bigint generated always as identity primary key,
  user_id     uuid not null references auth.users (id) on delete cascade,
  test_key    text not null check (test_key ~ '^[a-z0-9-]{1,80}$'),   -- e.g. cat-mock-5-sectional, general-quant
  title       text not null default '' check (char_length(title) <= 160),
  score       numeric(7,2) not null check (score between -1000 and 1000),
  max_score   numeric(7,2) not null check (max_score between 0 and 1000),
  accuracy    smallint check (accuracy between 0 and 100),
  questions   smallint check (questions between 0 and 500),
  time_s      integer check (time_s between 0 and 86400),
  created_at  timestamptz not null default now()
);
create index if not exists test_attempts_user_time on public.test_attempts (user_id, created_at desc);
alter table public.test_attempts enable row level security;
drop policy if exists "read own attempts"   on public.test_attempts;
drop policy if exists "insert own attempts" on public.test_attempts;
create policy "read own attempts"   on public.test_attempts for select to authenticated using ((select auth.uid()) = user_id);
create policy "insert own attempts" on public.test_attempts for insert to authenticated with check ((select auth.uid()) = user_id);
grant select, insert on public.test_attempts to authenticated;
grant usage on sequence public.test_attempts_id_seq to authenticated;
revoke all on public.test_attempts from anon;

-- ---------- passes: AptiSetu Pass purchases. Users can only READ their own rows. ----------
-- Rows are created and updated only by the Edge Functions (service role), after Razorpay signature checks.
create table if not exists public.passes (
  id                  bigint generated always as identity primary key,
  user_id             uuid not null references auth.users (id) on delete cascade,
  plan                text not null check (plan ~ '^[a-z0-9-]{1,40}$'),
  amount_paise        integer not null check (amount_paise > 0),
  currency            text not null default 'INR',
  razorpay_order_id   text not null unique,
  razorpay_payment_id text unique,
  status              text not null default 'created' check (status in ('created', 'paid', 'failed', 'refunded')),
  valid_until         timestamptz,
  live_mode           boolean not null default false,
  created_at          timestamptz not null default now(),
  updated_at          timestamptz not null default now()
);
create index if not exists passes_user on public.passes (user_id);
alter table public.passes enable row level security;
drop policy if exists "read own passes" on public.passes;
create policy "read own passes" on public.passes for select to authenticated using ((select auth.uid()) = user_id);
revoke all on public.passes from anon, authenticated;
grant select on public.passes to authenticated;

create or replace function public.has_pass(uid uuid default auth.uid()) returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.passes p where p.user_id = uid and p.status = 'paid' and (p.valid_until is null or p.valid_until > now()))
$$;
revoke all on function public.has_pass(uuid) from public, anon;
grant execute on function public.has_pass(uuid) to authenticated;

-- ---------- Open Mock: schedule, answer key (server only), attempts, leaderboard ----------
create table if not exists public.open_mocks (
  id        text primary key check (id ~ '^[a-z0-9-]{1,40}$'),     -- e.g. 2026-11
  title     text not null,
  pack      text not null,                                      -- question pack used, e.g. mock-5
  starts_at timestamptz not null,
  ends_at   timestamptz not null check (ends_at > starts_at)
);
alter table public.open_mocks enable row level security;
drop policy if exists "anyone reads schedule" on public.open_mocks;
create policy "anyone reads schedule" on public.open_mocks for select to anon, authenticated using (true);
grant select on public.open_mocks to anon, authenticated;

-- answer key: no policies and no grants, so only security-definer functions (and the service role) can read it
create table if not exists public.open_mock_keys (
  mock_id  text not null references public.open_mocks (id) on delete cascade,
  section  text not null check (section in ('varc', 'dilr', 'qa')),
  qid      text not null,
  qtype    text not null check (qtype in ('mcq', 'tita')),
  kind     text not null default '',
  answer   text not null,
  primary key (mock_id, section, qid)
);
alter table public.open_mock_keys enable row level security;
revoke all on public.open_mock_keys from anon, authenticated;

create table if not exists public.open_mock_attempts (
  user_id      uuid not null references auth.users (id) on delete cascade,
  mock_id      text not null references public.open_mocks (id) on delete cascade,
  section      text not null check (section in ('varc', 'dilr', 'qa')),
  score        integer not null,
  correct      smallint not null,
  wrong        smallint not null,
  submitted_at timestamptz not null default now(),
  primary key (user_id, mock_id, section)                      -- first attempt per section counts
);
alter table public.open_mock_attempts enable row level security;
drop policy if exists "read own open-mock attempts" on public.open_mock_attempts;
create policy "read own open-mock attempts" on public.open_mock_attempts for select to authenticated using ((select auth.uid()) = user_id);
revoke all on public.open_mock_attempts from anon, authenticated;
grant select on public.open_mock_attempts to authenticated;

-- Scores are computed on the server from the hidden key; clients send only their responses.
-- responses: {"<qid>": <option index> | "<typed answer>"}. Marking: MCQ +3 / -1, TITA +3 / 0.
create or replace function public.submit_open_mock(p_mock text, p_section text, p_responses jsonb)
returns table (score integer, correct integer, wrong integer, first_attempt boolean)
language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); m public.open_mocks; s int := 0; c int := 0; w int := 0; k record; r jsonb; ok boolean; ins int;
begin
  if uid is null then raise exception 'login required'; end if;
  select * into m from public.open_mocks where id = p_mock;
  if not found then raise exception 'unknown open mock'; end if;
  if now() < m.starts_at or now() > m.ends_at then raise exception 'this open mock is not live'; end if;
  if jsonb_typeof(p_responses) <> 'object' then raise exception 'bad responses'; end if;
  for k in select * from public.open_mock_keys where mock_id = p_mock and section = p_section loop
    r := p_responses -> k.qid;
    if r is null or r = 'null'::jsonb or r = '""'::jsonb then continue; end if;
    if k.qtype = 'mcq' then ok := (r #>> '{}') = k.answer;
    elsif k.kind = 'sequence' then ok := regexp_replace(r #>> '{}', '\s', '', 'g') = k.answer;
    else begin ok := abs((r #>> '{}')::numeric - k.answer::numeric) < 1e-9; exception when others then ok := false; end;
    end if;
    if ok then s := s + 3; c := c + 1; else w := w + 1; if k.qtype = 'mcq' then s := s - 1; end if; end if;
  end loop;
  insert into public.open_mock_attempts (user_id, mock_id, section, score, correct, wrong)
    values (uid, p_mock, p_section, s, c, w) on conflict do nothing;
  get diagnostics ins = row_count;
  return query select s, c, w, ins = 1;
end $$;
revoke all on function public.submit_open_mock(text, text, jsonb) from public, anon;
grant execute on function public.submit_open_mock(text, text, jsonb) to authenticated;

-- Public leaderboard: rank, display name and total only (no emails, no user ids).
create or replace function public.open_mock_leaderboard(p_mock text, p_limit integer default 50)
returns table (rank bigint, display_name text, total integer, sections integer)
language sql stable security definer set search_path = public as $$
  with t as (
    select a.user_id, sum(a.score)::int total, count(*)::int sections, max(a.submitted_at) last_at
    from public.open_mock_attempts a where a.mock_id = p_mock group by a.user_id)
  select rank() over (order by t.total desc), coalesce(p.display_name, 'Aspirant'), t.total, t.sections
  from t left join public.profiles p on p.user_id = t.user_id
  order by 1, t.last_at limit least(greatest(p_limit, 1), 200)
$$;
grant execute on function public.open_mock_leaderboard(text, integer) to anon, authenticated;

-- My rank (for the Pass "rank" feature): rank and number of candidates.
create or replace function public.my_open_mock_rank(p_mock text)
returns table (rank bigint, candidates bigint, total integer)
language sql stable security definer set search_path = public as $$
  with t as (select user_id, sum(score)::int total from public.open_mock_attempts where mock_id = p_mock group by user_id),
       r as (select user_id, total, rank() over (order by total desc) rk, count(*) over () n from t)
  select rk, n, total from r where user_id = auth.uid()
$$;
revoke all on function public.my_open_mock_rank(text) from public, anon;
grant execute on function public.my_open_mock_rank(text) to authenticated;
