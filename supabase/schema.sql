-- AptiSetu: CAT practice-set progress. Run once in Supabase > SQL Editor.
-- Each logged-in user can read, insert and update only their own rows (Row Level Security).

create table if not exists public.set_progress (
  user_id    uuid        not null references auth.users (id) on delete cascade,
  section    text        not null check (section in ('qa', 'varc', 'dilr')),
  set_no     smallint    not null check (set_no between 1 and 15),
  score      integer     not null check (score between -30 and 30),   -- 10 questions, +3 / -1
  total      integer     not null check (total between 1 and 30),
  updated_at timestamptz not null default now(),
  primary key (user_id, section, set_no)
);

alter table public.set_progress enable row level security;

drop policy if exists "read own progress"   on public.set_progress;
drop policy if exists "insert own progress" on public.set_progress;
drop policy if exists "update own progress" on public.set_progress;

create policy "read own progress"   on public.set_progress for select to authenticated
  using ((select auth.uid()) = user_id);
create policy "insert own progress" on public.set_progress for insert to authenticated
  with check ((select auth.uid()) = user_id);
create policy "update own progress" on public.set_progress for update to authenticated
  using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);
-- No delete policy: users cannot delete rows from the site. Deletion on request is done by the site owner
-- (deleting the user in Authentication > Users also removes their rows via ON DELETE CASCADE).

grant select, insert, update on public.set_progress to authenticated;
revoke all on public.set_progress from anon;

-- Dashboard settings (not SQL):
--   Authentication > Sign In / Providers > Email: enabled (magic link). 
--   Authentication > URL Configuration: Site URL = https://aptisetu.com
--   Redirect URLs: https://aptisetu.com/**  (add http://localhost:8766/** only while testing locally)
