// Phase 1 checks: formula flashcards, question-bank filters, career-table links. Same setup as tests/flow.js (server on :8765).
const {chromium}=require('playwright');const B='http://localhost:8765/';const OUT=process.argv[2]||require('os').tmpdir();
let fails=0;const ok=(c,m)=>{console.log((c?'PASS ':'FAIL ')+m);if(!c)fails++;};
(async()=>{const br=await chromium.launch();
 const ctx=await br.newContext({viewport:{width:390,height:844},deviceScaleFactor:2});
 await ctx.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.abort());
 const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error'&&!/ERR_FAILED|ERR_TUNNEL|fonts/.test(m.text()))errs.push(m.text())});
 await p.goto(B+'flashcards.html#reasoning');await p.waitForSelector('#fc-q');
 ok((await p.textContent('#fc-pos')).includes('Card 1'),'flashcards: starts at card 1');
 ok(await p.$eval('.fc-tab[aria-selected="true"]',e=>e.dataset.id)==='reasoning','hash opens reasoning deck');
 const q1=await p.textContent('#fc-q');ok(q1.endsWith('?')||q1.includes('?'),'front is a prompt: '+q1);
 await p.screenshot({path:OUT+'/1-flashcard-front.png',fullPage:false});
 await p.click('#fc-card');ok(await p.isVisible('#fc-a'),'flip shows answer');
 await p.screenshot({path:OUT+'/2-flashcard-back.png'});
 await p.click('#fc-know');ok((await p.textContent('#fc-known')).startsWith('1 of'),'knew-it counts');
 await p.keyboard.press('a');ok((await p.textContent('#fc-pos')).includes('Card 3'),'A key = review again, moves on');
 // finish deck
 for(let i=0;i<40;i++){if(await p.isVisible('#fc-done'))break;await p.click('#fc-know');}
 ok(await p.isVisible('#fc-done'),'deck finished screen');ok(await p.isVisible('#fc-review'),'review-missed button shown');
 await p.click('#fc-review');ok((await p.textContent('#fc-pos')).includes('of 1'),'review deck has the 1 missed card');
 await p.reload();ok((await p.textContent('#fc-known')).match(/^(\d+) of/)[1]>=10,'known progress persists after reload');
 const ov=await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1);ok(!ov,'no horizontal overflow at 390');
 // dark
 await p.evaluate(()=>document.documentElement.setAttribute('data-theme','dark'));await p.click('.fc-tab[data-id="cat-quant"]');
 await p.screenshot({path:OUT+'/3-flashcard-dark.png'});
 // q index filter
 await p.goto(B+'q/index.html');await p.click('.qf-chip[data-v="CAT"]');
 const vis=await p.$$eval('.card[data-t]',cs=>cs.filter(c=>c.offsetParent).map(c=>c.dataset.t));ok(vis.length>0&&vis.every(t=>t==='CAT'),'index exam filter: only CAT cards');
 await p.fill('#qf-q','percent');await p.waitForTimeout(100);await p.click('.qf-chip[data-v=""]');
 const lis=await p.$$eval('.qp-hubs li',ls=>ls.filter(l=>l.offsetParent).map(l=>l.textContent.toLowerCase()));ok(lis.length>0&&lis.every(t=>t.includes('percent')),'index search: '+lis.length+' percentage topics');
 await p.screenshot({path:OUT+'/4-qbank-search.png'});
 // hub difficulty
 await p.goto(B+'q/bank-ssc/quant-percentages.html');
 const chips=await p.$$eval('.qf-chip',c=>c.map(x=>x.dataset.v));ok(chips.length>=3,'hub chips: '+chips.join(','));
 await p.click('.qf-chip[data-v="Hard"]');const d=await p.$$eval('[data-qf-list] > li',ls=>ls.filter(l=>l.offsetParent).map(l=>l.dataset.d));ok(d.length>0&&d.every(x=>x==='Hard'),'hub difficulty filter: '+d.length+' Hard');
 await p.screenshot({path:OUT+'/5-hub-filter.png'});
 // career links
 await p.goto(B+'after-graduation.html');await p.fill('input[type=search]','SSC CGL').catch(()=>{});await p.waitForTimeout(200);
 const links=await p.$$eval('a.a12-link',as=>as.map(a=>a.getAttribute('href')));ok(links.includes('ssc-cgl.html'),'after-graduation links SSC CGL page: '+[...new Set(links)].join(','));
 await p.screenshot({path:OUT+'/6-career-link.png'});
 await p.goto(B+'formula-reasoning.html');ok(await p.$('a[href="flashcards.html#reasoning"]')!==null,'formula sheet links to its deck');
 ok(errs.length===0,'no JS errors '+errs.join('|'));
 await br.close();console.log(fails+' failed');process.exit(fails?1:0)})();
