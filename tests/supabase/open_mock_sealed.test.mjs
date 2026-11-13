// Sealed Open Mock edition (a fresh mock): the key and solutions are only in open_mock_keys; open_mock_review()
// releases them after the edition ends and never before. Run: node tests/supabase/open_mock_sealed.test.mjs
// The private key file (private/sql/*_KEY_PRIVATE.sql, git-ignored) is used when it is on this machine; without it
// the test seeds a small stand-in key, so it also runs in CI.
import { PGlite } from "@electric-sql/pglite"; import fs from "fs";
const db = new PGlite(); const R = new URL("../../", import.meta.url).pathname, D = R + "supabase/migrations/";
await db.exec(`create role anon; create role authenticated; create role service_role bypassrls; create schema auth; create table auth.users(id uuid primary key, email text, created_at timestamptz not null default now(), last_sign_in_at timestamptz);
create function auth.uid() returns uuid language sql stable as $$ select nullif(current_setting('t.uid', true),'')::uuid $$;
grant usage on schema auth to anon, authenticated; grant execute on function auth.uid() to anon, authenticated; grant usage on schema public to anon, authenticated;`);
for (const f of fs.readdirSync(D).sort()) await db.exec(fs.readFileSync(D + f, "utf8"));
let fail = 0; const ok = (c, m, v) => { console.log((c ? "PASS " : "FAIL ") + m, v === undefined ? "" : JSON.stringify(v)); if (!c) fail++; };
const isErr = (v, re) => typeof v === "string" && v.startsWith("ERR") && (!re || re.test(v));
const run = async (role, uid, sql) => { await db.exec(`set role ${role}; select set_config('t.uid','${uid}',false);`); try { return (await db.query(sql)).rows; } catch (e) { return "ERR " + e.message; } finally { await db.exec("reset role"); } };
const U1 = "11111111-1111-1111-1111-111111111111"; await db.exec(`insert into auth.users values ('${U1}')`);
const m = JSON.parse(fs.readFileSync(R + "data/open-mock.json", "utf8")).mocks.find(x => x.sealed), ID = m.id;
ok((await db.query(`select count(*)::int n from open_mock_keys where mock_id='${ID}'`)).rows[0].n === 0, "committed migrations hold no key for the sealed edition");
ok((await db.query(`select pack from open_mocks where id='${ID}'`)).rows[0].pack === m.pack, "committed migration adds the schedule row");
const P = R + "private/sql/"; const kf = fs.existsSync(P) ? fs.readdirSync(P).find(f => f.includes(ID.replace(/-/g, "_")) && f.endsWith("_KEY_PRIVATE.sql")) : null;
const pub = Object.fromEntries(["varc", "dilr", "qa"].map(s => [s, JSON.parse(fs.readFileSync(R + `data/open/${m.pack}.${s}.json`, "utf8")).questions]));
if (kf) { await db.exec(fs.readFileSync(P + kf, "utf8")); console.log("using private key file", kf); }
else { console.log("private key file not on this machine: seeding a stand-in key");
  for (const s of Object.keys(pub)) for (const q of pub[s]) await db.query("insert into open_mock_keys (mock_id, section, qid, qtype, kind, answer, solution) values ($1,$2,$3,$4,$5,$6,$7)", [ID, s, q.id, q.type, q.kind || "", q.type === "mcq" ? "0" : q.kind === "sequence" ? "1234" : "1", "stand-in solution text"]); }
for (const s of Object.keys(pub)) {
  const k = (await db.query(`select qid, qtype, kind, answer, solution from open_mock_keys where mock_id='${ID}' and section='${s}'`)).rows;
  ok(k.length === pub[s].length && pub[s].every(q => k.find(x => x.qid === q.id && x.qtype === q.type && x.kind === (q.kind || ""))), `${s}: key rows match the served question ids and types`);
  ok(k.every(x => x.solution && x.solution.length > 20 && (x.qtype !== "mcq" || /^[0-3]$/.test(x.answer))), `${s}: every key row has a solution; MCQ keys are 0-3`);
}
const key = (await db.query(`select qid, qtype, answer from open_mock_keys where mock_id='${ID}' and section='qa'`)).rows;
const right = Object.fromEntries(key.map(k => [k.qid, k.qtype === "mcq" ? +k.answer : k.answer]));
await db.exec(`update open_mocks set starts_at = now() - interval '1 hour', ends_at = now() + interval '1 hour' where id='${ID}'`);
ok(isErr(await run("authenticated", U1, `select * from open_mock_review('${ID}','qa')`), /after this open mock ends/), "during the window: review refused (logged in)");
ok(isErr(await run("anon", "", `select * from open_mock_review('${ID}','qa')`), /after this open mock ends/), "during the window: review refused (guest)");
ok(isErr(await run("authenticated", U1, "select * from open_mock_keys"), /permission denied/) && isErr(await run("anon", "", "select * from open_mock_keys"), /permission denied/), "key table closed to clients");
let r = await run("authenticated", U1, `select * from submit_open_mock('${ID}','qa','${JSON.stringify(right).replace(/'/g, "''")}'::jsonb)`);
ok(r[0] && r[0].score === 3 * key.length && r[0].first_attempt === true, "server scores a fully correct section", r);
ok(isErr(await run("anon", "", `select * from submit_open_mock('${ID}','qa','{}'::jsonb)`), /permission denied/), "guests cannot probe the scorer");
await db.exec(`update open_mocks set starts_at = now() + interval '1 hour', ends_at = now() + interval '2 hour' where id='${ID}'`);
ok(isErr(await run("anon", "", `select * from open_mock_review('${ID}','qa')`), /after this open mock ends/), "before the window: review refused");
await db.exec(`update open_mocks set starts_at = now() - interval '2 hour', ends_at = now() - interval '1 minute' where id='${ID}'`);
r = await run("anon", "", `select * from open_mock_review('${ID}','qa')`);
ok(Array.isArray(r) && r.length === key.length && r.every(x => x.solution && x.answer !== null), "after the end: guests get the key and solutions", Array.isArray(r) ? r.length : r);
r = await run("authenticated", U1, `select * from open_mock_review('${ID}','varc')`); ok(Array.isArray(r) && r.length === pub.varc.length, "after the end: logged-in users too");
ok(isErr(await run("anon", "", `select * from open_mock_review('nope','qa')`), /unknown open mock/), "unknown edition refused");
console.log(fail + " failed"); process.exit(fail ? 1 : 0);
