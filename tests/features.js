// Month-1 features: question pages, Daily 10, post-test report, report links. Run: NODE_PATH=... node tests/features.js (server on :8765)
const {chromium}=require('playwright');const fs=require('fs');const B='http://localhost:8765/';
(async()=>{const b=await chromium.launch();let fails=0,n=0;const ok=(t,c,x='')=>{n++;if(!c)fails++;console.log((c?'PASS ':'FAIL ')+t+(x?' — '+x:''))};
const newP=async(w=1280)=>{const p=await b.newPage({viewport:{width:w,height:900}});p.errs=[];p.on('console',m=>{if(m.type()==='error')p.errs.push(m.text())});p.on('pageerror',e=>p.errs.push(e.message));return p};
// static checks
const sm=fs.readFileSync('sitemap.xml','utf8');const qfiles=['cat','cuet','bank-ssc'].flatMap(t=>fs.readdirSync('q/'+t).map(f=>`q/${t}/${f}`));
ok('every q/ page is in sitemap.xml',qfiles.every(f=>sm.includes('https://aptisetu.com/'+f))&&sm.includes('q/index.html'),qfiles.length+' files');
const mockIds=new Set(['cat/qa','cat/dilr','cat/varc'].flatMap(f=>JSON.parse(fs.readFileSync(`data/${f}.json`)).questions.filter(q=>q.pack&&!q.pack.startsWith('practice-')).map(q=>q.id.toLowerCase())));
ok('no mock/sectional pack question has a page',!fs.readdirSync('q/cat').some(f=>mockIds.has(f.split('-')[0])));
ok('no page uses the personal address',!qfiles.some(f=>fs.readFileSync(f,'utf8').includes('vaibhavgupta2424')));
// question page render, answer matches the bank
{const p=await newP(390);const f=fs.readdirSync('q/cat').find(x=>/^cq1-/.test(x));await p.goto(B+'q/cat/'+f,{waitUntil:'networkidle'});
 const qa=JSON.parse(fs.readFileSync('data/cat/qa.json')).questions.find(q=>q.id==='CQ1');
 await p.click('.qp-ans summary');const t=await p.textContent('.qpage');
 ok('question page shows question, answer and solution',t.includes('Correct answer: '+qa.answer)&&await p.isVisible('.qp-ans .sol'));
 ok('question page has report link to edumaths360',/mailto:edumaths360@gmail\.com\?subject=Error%20report%3A%20question%20CQ1/.test(await p.getAttribute('.report-link','href')));
 ok('question page has 3-5 similar questions',(n=>n>=3&&n<=5)(await p.locator('.qp-sim li').count()));
 ok('question page has practice CTA and JSON-LD',/cat-practice\.html\?mode=practice&section=qa&topic=/.test(await p.getAttribute('.cta-row a.btn','href'))&&JSON.parse(await p.textContent('script[type="application/ld+json"]'))['@type']==='Quiz');
 ok('header nav rendered (relative links work under q/)',(await p.getAttribute('#site-header .logo','href'))==='index.html'&&(await p.evaluate(()=>document.querySelector('#site-header .logo').href))===B+'index.html');
 const sim=await p.getAttribute('.qp-sim a','href');await p.goto(B+sim);ok('similar link opens a question page',await p.isVisible('.qpage'));
 ok('question page: no console errors',!p.errs.length,p.errs.join('|'));await p.close()}
{const p=await newP();const f=fs.readdirSync('q/bank-ssc').find(x=>/^d1-/.test(x));await p.goto(B+'q/bank-ssc/'+f,{waitUntil:'networkidle'});ok('bank DILR page shows data',await p.isVisible('.q-data'));
 await p.goto(B+'q/index.html');ok('question bank index lists hubs',(await p.locator('.qp-hubs a').count())>50);
 await p.click('.qp-hubs a');ok('hub lists questions',(await p.locator('.qp-list a').count())>=1);ok('hub/index: no console errors',!p.errs.length,p.errs.join('|'));await p.close()}
// Daily 10
{const p=await newP();await p.goto(B);const hs=await p.$$eval('.daily-card a',a=>a.map(x=>x.textContent+'|'+x.getAttribute('href')));
 ok('home has Start today\'s 10 per track',hs.length===3&&hs.every(h=>h.startsWith("Start today's 10|")),hs.join(' '));
 const ids=[];for(let k=0;k<2;k++){const c=await b.newContext();const q=await c.newPage();await q.goto(B+'cat-practice.html?daily=1',{waitUntil:'networkidle'});await q.waitForSelector('#c-quiz:not(.hidden)');ids.push(await q.getAttribute('#c-setup','data-daily'));
  if(k===0){ok('CAT Daily 10 has QA + one DILR set + one RC set (11)',(await q.textContent('#c-qnum')).includes('of 11'));ok('exam view has report link',/mailto:edumaths360/.test(await q.getAttribute('#c-report .report-link','href')))}await c.close()}
 ok('Daily 10 deterministic for the same date',ids[0]&&ids[0]===ids[1]&&ids[0].split(',').length===11);
 {const q=await b.newPage();await q.goto(B+'cat-practice.html?daily=1',{waitUntil:'networkidle'});await q.waitForSelector('#c-quiz:not(.hidden)');const ids=(await q.getAttribute('#c-setup','data-daily')).split(',');ok('CAT daily mixes QA, DILR and VARC',ids.filter(x=>/^CQ/.test(x)).length===3&&ids.length===11,ids.join());await q.close()}
 {const q=await b.newPage();await q.goto(B+'cuet-practice.html?daily=1',{waitUntil:'networkidle'});await q.waitForSelector('#c-quiz:not(.hidden)');const ids=(await q.getAttribute('#c-setup','data-daily')).split(',');ok('CUET daily uses CUET-specific items',!ids.some(x=>/^G-/.test(x)),ids.join());await q.close()}
 for(const u of ['cuet-practice.html?daily=1']){await p.goto(B+u,{waitUntil:'networkidle'});await p.waitForSelector('#c-quiz:not(.hidden)');ok(u+' starts 10',(await p.textContent('#c-qnum')).includes('of 10'))}
 await p.goto(B+'practice.html?daily=1',{waitUntil:'networkidle'});await p.waitForSelector('#quiz:not(.hidden)');ok('Bank/SSC daily starts 10',(await p.textContent('#q-num')).includes('of 10')&&/Daily 10/.test(await p.textContent('#quiz-title')));
 ok('daily pages: no console errors',!p.errs.length,p.errs.join('|'));await p.close()}
// post-test report + progress graph after 2 attempts
{const c=await b.newContext();const p=await c.newPage();p.on('dialog',d=>d.accept());const errs=[];p.on('pageerror',e=>errs.push(e.message));
 for(let k=0;k<2;k++){await p.goto(B+'cat-practice.html?mode=practice&section=qa',{waitUntil:'networkidle'});await p.click('#c-start');await p.waitForSelector('#c-quiz:not(.hidden)');
  if(await p.locator('#c-answer .opt').count())await p.click('#c-answer .opt');await p.click('#c-submit');await p.waitForSelector('#c-results:not(.hidden)');
  const hasG=await p.locator('.prog-graph').count();ok(`attempt ${k+1}: weak topics + time per question shown`,await p.isVisible('.weak-list, .report-extra p')&&(await p.locator('.tpq-col').count())>0);
  ok(`attempt ${k+1}: progress graph ${k?'shown':'hidden'}`,k?hasG===1:hasG===0)}
 await p.screenshot({path:'/tmp/report.png',fullPage:false});ok('report: no page errors',!errs.length,errs.join('|'));await c.close()}
// Bank/SSC post-test report
{const c=await b.newContext();const p=await c.newPage();p.on('dialog',d=>d.accept());const errs=[];p.on('pageerror',e=>errs.push(e.message));
 for(let k=0;k<2;k++){await p.goto(B+'practice.html?daily=1',{waitUntil:'networkidle'});await p.waitForSelector('#quiz:not(.hidden)');await p.click('#opts .opt');await p.waitForTimeout(300);await p.click('#next');await p.click('#submit');await p.waitForSelector('#results:not(.hidden)');
  ok(`bank report ${k+1}: topic table, weak topics, time chart`,(await p.locator('#res-summary .topic-acc tr').count())>1&&(await p.locator('#res-summary .tpq-col').count())===10&&await p.isVisible('#res-summary .weak-list, #res-summary .report-extra p'));
  ok(`bank report ${k+1}: progress graph ${k?'shown':'hidden'}`,(await p.locator('#res-summary .prog-graph').count())===(k?1:0))}
 ok('bank report: no page errors',!errs.length,errs.join('|'));await c.close()}
// Month 2 content: facts boxes, exam pages, guides, formula sheets
{const NEW=['bank-ssc.html','ibps-po.html','ibps-clerk.html','sbi-po.html','ssc-cgl.html','ssc-chsl.html','guides.html','formula-sheets.html','formula-cat-quant.html','formula-bank-ssc-quant.html','formula-reasoning.html',...fs.readdirSync('.').filter(f=>/^guide-.*\.html$/.test(f))];
 ok('10 guides built',NEW.filter(f=>f.startsWith('guide-')).length===10);
 ok('new pages are in sitemap.xml',NEW.every(f=>sm.includes('https://aptisetu.com/'+f)));
 ok('3 formula PDFs exist',['cat-quant','bank-ssc-quant','reasoning'].every(s=>fs.statSync('assets/pdf/formula-'+s+'.pdf').size>10000));
 const p=await b.newPage({viewport:{width:360,height:800}});const errs=[];p.on('pageerror',e=>errs.push(e.message));let bad=[];
 for(const f of ['cat.html','cuet.html',...NEW]){await p.goto(B+f,{waitUntil:'domcontentloaded'});
  const r=await p.evaluate(()=>({w:document.documentElement.scrollWidth,prim:[...document.querySelectorAll('main .btn:not(.btn-ghost), .page-head .btn:not(.btn-ghost), .container .btn:not(.btn-ghost)')].filter(e=>e.offsetParent).length,facts:document.querySelectorAll('.facts').length,toc:!!document.querySelector('.toc'),ins:!!document.querySelector('.insight'),faq:document.querySelectorAll('.faq-item').length,src:document.querySelectorAll('.sources li').length}));
  if(r.w>360)bad.push(f+' overflow '+r.w);if(NEW.includes(f)&&r.prim>1)bad.push(f+' primary buttons '+r.prim);
  if((/^(cat|cuet|bank-ssc|ibps|sbi|ssc)/.test(f))&&r.facts!==1)bad.push(f+' facts '+r.facts);
  if(f.startsWith('guide-')&&!(r.toc&&r.ins&&r.faq>=2&&r.src>=1))bad.push(f+' guide format');}
 ok('new pages: facts boxes, guide format, 1 primary CTA, no overflow at 360px',!bad.length,bad.join('; '));
 ok('new pages: no page errors',!errs.length,errs.join('|'));await p.close()}
console.log(`${fails} failed of ${n}`);await b.close();process.exit(fails?1:0)})();
