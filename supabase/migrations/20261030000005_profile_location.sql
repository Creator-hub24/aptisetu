-- AptiSetu: optional profile fields (city, state, target exam) + an admin-only summary view.
-- The student fills these in themselves on My account; all are optional. They are never shown on the leaderboard.

alter table public.aptisetu_profiles add column if not exists city        text;
alter table public.aptisetu_profiles add column if not exists state       text;
alter table public.aptisetu_profiles add column if not exists target_exam text;
alter table public.aptisetu_profiles add column if not exists updated_at  timestamptz not null default now();
do $$ begin
  if not exists (select 1 from pg_constraint where conname = 'aptisetu_profiles_city_len')  then
    alter table public.aptisetu_profiles add constraint aptisetu_profiles_city_len  check (city  is null or char_length(city)  between 2 and 60); end if;
  if not exists (select 1 from pg_constraint where conname = 'aptisetu_profiles_state_len') then
    alter table public.aptisetu_profiles add constraint aptisetu_profiles_state_len check (state is null or char_length(state) between 2 and 40); end if;
  if not exists (select 1 from pg_constraint where conname = 'aptisetu_profiles_exam_chk')  then
    alter table public.aptisetu_profiles add constraint aptisetu_profiles_exam_chk  check (target_exam is null or target_exam in ('CAT','CLAT','Bank','SSC','CUET','Placements','Other')); end if;
end $$;

-- Admin summary: lives in its own schema, which the public API does not expose, and is granted to nobody.
-- Open it in the Supabase dashboard (SQL Editor):  select * from aptisetu_admin.user_summary order by signed_up desc;
create schema if not exists aptisetu_admin;
revoke all on schema aptisetu_admin from public, anon, authenticated;
create or replace view aptisetu_admin.user_summary as
select u.email,
       p.display_name,
       p.city, p.state, p.target_exam,
       u.created_at                                   as signed_up,
       u.last_sign_in_at                              as last_login,
       coalesce(t.tests, 0)                           as tests_saved,
       t.avg_pct                                      as avg_test_pct,
       t.last_test_at,
       coalesce(s.sets_done, 0)                       as cat_sets_done,
       coalesce(o.open_mock_total, 0)                 as open_mock_total,
       coalesce(pa.has_pass, false)                   as has_pass
from auth.users u
left join public.aptisetu_profiles p on p.user_id = u.id
left join (select user_id, count(*) tests, round(avg(100.0 * score / nullif(max_score, 0)), 1) avg_pct, max(created_at) last_test_at
           from public.test_attempts group by user_id) t on t.user_id = u.id
left join (select user_id, count(*) sets_done from public.set_progress group by user_id) s on s.user_id = u.id
left join (select user_id, sum(score) open_mock_total from public.open_mock_attempts group by user_id) o on o.user_id = u.id
left join (select user_id, bool_or(status = 'paid' and (valid_until is null or valid_until > now())) has_pass from public.passes group by user_id) pa on pa.user_id = u.id;
revoke all on aptisetu_admin.user_summary from public, anon, authenticated;
