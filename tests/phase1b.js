// Phase 1b checks: home goal selector, contact report builder, backup code, WebSite JSON-LD. Server on :8765 (see tests/flow.js).
const {chromium}=require('playwright');const B='http://localhost:8765/';const OUT=process.argv[2]||require('os').tmpdir();
let fails=0;const ok=(c,m)=>{console.log((c?'PASS ':'FAIL ')+m);if(!c)fails++;};
(async()=>{const br=await chromium.launch();
 const ctx=await br.newContext({viewport:{width:390,height:844},deviceScaleFactor:2});
 await ctx.route(/fonts\.(googleapis|gstatic)\.com|gc\.zgo\.at|supabase/,r=>r.abort());
 const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
 // home
 await p.goto(B);const ld=await p.$eval('script[type="application/ld+json"]',s=>JSON.parse(s.textContent));ok(ld['@type']==='WebSite'&&/aptisetu/.test(ld.url),'WebSite JSON-LD valid');
 ok(await p.isVisible('[data-goal-pane="cat"]')&&!(await p.isVisible('[data-goal-pane="bank"]')),'CAT pane shown by default');
 await p.click('[data-goal="bank"]');ok(await p.isVisible('[data-goal-pane="bank"]')&&(await p.getAttribute('[data-goal="bank"]','aria-pressed'))==='true','bank chip shows bank pane');
 ok(await p.$eval('[data-goal-pane="bank"] a.btn',a=>a.getAttribute('href'))==='bank-ssc.html','bank primary link');
 await p.reload();ok(await p.isVisible('[data-goal-pane="bank"]'),'choice remembered');
 await p.screenshot({path:OUT+'/7-home-goal.png'});
 ok(!(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1)),'home no overflow at 390');
 for(const k of ['cat','cuet','placements']){await p.click(`[data-goal="${k}"]`);const hs=await p.$$eval(`[data-goal-pane="${k}"] a`,as=>as.map(a=>a.getAttribute('href')));for(const h of hs){const r=await p.request.get(B+h.split('?')[0]);ok(r.ok(),`${k} link ${h} exists`)}}
 // contact
 await p.goto(B+'contact.html?q=Q23');ok((await p.inputValue('#rp-qid'))==='Q23','question ID prefilled from ?q=');
 await p.click('#rp-form button[type=submit]');ok(/Details/.test(await p.textContent('#rp-msg')),'empty details blocked');
 await p.selectOption('#rp-type','Wrong answer or solution');await p.fill('#rp-body','Answer should be 7.2 days, key says 6.');
 await p.click('#rp-form button[type=submit]');ok(/email app/.test(await p.textContent('#rp-msg')),'submit says email app opens');
 await p.screenshot({path:OUT+'/8-contact-report.png',fullPage:false});
 // backup
 await p.goto(B+'login.html');ok(/backup code/.test(await p.textContent('#login-box')),'login notice points to backup');
 await p.evaluate(()=>{localStorage.clear();localStorage.setItem('aptisetu.history','[{"s":5}]');localStorage.setItem('fc:reasoning','["x"]');localStorage.setItem('sb-abc-auth-token','SECRET');localStorage.setItem('aptisetu.mock.user','u');});
 await p.click('#bk-make');const code=await p.inputValue('#bk-code');ok(code.startsWith('APTI1.'),'backup code made');
 const dec=JSON.parse(Buffer.from(code.slice(6),'base64').toString('utf8'));ok(dec.data['aptisetu.history']&&dec.data['fc:reasoning'],'code carries progress keys');ok(!dec.data['sb-abc-auth-token']&&!dec.data['aptisetu.mock.user'],'code excludes login token and test keys');
 await p.evaluate(()=>localStorage.clear());await p.fill('#bk-code','hello');await p.click('#bk-check');ok(/not an AptiSetu/.test(await p.textContent('#bk-msg')),'rejects bad code');
 await p.fill('#bk-code',code);await p.click('#bk-check');ok(await p.isVisible('#bk-apply'),'asks before replacing');
 await p.screenshot({path:OUT+'/9-backup.png'});
 await p.click('#bk-apply');const h=await p.evaluate(()=>localStorage.getItem('aptisetu.history'));ok(h==='[{"s":5}]','progress restored');
 const evil='APTI1.'+Buffer.from(JSON.stringify({app:'aptisetu',v:1,data:{'sb-x-auth-token':'EVIL','aptisetu.history':'[]'}})).toString('base64');
 await p.fill('#bk-code',evil);await p.click('#bk-check');await p.click('#bk-apply');ok(await p.evaluate(()=>localStorage.getItem('sb-x-auth-token'))===null,'restore ignores non-progress keys');
 ok(errs.length===0,'no JS errors '+errs.join('|'));
 await br.close();console.log(fails+' failed');process.exit(fails?1:0)})();
