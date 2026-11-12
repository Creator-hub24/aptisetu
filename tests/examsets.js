// CUET / Bank / SSC practice sets: data rules, hubs, guest access, unlocking, timers, marking, saved progress keys,
// light + dark screenshots at 390 px. Server on :8765 (see tests/flow.js). Run: NODE_PATH=<playwright> node tests/examsets.js
const {chromium}=require('playwright');const fs=require('fs'),path=require('path');
const B=process.env.BASE||'http://localhost:8765/';const ROOT=path.join(__dirname,'..');const S=process.env.SHOTS||path.join(ROOT,'screenshots/phase1/');
let fails=0,n=0;const ok=(c,m,x='')=>{n++;if(!c)fails++;console.log((c?'PASS ':'FAIL ')+m+(x?' — '+x:''))};
const J=f=>JSON.parse(fs.readFileSync(path.join(ROOT,f),'utf8'));
const META={cuet:J('data/sets/cuet.json'),bank:J('data/sets/bank.json'),ssc:J('data/sets/ssc.json')};
const RULE={cuet:{c:5,w:-1,size:{gat:25,english:25,maths:25},timer:{gat:30,english:30,maths:30}},
            bank:{c:1,w:-0.25,size:{quant:35,reasoning:35,di:10},timer:{quant:20,reasoning:20,di:6}},
            ssc:{c:2,w:-0.5,size:{maths:25,reasoning:25},timer:{maths:15,reasoning:15}}};
const LV=['Easy','Medium','Hard'];
// ---------- data rules (no browser) ----------
{const seen=new Map();let allOk=true,levelOk=true,sizeOk=true,metaOk=true;
 for(const [ex,m] of Object.entries(META)){
  metaOk=metaOk&&m.marks.correct===RULE[ex].c&&m.marks.wrong===RULE[ex].w;
  for(const [sec,r] of Object.entries(m.sections)){
   const src=J(r.src).questions,by=new Map(src.map(q=>[q.id,q]));
   if(r.size!==RULE[ex].size[sec]||r.timer!==RULE[ex].timer[sec])metaOk=false;
   let prevEnd=0;for(const L of LV){const g=r[L];if(g.range[0]!==prevEnd+1)metaOk=false;prevEnd=g.range[1];
    for(const st of g.ready){if(st.set<g.range[0]||st.set>g.range[1])metaOk=false;if(st.ids.length!==r.size||new Set(st.ids).size!==r.size)sizeOk=false;
     // level rule: each whole passage / data set takes the majority level (ties go harder)
     const grp=new Map();st.ids.forEach(i=>{const q=by.get(i);if(!q){allOk=false;return}const k=q.set||q.id;(grp.get(k)||grp.set(k,[]).get(k)).push(q)});
     for(const qs of grp.values()){const c=LV.map(l=>qs.filter(q=>q.difficulty===l).length),top=Math.max(...c);const lvl=LV[c.lastIndexOf(top)];if(lvl!==L)levelOk=false;
      const full=src.filter(q=>(q.set||q.id)===(qs[0].set||qs[0].id));if(qs[0].set&&full.length!==qs.length)levelOk=false;}
     for(const i of st.ids){const q=by.get(i);if(!q)continue;if(ex==='cuet'&&q.source==='general')allOk=false;const k=r.src+'|'+i;if(seen.has(k)){allOk=false;console.log('  dup',k,seen.get(k),ex,sec,st.set)}seen.set(k,ex+' '+sec+' '+st.set);}}}
   if(prevEnd!==r.count)metaOk=false;}}
 ok(metaOk,'sets JSON: marking, set sizes, timers and level ranges match the official-pattern config');
 ok(sizeOk,'every ready set has exactly its set size, no repeated question inside a set');
 ok(allOk,'each question is in at most one set across CUET, Bank and SSC; CUET sets use no shared Bank/SSC items');
 ok(levelOk,'set level = question difficulty tag (passages/data sets whole, majority level)');
 const cq=J('data/cat/sets.json');ok(cq.timers.qa===20&&cq.timers.varc===20&&cq.timers.dilr===25,'CAT set timers unchanged (20/20/25)');}
(async()=>{const br=await chromium.launch();
 const mk=async(scheme='light')=>{const ctx=await br.newContext({viewport:{width:390,height:844},colorScheme:scheme});await ctx.route(/fonts\.(googleapis|gstatic)\.com|gc\.zgo\.at|supabase\.co/,r=>r.abort());return ctx};
 const watch=p=>{const e=[];p.on('pageerror',x=>e.push(x.message));p.on('console',m=>{if(m.type()==='error'&&!/Failed to load resource|ERR_FAILED|net::/.test(m.text()))e.push(m.text())});return e};
 const HUBS=Object.entries(META).flatMap(([ex,m])=>Object.keys(m.sections).map(sec=>[ex,sec]));
 // ---------- hubs (guest) ----------
 {const ctx=await mk();const p=await ctx.newPage();const errs=watch(p);
  for(const [ex,sec] of HUBS){const r=META[ex].sections[sec],ready=LV.flatMap(L=>r[L].ready.map(x=>x.set)),guest=Math.min(...ready);
   await p.goto(B+`${ex}-${sec}-sets.html`,{waitUntil:'networkidle'});await p.waitForTimeout(250);
   const cards=await p.$$eval('#set-hub .set-card',cs=>cs.map(c=>[c.querySelector('b').textContent,c.querySelector('.sbadge').textContent.trim(),c.getAttribute('href')||'']));
   const want=[];for(let k=1;k<=r.count;k++)want.push(!ready.includes(k)?'Coming soon':k===guest?'Start →':'🔒 Login to unlock');
   ok(cards.length===r.count&&cards.every((c,i)=>c[1]===want[i]),`${ex}-${sec} hub: ${ready.length} ready of ${r.count}; guest set ${guest} open, others locked or Coming soon`,JSON.stringify(cards.map(c=>c[1][0])));
   const g=cards[guest-1];ok(g&&g[2]===`set.html?exam=${ex}&sec=${sec}&set=${guest}`,`${ex}-${sec} guest link`,g&&g[2]);
   const txt=await p.textContent('main');ok(!/\b\d+\s+questions? (each|per set)\b|\bquestions each\b/i.test(txt),`${ex}-${sec} hub shows no question counts`);
   ok(new RegExp(`\\b${r.timer} min per set|${r.timer}-minute timer`).test(txt),`${ex}-${sec} hub shows the ${r.timer}-minute timer`);
   ok(!(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1)),`${ex}-${sec} hub fits 390 px`);}
  ok(!errs.length,'hubs: no JS / CSP errors',errs.join(' | '));await ctx.close();}
 // ---------- guest access on set.html ----------
 {const ctx=await mk();const p=await ctx.newPage();const errs=watch(p);
  for(const [ex,sec] of HUBS){const r=META[ex].sections[sec],ready=LV.flatMap(L=>r[L].ready.map(x=>x.set)),guest=Math.min(...ready),other=ready.find(k=>k!==guest),soon=[...Array(r.count).keys()].map(i=>i+1).find(k=>!ready.includes(k));
   await p.goto(B+`set.html?exam=${ex}&sec=${sec}&set=${guest}`,{waitUntil:'networkidle'});await p.waitForSelector('#c-start:not([disabled])',{timeout:5000}).catch(()=>{});
   const info=await p.textContent('#set-info');ok(await p.isVisible('#c-start')&&info.includes(r.timer+'-minute timer'),`${ex}-${sec} guest: set ${guest} opens, ${r.timer}-minute timer`,info.trim().slice(0,90));
   ok(!/\d+ questions/.test(info),`${ex}-${sec} set info shows no question count`);
   if(other){await p.goto(B+`set.html?exam=${ex}&sec=${sec}&set=${other}`,{waitUntil:'networkidle'});await p.waitForTimeout(300);
    ok(/login/i.test(await p.textContent('#set-info'))&&!(await p.isVisible('#c-start')),`${ex}-${sec} guest: set ${other} asks for login`);}
   if(soon){await p.goto(B+`set.html?exam=${ex}&sec=${sec}&set=${soon}`,{waitUntil:'networkidle'});await p.waitForTimeout(300);
    ok(/coming soon/i.test(await p.textContent('#set-info'))&&!(await p.isVisible('#c-start')),`${ex}-${sec} set ${soon} is Coming soon`);}}
  for(const bad of ['set.html?exam=cuet&sec=qa&set=1','set.html?exam=xyz&sec=gat&set=1','set.html?exam=bank&sec=__proto__&set=1','set.html?exam=ssc&sec=maths&set=99']){await p.goto(B+bad,{waitUntil:'networkidle'});await p.waitForTimeout(300);
   ok(/doesn't exist/.test(await p.textContent('#set-info'))&&!(await p.isVisible('#c-start')),`bad URL handled: ${bad}`);}
  ok(!errs.length,'set pages: no JS / CSP errors',errs.join(' | '));await ctx.close();}
 // ---------- timers, marking and saved progress (mock login) ----------
 const login=async ctx=>{const p=await ctx.newPage();await p.goto(B+'login.html?mock=1');await p.evaluate(()=>{sessionStorage.setItem('aptisetu.mock.user',JSON.stringify({id:'mock-t@x.in',email:'t@x.in'}));sessionStorage.removeItem('aptisetu.mock.progress')});return p};
 const answerKey=ex=>{const m={};for(const r of Object.values(META[ex].sections))for(const q of J(r.src).questions)m[q.id]=q;return m};
 const curId=async p=>{const h=await p.$eval('#c-report a',a=>a.getAttribute('href')).catch(()=>'');const m=decodeURIComponent(h||'').match(/question ([A-Za-z0-9-]+)/);return m&&m[1]};
 for(const [ex,sec] of [['cuet','gat'],['bank','quant'],['bank','di'],['ssc','maths']]){const ctx=await mk();const p=await login(ctx);const errs=watch(p);const r=META[ex].sections[sec],R=RULE[ex];const first=Math.min(...LV.flatMap(L=>r[L].ready.map(x=>x.set)));
  await p.goto(B+`set.html?exam=${ex}&sec=${sec}&set=${first}`,{waitUntil:'networkidle'});await p.waitForSelector('#c-start:not([disabled])');await p.click('#c-start');await p.waitForTimeout(400);
  const tm=(await p.textContent('#c-timer')).trim(),mm=String(r.timer).padStart(2,'0');ok(new RegExp(`${mm}:00|${String(r.timer-1).padStart(2,'0')}:5\\d`).test(tm),`${ex}-${sec}: clock starts at ${mm}:00`,tm);
  const nq=(await p.textContent('#c-qnum')).match(/of (\d+)/)[1];ok(+nq===r.size,`${ex}-${sec}: set runs ${r.size} questions`,nq);
  const marks=(await p.textContent('#c-marks')).trim();ok(marks===`+${R.c} / −${Math.abs(R.w)}`,`${ex}-${sec}: marks shown ${marks}`);
  const key=answerKey(ex);
  // Q1 right, Q2 wrong, rest blank
  for(let k=0;k<2;k++){const id=await curId(p),q=key[id];const opts=await p.$$('#c-answer .opt');let hit=-1;
   for(let i=0;i<opts.length;i++){const h=await opts[i].$eval('span',s=>s.innerHTML);if(h===q.options[q.answer])hit=i;}
   if(hit<0){ok(false,`${ex}-${sec}: found the correct option for ${id}`);break}
   await opts[k===0?hit:(hit+1)%opts.length].click();await p.click('#c-next');await p.waitForTimeout(80);}
  if(ex==='cuet')await p.screenshot({path:S+'set-cuet-gat-running-390-light.png'});
  p.once('dialog',d=>d.accept());await p.click('#c-submit');await p.waitForSelector('#c-results:not(.hidden)');await p.waitForTimeout(500);
  const sc=parseFloat(await p.$eval('#c-res-head .kpi.main b',e=>e.textContent)),want=R.c+R.w;ok(Math.abs(sc-want)<1e-9,`${ex}-${sec}: 1 right + 1 wrong scores ${want}`,String(sc));
  const out=await p.$eval('#c-res-head .kpi.main span',e=>e.textContent);ok(out.includes(String(R.c*r.size)),`${ex}-${sec}: out of ${R.c*r.size}`,out);
  const rows=await p.evaluate(()=>JSON.parse(sessionStorage.getItem('aptisetu.mock.progress')||'[]'));const row=rows.find(x=>x.section===`${ex}-${sec}`);
  ok(row&&row.set_no===first&&Math.abs(row.score-want)<1e-9&&row.total===R.c*r.size,`${ex}-${sec}: saved to set_progress as section "${ex}-${sec}", set ${first}`,JSON.stringify(rows));
  ok(/Saved to your account/.test(await p.textContent('#set-save')),`${ex}-${sec}: result page says saved`);
  ok(!errs.length,`${ex}-${sec}: no JS errors`,errs.join(' | '));await ctx.close();}
 // auto-submit when the SSC 15-minute timer runs out
 {const ctx=await mk();const p=await login(ctx);await p.clock.install();await p.goto(B+'set.html?exam=ssc&sec=reasoning&set=1',{waitUntil:'networkidle'});await p.waitForSelector('#c-start:not([disabled])');await p.click('#c-start');
  await p.clock.runFor(14*60*1000);const before=await p.$eval('#c-results',e=>e.classList.contains('hidden'));await p.clock.runFor(61*1000);
  ok(before&&await p.$eval('#c-results',e=>!e.classList.contains('hidden')),'SSC set still running at 14 min, auto-submits at 15 min');await ctx.close();}
 // ---------- unlocking (mock login) and no collision with CAT rows ----------
 {const ctx=await mk();const p=await login(ctx);
  const st=async(ex,sec)=>p.evaluate(([e,s])=>CatSets.status(s,e).then(x=>x.sets.map(y=>y.state)),[ex,sec]);
  const put=rows=>p.evaluate(r=>sessionStorage.setItem('aptisetu.mock.progress',JSON.stringify(r)),rows);
  await p.goto(B+'cuet-maths-sets.html',{waitUntil:'networkidle'});
  let s=await st('cuet','maths');ok(s[0]==='open'&&s[1]==='open'&&s[3]==='locked',"cuet-maths logged in: Easy open, Medium locked",s.join());
  await put([{section:'cuet-maths',set_no:1,score:10,total:125},{section:'qa',set_no:2,score:3,total:30}]);s=await st('cuet','maths');ok(s[0]==='done'&&s[3]==='locked','one Easy set done (and a CAT row for set 2): Medium still locked',s.join());
  await put([{section:'cuet-maths',set_no:1,score:10,total:125},{section:'cuet-maths',set_no:2,score:0,total:125}]);s=await st('cuet','maths');ok(s[3]==='open'&&s[4]==='open','all Easy sets done: Medium unlocks',s.join());
  s=await st('cat','qa');ok(s[0]==='open'&&s[1]==='open'&&!s.includes('done'),'CUET rows do not mark CAT sets done (no collision)',s.slice(0,3).join());
  await put([{section:'qa',set_no:1,score:30,total:30}]);s=await st('cuet','maths');ok(s[0]==='open','CAT row for qa set 1 does not mark CUET set 1 done',s[0]);
  s=await st('bank','reasoning');ok(s[3]==='open'&&s.slice(0,3).every(x=>x==='soon'),'bank-reasoning: no Easy sets yet, so Medium is open',s.join());
  await put([]);s=await st('ssc','maths');ok(s[6]==='locked','ssc-maths Hard locked before Medium is done',s.join());
  await put([{section:'ssc-maths',set_no:1,score:1,total:50},{section:'ssc-maths',set_no:4,score:1,total:50},{section:'ssc-maths',set_no:5,score:1,total:50}]);s=await st('ssc','maths');ok(s[6]==='open','ssc-maths Hard unlocks after Easy + Medium',s.join());
  await put([{section:'bank-quant',set_no:1,score:5.75,total:35}]);await p.goto(B+'bank-quant-sets.html',{waitUntil:'networkidle'});await p.waitForTimeout(300);
  ok(/Done · 5\.75\/35/.test(await p.textContent('#set-hub')),'hub shows a fractional Bank score as done');
  await ctx.close();}
 // ---------- screenshots: hubs, one set page per exam, home (light + dark, 390) ----------
 for(const scheme of ['light','dark']){const ctx=await mk(scheme);const p=await ctx.newPage();
  for(const [ex,sec] of HUBS){await p.goto(B+`${ex}-${sec}-sets.html`,{waitUntil:'networkidle'});await p.waitForTimeout(250);await p.screenshot({path:S+`hub-${ex}-${sec}-390-${scheme}.png`,fullPage:true});}
  for(const [ex,sec,k] of [['cuet','gat',1],['bank','quant',1],['ssc','maths',1]]){await p.goto(B+`set.html?exam=${ex}&sec=${sec}&set=${k}`,{waitUntil:'networkidle'});await p.waitForSelector('#c-start:not([disabled])');await p.screenshot({path:S+`set-${ex}-${sec}-${k}-390-${scheme}.png`});
   await p.click('#c-start');await p.waitForTimeout(400);await p.screenshot({path:S+`set-${ex}-${sec}-${k}-running-390-${scheme}.png`});}
  await p.goto(B+'index.html',{waitUntil:'networkidle'});await p.waitForTimeout(300);await p.screenshot({path:S+`home-390-${scheme}.png`,fullPage:true});
  const t=await p.textContent('main');ok(!/\b\d[\d,]*\s+(free\s+)?questions\b/i.test(t.replace(/\d+ question types/g,'')),`home (${scheme}) shows no question counts`);
  await p.goto(B+'cuet.html');ok(!/\b(562|128|169|345)\b/.test(await p.textContent('main')),`cuet.html (${scheme}) has no question-count table numbers`);
  await ctx.close();}
 // header chip
 {const ctx=await mk();const p=await login(ctx);await p.goto(B+'index.html',{waitUntil:'networkidle'});await p.waitForTimeout(400);
  const chip=(await p.textContent('[data-chip=a]')).trim();ok(chip==='Logged in','header chip says "Logged in" for a session',chip);await ctx.close();}
 console.log(`${fails} failed of ${n}`);await br.close();process.exit(fails?1:0)})();
