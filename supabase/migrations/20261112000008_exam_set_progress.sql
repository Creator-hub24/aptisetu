-- AptiSetu: practice-set progress for CUET (UG), Bank and SSC as well as CAT.
-- NOT YET APPLIED: Vaibhav must run this once in Supabase > SQL Editor (or `supabase db push`) before the
-- CUET / Bank / SSC sets can save results. Until then those saves fail with a check-constraint error and the site
-- shows "Could not save your result"; CAT sets keep working unchanged.
--
-- Keying: the primary key stays (user_id, section, set_no). CAT rows keep their section values ('qa', 'varc', 'dilr');
-- the other exams store "<exam>-<section>" (e.g. 'cuet-gat', 'bank-quant', 'ssc-maths'), so a CUET/Bank/SSC row can
-- never collide with a CAT row, and no existing row changes. Bank and SSC marking has quarter and half marks
-- (−0.25 / −0.50), so score becomes numeric(7,2). Existing integer scores convert exactly.

alter table public.set_progress drop constraint if exists set_progress_section_check;
alter table public.set_progress add constraint set_progress_section_check check (section in (
  'qa', 'varc', 'dilr',                                   -- CAT (unchanged)
  'cuet-gat', 'cuet-english', 'cuet-maths',               -- CUET (UG): 25-question sets, +5 / −1
  'bank-quant', 'bank-reasoning', 'bank-di',              -- Bank prelims style: +1 / −0.25
  'ssc-maths', 'ssc-reasoning'));                         -- SSC CGL/CHSL Tier I style: +2 / −0.50

alter table public.set_progress drop constraint if exists set_progress_set_no_check;
alter table public.set_progress add constraint set_progress_set_no_check check (set_no between 1 and 60);

-- score: CAT −30..30 (10 questions, +3 / −1); CUET −25..125 (25 × +5 / −1); Bank −8.75..35; SSC −12.5..50
alter table public.set_progress drop constraint if exists set_progress_score_check;
alter table public.set_progress alter column score type numeric(7,2) using score::numeric;
alter table public.set_progress add constraint set_progress_score_check check (score between -250 and 250);

alter table public.set_progress drop constraint if exists set_progress_total_check;
alter table public.set_progress add constraint set_progress_total_check check (total between 1 and 250);

-- Row Level Security, policies and grants are unchanged (users read / insert / update only their own rows).
