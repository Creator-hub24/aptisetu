// Open Mock is UNRANKED practice: label shown, no leaderboard/rank anywhere, own saved scores only, repeat attempt keeps the first score.
const {chromium}=require('playwright');const B='http://localhost:8765/';let f=0;
const ok=(c,m)=>{console.log((c?'PASS ':'FAIL ')+m);if(!c)f++};
(async()=>{const b=await chromium.launch();const p=await b.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
const om=JSON.parse(require('fs').readFileSync('data/open-mock.json','utf8')).mocks.slice(-1)[0];
ok(om.ranked===false&&/^Unranked practice, (Mock \d|new) questions$/.test(om.label),'open-mock.json: ranked false + label');
await p.goto(B+'open-mock.html');const txt=await p.locator('main, body').first().innerText();
ok(txt.includes(om.label),'open-mock.html shows the current edition label');
ok(await p.locator('#om-board, #om-name, #om-me').count()===0,'no leaderboard, display-name form or rank box');
ok(!/your rank|counts for rank|all-India leaderboard|Rank<\/th>/i.test(await p.content()),'no rank copy on open-mock.html');
for(const u of['index.html','mock-tests.html','pass.html','privacy.html','terms.html','login.html']){const h=(await (await p.request.get(B+u)).text()).replace(/<script[\s\S]*?<\/script>/g,'');
 const bad=h.match(/[^.>]{0,40}(leaderboard|open mock rank|to be ranked)[^.<]{0,40}/gi)?.filter(s=>!/no (public )?leaderboard|unranked/i.test(s));ok(!bad||!bad.length,u+': no leaderboard/rank promise'+(bad&&bad.length?' -> '+bad[0]:''));}
await p.goto(B+'open-mock.html?mock=1');await p.evaluate(()=>sessionStorage.setItem('aptisetu.mock.user',JSON.stringify({id:'mock-1',email:'edumaths360@gmail.com'})));
await p.goto(B+'open-mock.html');await p.waitForFunction(()=>window.Account&&document.querySelector('.om-mine'));
const r1=await p.evaluate(id=>Account.submitOpenMock(id,'qa',{__score:42}),om.id);const r2=await p.evaluate(id=>Account.submitOpenMock(id,'qa',{__score:3}),om.id);
ok(r1.first_attempt===true&&r1.score===42,'first attempt saved');ok(r2.first_attempt===false&&r2.score===42,'repeat attempt returns the stored first score');
ok(typeof (await p.evaluate(()=>Account.leaderboard))==='undefined','Account.leaderboard removed');
await p.reload();await p.waitForFunction(id=>/42/.test(document.querySelector(`.om-ed[data-mock="${id}"] .om-mine`).innerText),om.id,{timeout:8000}).catch(()=>{});
const mine=await p.locator(`.om-ed[data-mock="${om.id}"] .om-mine`).innerText();ok(/QA\s+42/.test(mine)&&/not taken yet/.test(mine),'own saved scores shown');
// sealed editions: nothing with an answer or a solution is served, the pack is in no listing, and no question counts are shown
const fs=require('fs');const all=JSON.parse(fs.readFileSync('data/open-mock.json','utf8')).mocks;
for(const m of all.filter(x=>x.sealed)){for(const s of['varc','dilr','qa']){const raw=fs.readFileSync(`data/open/${m.pack}.${s}.json`,'utf8'),d=JSON.parse(raw);
  ok(!/"(answer|solution)"/.test(raw)&&d.questions.every(q=>!('answer' in q)&&!('solution' in q)&&q.question),`${m.pack} ${s}: served file has questions only, no answers or solutions`);
  ok(!fs.readFileSync(`data/cat/${s}.json`,'utf8').includes(`"${m.pack}"`),`${m.pack} ${s}: not in the public bank`);}
 ok(!fs.readFileSync('data/cat.json','utf8').includes(`"${m.pack}"`)&&!fs.existsSync(`tools/cat/packs/${m.pack}.qa.json`),`${m.pack}: not in data/cat.json or tools/cat/packs`);
 const mig=fs.readdirSync('supabase/migrations').map(f=>fs.readFileSync('supabase/migrations/'+f,'utf8')).join('\n');
 ok(!new RegExp(`\\('${m.id}', '(varc|dilr|qa)',`).test(mig),`${m.id}: answer key is not in any committed migration`);
 for(const u of['mock-tests.html','cat-practice.html','cat.html','index.html','sitemap.xml'])ok(!fs.readFileSync(u,'utf8').includes(m.pack),`${u}: does not list ${m.pack}`);}
const omh=fs.readFileSync('open-mock.html','utf8');ok(!/(?<!Mock )\b\d+ (Qs|questions)\b/i.test(omh),'open-mock.html shows no question counts');
ok(!/career launcher/i.test(omh),'no Career Launcher on open-mock.html');
// sealed section in the exam engine: opens only in the window, timed only, no key in the page
{const m=all.find(x=>x.sealed);if(m){const u=`cat-practice.html?mode=sectional&section=qa&pack=${m.pack}&open=${m.id}`;
 const q2=await b.newPage();await q2.clock.install({time:new Date(Date.parse(m.starts_at)-3600e3)});await q2.goto(B+u);await q2.waitForFunction(()=>/Open Mock/.test(document.querySelector('#c-info').textContent));
 ok(await q2.locator('#c-start').isDisabled()&&/opens/i.test(await q2.locator('#c-info').innerText()),'sealed section cannot be started before the window');await q2.close();
 const q=await b.newPage();const e2=[];q.on('pageerror',e=>e2.push(e.message));await q.clock.install({time:new Date(Date.parse(m.starts_at)+3600e3)});q.on('dialog',d=>d.accept());
 await q.goto(B+u);await q.waitForFunction(()=>/Open Mock/.test(document.querySelector('#c-info').textContent));
 ok(!/\d+ (fixed )?questions/.test(await q.locator('#c-info').innerText()),'setup text shows no question count');
 await q.click('#c-start');await q.waitForSelector('#c-quiz:not(.hidden)');
 ok(await q.locator('#c-check').isHidden(),'sealed section is timed only (no check-answer button)');
 if(await q.locator('#c-answer .opt').count())await q.locator('#c-answer .opt').first().click();
 await q.click('#c-submit');await q.waitForSelector('#c-results:not(.hidden)');const res=await q.locator('#c-results').innerText();
 ok(/submitted/.test(res)&&/answers and solutions stay closed/.test(res)&&!/Solution:/.test(res)&&!/Correct answer/.test(res),'sealed results: no answers or solutions before the edition ends');
 const pend=await q.evaluate(()=>JSON.parse(localStorage.getItem('aptisetu.openmock.pending')||'{}'));ok(!!pend[m.id+':qa']&&pend[m.id+':qa'].ids.length>0,'responses kept in the browser for later scoring');
 ok(!e2.length,'sealed run: no page errors'+(e2.length?': '+e2[0]:''));await q.close();}}
// reused edition: an MCQ response goes to the server as the option's ORIGINAL position, whatever the shuffle shows
{const m=all.find(x=>!x.sealed&&x.pack==='mock-4');if(m){const q=await b.newPage();await q.clock.install({time:new Date(Date.parse(m.starts_at)+3600e3)});q.on('dialog',d=>d.accept());
 await q.goto(B+'cat-practice.html?mock=1');await q.evaluate(()=>sessionStorage.setItem('aptisetu.mock.user',JSON.stringify({id:'mock-2',email:'x@example.com'})));
 await q.goto(B+`cat-practice.html?mode=sectional&section=qa&pack=${m.pack}&open=${m.id}`);await q.waitForFunction(()=>window.Account&&!document.querySelector('#c-start').disabled);
 await q.evaluate(()=>{window.__sent=null;const f=Account.submitOpenMock;Account.submitOpenMock=(a,b2,r)=>{window.__sent=r;return f.call(Account,a,b2,r);};});
 await q.click('#c-start');await q.waitForSelector('#c-quiz:not(.hidden)');
 let picked=null;for(let i=0;i<22&&!picked;i++){if(await q.locator('#c-answer .opt').count()){const t=(await q.locator('#c-answer .opt').nth(2).locator('span').innerText()).trim();await q.locator('#c-answer .opt').nth(2).click();picked={i,t};}else await q.click('#c-next');}
 await q.click('#c-submit');await q.waitForFunction(()=>window.__sent);const sent=await q.evaluate(()=>window.__sent);
 const bank=JSON.parse(fs.readFileSync('data/cat/qa.json','utf8')).questions.filter(x=>x.pack===m.pack);const id=Object.keys(sent).find(k=>k!=='__score');const bq=bank.find(x=>x.id===id);
 ok(bq&&String(bq.options[sent[id]]).trim()===picked.t,'MCQ response sent in bank order (matches the option text chosen)');await q.close();}}
ok(!errs.length,'no page errors'+(errs.length?': '+errs[0]:''));
await b.close();console.log(f+' failed');process.exit(f?1:0);})();
