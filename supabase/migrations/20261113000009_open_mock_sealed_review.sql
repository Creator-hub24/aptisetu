-- AptiSetu, 13 November 2026: sealed Open Mock editions (a fresh mock whose answers are not in any public file).
-- 1. open_mock_keys also stores each question's worked solution (still no client grants on the table).
-- 2. open_mock_review() hands the key and the solutions to the browser ONLY after the edition has ended, so the
--    results page can show answers and solutions from 10 pm IST without anyone publishing a file at that moment.
-- Run this once, before the private key file for a sealed edition. It does not change submit_open_mock or any score.
alter table public.open_mock_keys add column if not exists solution text;

create or replace function public.open_mock_review(p_mock text, p_section text)
returns table (qid text, qtype text, kind text, answer text, solution text)
language plpgsql stable security definer set search_path = public as $$
declare m public.open_mocks;
begin
  select * into m from public.open_mocks where id = p_mock;
  if not found then raise exception 'unknown open mock'; end if;
  if now() <= m.ends_at then raise exception 'answers open after this open mock ends'; end if;
  return query select k.qid, k.qtype, k.kind, k.answer, k.solution
    from public.open_mock_keys k where k.mock_id = p_mock and k.section = p_section order by k.qid;
end $$;
revoke all on function public.open_mock_review(text, text) from public;
grant execute on function public.open_mock_review(text, text) to anon, authenticated;
