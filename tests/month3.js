// Month 3 smoke: open-mock, account, pass, refund pages load without JS errors; Hindi toggle on a bank-ssc q page.
const {chromium}=require('playwright');const B='http://localhost:8765/';let f=0;
const ok=(c,m)=>{console.log((c?'PASS ':'FAIL ')+m);if(!c)f++};
(async()=>{const b=await chromium.launch();const p=await b.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
for(const u of['open-mock.html','account.html','pass.html','refund.html']){const r=await p.goto(B+u);ok(r.ok(),u+' loads');
 ok(await p.locator('.btn-primary, .btn.primary').count()<=1,u+' ≤1 primary button');}
const fs=require('fs');const d='q/bank-ssc/';const q='bank-ssc/'+fs.readdirSync(d).find(n=>n.endsWith('.html'));
await p.goto(B+'q/'+q);const t=p.locator('.lang-toggle button, .lang-toggle').first();ok(await t.count()>0,'Hindi toggle on '+q);
ok(errs.length===0,'no page errors '+errs.join('|'));await b.close();console.log(f+' failed');process.exit(f?1:0)})();
