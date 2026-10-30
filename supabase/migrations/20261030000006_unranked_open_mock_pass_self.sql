-- AptiSetu, 30 October 2026: Open Mock is UNRANKED practice (1 Nov 2026 uses the public CAT Mock 5),
-- has_pass/pass_ok only ever look at the signed-in caller, and a repeat Open Mock submission returns the stored first score.
-- New file on purpose: earlier migrations are already applied to the live project and are not edited.

-- ---------- 1. Unranked: no public leaderboard, no "my rank" ----------
revoke all on function public.open_mock_leaderboard(text, integer) from public, anon, authenticated;
revoke all on function public.my_open_mock_rank(text) from public, anon, authenticated;

-- ---------- 2. has_pass() / pass_ok(): no uid argument, always auth.uid() ----------
-- The old (uid uuid default auth.uid()) versions let any logged-in user ask about another user's Pass.
-- The test_attempts read policy depends on pass_ok, so it is dropped and recreated around the swap.
drop policy if exists "read own attempts" on public.test_attempts;
drop function if exists public.pass_ok(uuid);
drop function if exists public.has_pass(uuid);

create or replace function public.has_pass() returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.passes p where p.user_id = auth.uid() and p.status = 'paid' and (p.valid_until is null or p.valid_until > now()))
$$;
revoke all on function public.has_pass() from public, anon;
grant execute on function public.has_pass() to authenticated;

create or replace function public.pass_ok() returns boolean
language sql stable security definer set search_path = public as $$
  select coalesce((select value = 'true'::jsonb from public.app_settings where key = 'pass_gating'), false) = false
      or public.has_pass()
$$;
revoke all on function public.pass_ok() from public, anon;
grant execute on function public.pass_ok() to authenticated;

create policy "read own attempts" on public.test_attempts for select to authenticated
  using ((select auth.uid()) = user_id and public.pass_ok());

-- ---------- 3. submit_open_mock: a repeat submission returns the stored first score ----------
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
  if ins = 1 then
    return query select s, c, w, true;
  else
    -- repeat attempt: report the stored first score, not this attempt's
    return query select a.score, a.correct::int, a.wrong::int, false
      from public.open_mock_attempts a where a.user_id = uid and a.mock_id = p_mock and a.section = p_section;
  end if;
end $$;
revoke all on function public.submit_open_mock(text, text, jsonb) from public, anon;
grant execute on function public.submit_open_mock(text, text, jsonb) to authenticated;
