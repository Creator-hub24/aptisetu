-- Pass gating switch. While pass_gating = false (the default) every feature stays free, so nothing changes for users
-- until the owner confirms the price and turns it on:  update public.app_settings set value = 'true' where key = 'pass_gating';
create table if not exists public.app_settings (key text primary key, value jsonb not null);
alter table public.app_settings enable row level security;
drop policy if exists "anyone reads settings" on public.app_settings;
create policy "anyone reads settings" on public.app_settings for select to anon, authenticated using (true);
revoke all on public.app_settings from anon, authenticated;
grant select on public.app_settings to anon, authenticated;
insert into public.app_settings (key, value) values ('pass_gating', 'false') on conflict (key) do nothing;

create or replace function public.pass_ok(uid uuid default auth.uid()) returns boolean
language sql stable security definer set search_path = public as $$
  select coalesce((select value = 'true'::jsonb from public.app_settings where key = 'pass_gating'), false) = false
      or public.has_pass(uid)
$$;
revoke all on function public.pass_ok(uuid) from public, anon;
grant execute on function public.pass_ok(uuid) to authenticated;

-- Saved history is a Pass feature: rows are always saved, but reading them needs the Pass once gating is on.
drop policy if exists "read own attempts" on public.test_attempts;
create policy "read own attempts" on public.test_attempts for select to authenticated
  using ((select auth.uid()) = user_id and public.pass_ok());

-- Your rank is a Pass feature once gating is on (the public top-50 board stays free).
create or replace function public.my_open_mock_rank(p_mock text)
returns table (rank bigint, candidates bigint, total integer)
language plpgsql stable security definer set search_path = public as $$
begin
  if not public.pass_ok() then raise exception 'AptiSetu Pass required'; end if;
  return query
  with t as (select user_id, sum(score)::int total from public.open_mock_attempts where mock_id = p_mock group by user_id),
       r as (select user_id, t.total, rank() over (order by t.total desc) rk, count(*) over () n from t)
  select r.rk, r.n, r.total from r where r.user_id = auth.uid();
end $$;
revoke all on function public.my_open_mock_rank(text) from public, anon;
grant execute on function public.my_open_mock_rank(text) to authenticated;
