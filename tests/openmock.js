// Open Mock is UNRANKED practice: label shown, no leaderboard/rank anywhere, own saved scores only, repeat attempt keeps the first score.
const {chromium}=require('playwright');const B='http://localhost:8765/';let f=0;
const ok=(c,m)=>{console.log((c?'PASS ':'FAIL ')+m);if(!c)f++};
(async()=>{const b=await chromium.launch();const p=await b.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
const om=JSON.parse(require('fs').readFileSync('data/open-mock.json','utf8')).mocks.slice(-1)[0];
ok(om.ranked===false&&/Unranked practice, Mock 5 questions/.test(om.label),'open-mock.json: ranked false + label');
await p.goto(B+'open-mock.html');const txt=await p.locator('main, body').first().innerText();
ok(/Unranked practice, Mock 5 questions/.test(txt),'open-mock.html shows "Unranked practice, Mock 5 questions"');
ok(await p.locator('#om-board, #om-name, #om-me').count()===0,'no leaderboard, display-name form or rank box');
ok(!/your rank|counts for rank|all-India leaderboard|Rank<\/th>/i.test(await p.content()),'no rank copy on open-mock.html');
for(const u of['index.html','mock-tests.html','pass.html','privacy.html','terms.html','login.html']){const h=(await (await p.request.get(B+u)).text()).replace(/<script[\s\S]*?<\/script>/g,'');
 const bad=h.match(/[^.>]{0,40}(leaderboard|open mock rank|to be ranked)[^.<]{0,40}/gi)?.filter(s=>!/no (public )?leaderboard|unranked/i.test(s));ok(!bad||!bad.length,u+': no leaderboard/rank promise'+(bad&&bad.length?' -> '+bad[0]:''));}
await p.goto(B+'open-mock.html?mock=1');await p.evaluate(()=>sessionStorage.setItem('aptisetu.mock.user',JSON.stringify({id:'mock-1',email:'edumaths360@gmail.com'})));
await p.goto(B+'open-mock.html');await p.waitForFunction(()=>window.Account&&document.querySelector('#om-mine'));
const r1=await p.evaluate(id=>Account.submitOpenMock(id,'qa',{__score:42}),om.id);const r2=await p.evaluate(id=>Account.submitOpenMock(id,'qa',{__score:3}),om.id);
ok(r1.first_attempt===true&&r1.score===42,'first attempt saved');ok(r2.first_attempt===false&&r2.score===42,'repeat attempt returns the stored first score');
ok(typeof (await p.evaluate(()=>Account.leaderboard))==='undefined','Account.leaderboard removed');
await p.reload();await p.waitForFunction(()=>/42/.test(document.querySelector('#om-mine').innerText),null,{timeout:8000}).catch(()=>{});
const mine=await p.locator('#om-mine').innerText();ok(/QA\s+42/.test(mine)&&/not taken yet/.test(mine),'own saved scores shown');
ok(!errs.length,'no page errors'+(errs.length?': '+errs[0]:''));
await b.close();console.log(f+' failed');process.exit(f?1:0);})();
