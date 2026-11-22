// set_progress after 20261112000008_exam_set_progress.sql: CAT rows unchanged, CUET/Bank/SSC rows keyed "<exam>-<section>",
// fractional Bank/SSC scores, RLS still per user. Run: NODE_PATH=<dir with @electric-sql/pglite> node tests/supabase/set_progress_exams.test.mjs
import { PGlite } from "@electric-sql/pglite"; import fs from "fs";
const D = new URL("../../supabase/migrations/", import.meta.url).pathname;
const db = new PGlite();
await db.exec(`create role anon; create role authenticated; create role service_role bypassrls; create schema auth; create table auth.users(id uuid primary key, email text, created_at timestamptz not null default now(), last_sign_in_at timestamptz);
create function auth.uid() returns uuid language sql stable as $$ select nullif(current_setting('t.uid', true),'')::uuid $$;
grant usage on schema auth to anon, authenticated; grant execute on function auth.uid() to anon, authenticated; grant usage on schema public to anon, authenticated;`);
const U1 = "11111111-1111-1111-1111-111111111111", U2 = "22222222-2222-2222-2222-222222222222";
let fail = 0; const ok = (c, m, v) => { console.log((c ? "PASS " : "FAIL ") + m, v === undefined ? "" : JSON.stringify(v)); if (!c) fail++; };
const as = async (uid, sql) => { await db.exec(`set role authenticated; select set_config('t.uid','${uid}',false);`); try { return (await db.query(sql)).rows; } catch (e) { return "ERR " + e.message; } finally { await db.exec("reset role"); } };
const files = fs.readdirSync(D).sort(), last = files.indexOf("20261112000008_exam_set_progress.sql");
ok(last >= 0 && files.slice(last + 1).every(f => !/set_progress/.test(fs.readFileSync(D + f, "utf8"))), "no later migration touches set_progress");
for (const f of files.slice(0, last)) await db.exec(fs.readFileSync(D + f, "utf8"));
await db.exec(`insert into auth.users values ('${U1}'),('${U2}')`);
// a CAT row written before the migration must survive it unchanged
ok(Array.isArray(await as(U1, `insert into set_progress(user_id,section,set_no,score,total) values ('${U1}','qa',1,27,30) returning 1`)), "CAT row before migration");
ok(typeof (await as(U1, `insert into set_progress(user_id,section,set_no,score,total) values ('${U1}','cuet-gat',1,4,125)`)) === "string", "before migration: CUET row rejected (so the site shows 'could not save')");
await db.exec(fs.readFileSync(D + files[last], "utf8"));
let r = await as(U1, "select section, set_no, score::float8 s, total from set_progress"); ok(r.length === 1 && r[0].section === "qa" && r[0].s === 27, "CAT row unchanged after migration", r);
for (const [sec, n, sc, tot] of [["cuet-gat", 1, 4, 125], ["cuet-english", 4, -25, 125], ["bank-quant", 1, 0.75, 35], ["bank-di", 11, -2.5, 10], ["ssc-maths", 7, 1.5, 50], ["ssc-reasoning", 1, -12.5, 50], ["qa", 2, -30, 30]])
  ok(Array.isArray(await as(U1, `insert into set_progress(user_id,section,set_no,score,total) values ('${U1}','${sec}',${n},${sc},${tot}) returning 1`)), `insert ${sec} set ${n} score ${sc}/${tot}`);
r = await as(U1, "select section, score::float8 s from set_progress where set_no = 1 order by section"); ok(r.map(x => x.section).join() === "bank-quant,cuet-gat,qa,ssc-reasoning" && r.find(x => x.section === "bank-quant").s === 0.75, "same set number in CAT and other exams = separate rows", r);
ok(Array.isArray(await as(U1, `insert into set_progress(user_id,section,set_no,score,total) values ('${U1}','bank-quant',1,5.25,35) on conflict (user_id,section,set_no) do update set score = excluded.score returning 1`)), "upsert on (user_id, section, set_no) still works");
ok(typeof (await as(U1, `insert into set_progress(user_id,section,set_no,score,total) values ('${U1}','cuet-qa',1,1,10)`)) === "string", "unknown section rejected");
ok(typeof (await as(U1, `insert into set_progress(user_id,section,set_no,score,total) values ('${U1}','ssc-maths',1,900,50)`)) === "string", "absurd score rejected");
ok(typeof (await as(U2, `insert into set_progress(user_id,section,set_no,score,total) values ('${U1}','ssc-maths',2,1,50)`)) === "string", "cannot write another user's row");
r = await as(U2, "select count(*)::int n from set_progress"); ok(r[0] && r[0].n === 0, "cannot read another user's rows", r);
r = await db.query("select count(*)::int n from aptisetu_admin.user_summary"); ok(r.rows[0].n === 2, "admin summary view still works", r.rows);
console.log(fail ? fail + " failed" : "all passed"); process.exit(fail ? 1 : 0);
