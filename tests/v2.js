// v2 design checks: chips row, mistakes notebook, Daily-10 parts, tracks page, QB question search, share links, home lab preview, grouped nav, no fabricated claims.
const {chromium}=require('playwright');const B=process.env.BASE||'http://localhost:8765/';const OUT=process.argv[2]||require('os').tmpdir();
let fails=0,n=0;const ok=(c,m,x)=>{n++;console.log((c?'PASS ':'FAIL ')+m+(c||x===undefined?'':' :: '+x));if(!c)fails++;};
(async()=>{const br=await chromium.launch();
 const ctx=await br.newContext({viewport:{width:390,height:844}});await ctx.grantPermissions(['clipboard-read','clipboard-write'],{origin:B.replace(/\/$/,'')});
 await ctx.route(/fonts\.(googleapis|gstatic)\.com|gc\.zgo\.at|supabase/,r=>r.abort());
 const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
 // home: chips, hero, lab preview, targets
 await p.goto(B);await p.evaluate(()=>localStorage.clear());await p.reload();
 ok(await p.isVisible('#chips-row'),'chips row visible');
 ok((await p.textContent('[data-chip=m] b')).trim()==='0','mistakes chip starts at 0');
 ok((await p.textContent('[data-chip=s] b')).trim()==='0','streak chip starts at 0');
 ok(/Sign in/.test(await p.textContent('[data-chip=a]'))&&(await p.getAttribute('[data-chip=a]','href'))==='login.html','sign-in chip links to login');
 ok(/See the maths/i.test(await p.textContent('.hero-v2 h1')),'v2 hero headline');
 ok((await p.$$('.hero-v2 .goal-chip')).length===4,'four track cards');
 ok(/1\/6 \+ 1\/12 = 1\/4/.test(await p.textContent('#pk-out'))&&/4 h/.test(await p.textContent('#pk-out')),'lab preview default 6 h + 12 h = 4 h');
 await p.$eval('#pk-a',e=>{e.value=10;e.dispatchEvent(new Event('input',{bubbles:true}))});await p.$eval('#pk-b',e=>{e.value=15;e.dispatchEvent(new Event('input',{bubbles:true}))});
 ok(/\b6 h\b/.test(await p.textContent('#pk-out')),'lab preview 10 h + 15 h = 6 h',await p.textContent('#pk-out'));
 ok((await p.getAttribute('#pk-link','href'))==='quant-lab-concept-lab.html?s=twA:10,twB:15,twC:0','lab preview links to Concept Lab with values');
 ok((await p.$$eval('.tcard',a=>a.map(x=>x.getAttribute('href')))).join()==='cat-practice.html?daily=1&part=qa,cat-practice.html?daily=1&part=dilr,cat-practice.html?daily=1&part=varc','target cards link to Daily 10 parts');
 ok((await p.$$('.pod a[href^="practice.html?section="]')).length===2,'placement pods link to real quizzes');
 ok(/whatsapp\.com\/channel/.test(await p.getAttribute('.om-alert a[href*="whatsapp"]','href')),'Open Mock alert uses WhatsApp channel');
 ok(await p.evaluate(()=>[...document.querySelectorAll('main .btn:not(.btn-ghost)')].filter(b=>{const r=b.getBoundingClientRect();return b.offsetParent&&r.top<innerHeight*1.5}).length)===1,'one primary button in the home hero screen');
 // nav groups
 const nav=await p.evaluate(()=>[...document.querySelectorAll('#site-header nav > ul > li, #site-header .nav > li, #site-header nav li.has-sub, #site-header nav > a')].map(x=>x.textContent.replace(/\s+/g,' ').trim().slice(0,40)));
 const navTxt=await p.textContent('#site-header');
 for(const g of ['Home','Quant Lab','Tracks & Practice','Question Bank','Flashcards & Guides','Careers','About & Legal'])ok(navTxt.includes(g),'nav has '+g);
 ok(!/Branch Patch|STAGING/i.test(navTxt),'no staging items in nav');
 // Daily 10 part
 await p.goto(B+'cat-practice.html?daily=1&part=qa',{waitUntil:'networkidle'});await p.waitForSelector('#c-quiz:not(.hidden)');
 const ids=(await p.getAttribute('#c-setup','data-daily')).split(',');ok(ids.length===3&&ids.every(x=>/^CQ/.test(x)),'?part=qa gives the 3 QA questions',ids.join());
 ok(/Quant mini-set/.test(await p.textContent('body')),'part title shown');
 for(const pt of ['dilr','varc']){await p.goto(B+'cat-practice.html?daily=1&part='+pt,{waitUntil:'networkidle'});await p.waitForSelector('#c-quiz:not(.hidden)');const d=(await p.getAttribute('#c-setup','data-daily')).split(',');ok(d.length===4,`?part=${pt} gives 4 questions`,d.join())}
 // mistakes: wrong answers land in the notebook and the chip
 await p.goto(B+'practice.html?daily=1',{waitUntil:'networkidle'});await p.waitForSelector('#quiz:not(.hidden)');
 for(let i=0;i<10;i++){await p.click('#opts .opt');await p.waitForTimeout(120);if(i<9&&await p.isVisible('#next'))await p.click('#next');}
 await p.click('#submit');await p.waitForSelector('#results:not(.hidden)');await p.waitForTimeout(200);
 const wrong=await p.evaluate(()=>Object.keys(JSON.parse(localStorage.getItem('aptisetu.mistakes.v1')||'{}')).length);
 const shownWrong=await p.$$eval('#results .opt.wrong',a=>a.length);
 ok(wrong===shownWrong,'notebook count equals wrong answers in the review',wrong+' vs '+shownWrong);
 ok((await p.textContent('[data-chip=m] b')).trim()===String(wrong),'mistakes chip shows real count');
 ok(await p.evaluate(()=>Notebook.seenCount())>=10,'questions marked as seen');
 // mistakes page
 await p.goto(B+'mistakes.html');await p.waitForTimeout(600);
 const items=await p.$$('.mk-item');ok(items.length===wrong,'mistakes page lists each mistake',items.length);
 if(wrong){ok(/q\/bank-ssc\//.test(await p.getAttribute('.mk-item a','href')||''),'mistake links to its question page',await p.getAttribute('.mk-item a','href'));
  await p.click('.mk-item [data-rm]');await p.waitForTimeout(200);ok((await p.$$('.mk-item')).length===wrong-1,'remove button works');}
 await p.screenshot({path:OUT+'/v2-mistakes.png',fullPage:true});
 p.once('dialog',d=>d.accept());if(await p.isVisible('#mk-clear'))await p.click('#mk-clear');await p.waitForTimeout(200);
 ok(await p.isVisible('#mk-empty')&&(await p.textContent('[data-chip=m] b')).trim()==='0','clear empties notebook and chip');
 // tracks
 await p.goto(B+'tracks.html');await p.waitForTimeout(400);
 await p.click('.lang-toggle button[data-lang=hi]');ok(await p.evaluate(()=>localStorage.getItem('aptisetu.sol-lang'))==='hi'&&(await p.getAttribute('.lang-toggle button[data-lang=hi]','aria-pressed'))==='true','tracks Hindi toggle saves choice');
 await p.click('.lang-toggle button[data-lang=en]');
 ok(/seen on this device: [1-9]/.test(await p.textContent('#nr-count')),'no-repeat count shown');
 p.once('dialog',d=>d.accept());await p.click('#nr-reset');ok(/: 0$/.test(await p.textContent('#nr-count')),'pool reset');
 ok((await p.$$('.trk')).length===4,'four track cards');ok(/40 min a section/.test(await p.textContent('.trk-cat')),'CAT weightage tags');
 const threfs=await p.$$eval('main a[href]',a=>[...new Set(a.map(x=>x.getAttribute('href').split('?')[0].split('#')[0]))].filter(h=>h&&!/^(https?:|mailto:)/.test(h)));
 for(const h of threfs){const r=await p.request.get(B+h);if(!r.ok())ok(false,'tracks link '+h+' exists')}ok(true,`tracks links checked (${threfs.length})`);
 ok(!(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1)),'tracks no overflow at 390');
 // QB question search + difficulty
 await p.goto(B+'q/index.html');await p.fill('#qf-q','trader marks');await p.waitForTimeout(800);
 ok(await p.isVisible('#qf-res')&&(await p.$$('#qf-qs li')).length>=1,'question search finds questions');
 ok(await p.$$eval('#qf-qs li',l=>l.every(x=>/trader marks/i.test(x.textContent))),'question results match the search');
 await p.fill('#qf-q','');await p.selectOption('#qf-d','Hard');await p.waitForTimeout(600);
 ok(await p.$$eval('#qf-qs li',l=>l.length>0&&l.every(x=>/Hard/.test(x.textContent))),'difficulty filter shows only Hard');
 // share-sim
 await p.goto(B+'quant-lab-concept-lab.html?s=twA:9,twB:18,twC:0');await p.waitForTimeout(800);
 ok(await p.evaluate(()=>{const e=document.querySelector('#twA,[data-id=twA]');return e&&e.value})==='9','?s= sets Concept Lab slider');
 await p.evaluate(()=>{const e=document.querySelector('#twA,[data-id=twA]');e.value=7;e.dispatchEvent(new Event('input',{bubbles:true}))});
 const c=p.locator('.ql-lab-grid > .card',{has:p.locator('#twA,[data-id=twA]')}).locator('.share-sim button');await c.click();await p.waitForTimeout(300);
 const clip=await p.evaluate(()=>navigator.clipboard.readText());ok(/\?s=twA:7,twB:18,twC:0/.test(clip),'copied link carries slider values',clip);
 await p.goto(B+'quant-lab-explainers.html');await p.waitForTimeout(800);ok((await p.$$('.share-sim')).length===1,'explainers have one share bar');
 // no fabricated claims anywhere we ship
 for(const u of ['index.html','about.html','tracks.html','open-mock.html','q/index.html','careers.html','mistakes.html']){const t=await (await p.request.get(B+u)).text();
  ok(!/1,428|840\+|support@aptisetu\.com|99\.8|Branch Patch|STAGING/i.test(t),u+': no fabricated counts, claims or staging text');}
 await p.goto(B+'about.html');ok(/Vaibhav Gupta/.test(await p.textContent('main'))&&/Career Launcher/.test(await p.textContent('main'))&&/edumaths360@gmail\.com/.test(await p.textContent('main')),'about names the real maker and email');
 ok(!errs.length,'no page errors',errs.join('|'));
 await br.close();console.log(`${fails} failed of ${n}`);process.exit(fails?1:0);})();
