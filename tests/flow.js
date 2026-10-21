const {chromium}=require('playwright');const B='http://localhost:8765/';const S='/workspace/edu-portal/screenshots/flow/';
(async()=>{const b=await chromium.launch();let fails=0,n=0;const ok=(t,c,x='')=>{n++;if(!c)fails++;console.log((c?'PASS ':'FAIL ')+t+(x?' — '+x:''))};
for(const W of [1280,390]){const p=await b.newPage({viewport:{width:W,height:W>500?900:844}});let errs=[];p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});p.on('pageerror',e=>errs.push(e.message));
 const vis=s=>p.locator(s).isVisible();
 // cat.html cards
 errs=[];await p.goto(B+'cat.html');const cards=p.locator('.sec-card');const cnt=await cards.count();
 const hrefs=await p.$$eval('.sec-card .cta-row',rs=>rs.map(r=>[...r.querySelectorAll('a')].map(a=>a.textContent.trim()+'|'+a.getAttribute('href'))));
 ok(`${W} cat.html: 3 cards × 3 buttons (Sets, sectional, Practise)`,cnt==3&&hrefs.every(h=>h.length==3&&/^Sets\|cat-(varc|dilr|quant)-sets\.html$/.test(h[0])&&/mode=sectional/.test(h[1])&&/mode=practice/.test(h[2])),JSON.stringify(hrefs));
 const fit=await p.$$eval('.sec-card .cta-row a',as=>as.every(a=>{const r=a.getBoundingClientRect(),c=a.closest('.sec-card').getBoundingClientRect();return r.right<=c.right+1}));ok(`${W} card buttons fit inside the card`,fit);
 await cards.first().scrollIntoViewIfNeeded();await p.locator('.sec-card').first().evaluate(e=>e.parentElement.scrollIntoView());await p.screenshot({path:S+`cat-cards-${W}.png`});
 // QA Practise click
 await p.locator('.sec-card',{hasText:'QA'}).locator('a',{hasText:'Practise'}).click();await p.waitForURL(/cat-practice/);await p.waitForTimeout(700);
 ok(`${W} QA Practise → summary "CAT · QA · Practice", steps hidden, topic visible`,(await p.textContent('#c-summary-text')).trim()=='CAT · QA · Practice'&&!(await vis('#c-choose'))&&await vis('#c-topic-wrap')&&await vis('#c-start')&&/Practice:/.test(await p.textContent('#c-info')));
 await p.screenshot({path:S+`practice-from-qa-practise-${W}.png`});
 await p.click('#c-start');await p.waitForTimeout(500);ok(`${W} QA practice starts`,/QA|Quant/.test(await p.textContent('#c-quiz'))&&await vis('#c-quiz'));
 // DILR sectional
 errs=[];await p.goto(B+'cat.html');await p.locator('.sec-card',{hasText:'DILR'}).locator('a',{hasText:'sectional'}).click();await p.waitForURL(/cat-practice/);await p.waitForTimeout(700);
 ok(`${W} DILR sectional → summary, no topic step`,(await p.textContent('#c-summary-text')).trim()=='CAT · DILR · Sectional'&&!(await vis('#c-choose'))&&!(await vis('#c-topic-wrap')));
 await p.screenshot({path:S+`practice-from-dilr-sectional-${W}.png`});
 await p.click('#c-change');ok(`${W} Change reveals full chooser with selections kept`,await vis('#c-choose')&&!(await vis('#c-summary'))&&await p.$eval('input[name=csec]:checked',e=>e.value)=='dilr'&&await p.$eval('input[name=cmode]:checked',e=>e.value)=='sectional');
 // plain page
 await p.goto(B+'cat-practice.html');await p.waitForTimeout(600);ok(`${W} plain cat-practice unchanged (steps visible, no summary)`,await vis('#c-choose')&&!(await vis('#c-summary')));await p.screenshot({path:S+`practice-plain-${W}.png`});
 // invalid params → full chooser
 await p.goto(B+'cat-practice.html?mode=foo&section=qa');ok(`${W} invalid mode → full chooser`,await vis('#c-choose'));
 await p.goto(B+'cat-practice.html?section=qa');ok(`${W} section only → full chooser (as before)`,await vis('#c-choose'));
 // topic link from cat.html
 await p.goto(B+'cat-practice.html?mode=practice&section=qa&topic=Geometry');await p.waitForTimeout(600);ok(`${W} topic link collapses and keeps topic`,!(await vis('#c-choose'))&&await p.$eval('#c-topic',e=>e.value)=='Geometry',await p.$eval('#c-topic',e=>e.value));
 // CUET
 await p.goto(B+'cuet.html');const ch=await p.$$eval('.sec-card .cta-row',rs=>rs.map(r=>r.querySelectorAll('a').length));
 await p.locator('.sec-card .cta-row a',{hasText:'Practise'}).first().click();await p.waitForURL(/cuet-practice/);await p.waitForTimeout(700);
 const ct=(await p.textContent('#c-summary-text')).trim();ok(`${W} CUET card Practise → collapsed (${ct})`,/^CUET · .+ · Practice$/.test(ct)&&!(await vis('#c-choose')),'cards '+JSON.stringify(ch));
 if(W==390)await p.screenshot({path:S+`cuet-practice-from-card-${W}.png`});
 ok(`${W} no console/CSP errors`,!errs.length,errs.join('|'));await p.close()}
console.log(`${fails} failed of ${n}`);await b.close()})()
