// UI/UX regression checks: theme toggle, no flash, focus ring, skip link, heading order, horizontal overflow, console errors.
const {chromium}=require('playwright');const B=process.env.BASE||'http://localhost:8765/';
const PAGES=['index.html','cat.html','practice.html','cat-practice.html','cat-quant-sets.html','cat-dilr-sets.html','set.html?sec=qa&set=1','quant.html','reasoning.html','varc.html','dilr.html','cuet.html','login.html','quant-lab.html','about.html'];
(async()=>{const b=await chromium.launch();let fails=0,n=0;const ok=(t,c,x='')=>{n++;if(!c)fails++;console.log((c?'PASS ':'FAIL ')+t+(x?' — '+x:''))};
 // 1. Theme toggle: aria-pressed, persists across pages + reload, independent of progress keys
 {const c=await b.newContext({viewport:{width:390,height:844},colorScheme:'light'});const p=await c.newPage();
  await p.goto(B+'index.html');const btn=p.locator('.theme-btn');
  ok('toggle exists with aria-label + aria-pressed=false',await btn.count()==1&&!!(await btn.getAttribute('aria-label'))&&await btn.getAttribute('aria-pressed')=='false');
  const box=await btn.boundingBox();ok('toggle is >=44px',box.width>=44&&box.height>=44,`${box.width}x${box.height}`);
  await btn.click();ok('click → dark, aria-pressed=true',await p.getAttribute('html','data-theme')=='dark'&&await btn.getAttribute('aria-pressed')=='true');
  ok('stored as UI pref only',await p.evaluate(()=>localStorage.getItem('aptisetu.theme'))=='dark');
  await p.goto(B+'cat-quant-sets.html');ok('persists to another page',await p.getAttribute('html','data-theme')=='dark'&&await p.locator('.theme-btn').getAttribute('aria-pressed')=='true');
  await p.reload();ok('persists after reload',await p.getAttribute('html','data-theme')=='dark');
  await p.locator('.theme-btn').click();ok('toggle back → light',await p.getAttribute('html','data-theme')=='light'&&await p.evaluate(()=>localStorage.getItem('aptisetu.theme'))=='light');
  await c.close();}
 // 2. Default follows device; no flash (theme set before first paint, before body exists)
 for(const cs of ['dark','light']){const c=await b.newContext({colorScheme:cs});const p=await c.newPage();
  await p.addInitScript(()=>{new MutationObserver((m,o)=>{if(document.body){window.__t0=document.documentElement.getAttribute('data-theme');o.disconnect()}}).observe(document,{childList:true,subtree:true})});
  await p.goto(B+'index.html');const t0=await p.evaluate(()=>window.__t0);
  ok(`device ${cs}: theme set before <body> parsed (no flash)`,t0==cs,`at body: ${t0}`);
  const bg=await p.evaluate(()=>getComputedStyle(document.body).backgroundColor);ok(`device ${cs}: body bg ${bg}`,cs=='dark'?bg=='rgb(11, 18, 32)':bg!='rgb(11, 18, 32)');await c.close();}
 // 3. Skip link + focus ring
 for(const th of ['light','dark']){const c=await b.newContext({viewport:{width:1440,height:900}});await c.addInitScript(t=>localStorage.setItem('aptisetu.theme',t),th);const p=await c.newPage();
  await p.goto(B+'index.html');await p.keyboard.press('Tab');
  const sk=await p.evaluate(()=>{const a=document.activeElement,r=a.getBoundingClientRect();return {cls:a.className,top:r.top,txt:a.textContent}});
  ok(`${th}: first Tab focuses visible skip link`,sk.cls=='skip-link'&&sk.top>=0,JSON.stringify(sk));
  await p.keyboard.press('Enter');ok(`${th}: skip link moves focus to main`,await p.evaluate(()=>document.activeElement.id)=='main');
  await p.keyboard.press('Tab');const f=await p.evaluate(()=>{const s=getComputedStyle(document.activeElement);return {w:s.outlineWidth,st:s.outlineStyle,o:s.outlineOffset,c:s.outlineColor,tag:document.activeElement.textContent.trim().slice(0,30)}});
  ok(`${th}: focus ring 3px solid with offset`,f.w=='3px'&&f.st=='solid'&&parseFloat(f.o)>=2,JSON.stringify(f));await c.close();}
 // 4. Overflow + heading order + console errors, every page, 6 widths, both themes
 for(const th of ['light','dark']){const c=await b.newContext();await c.addInitScript(t=>localStorage.setItem('aptisetu.theme',t),th);const p=await c.newPage();let errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error'&&!/fonts|supabase|net::|Failed to load resource/i.test(m.text()))errs.push(m.text())});
  const bad=[],hd=[];
  for(const pg of PAGES){for(const W of [360,390,430,768,1024,1440]){await p.setViewportSize({width:W,height:900});await p.goto(B+pg);await p.waitForTimeout(150);
    const o=await p.evaluate(()=>document.documentElement.scrollWidth-innerWidth);if(o>0)bad.push(`${pg}@${W}:+${o}`);}
   const hs=await p.$$eval('h1,h2,h3,h4,h5,h6',a=>a.filter(e=>e.offsetParent!==null||e.closest('details')).map(e=>+e.tagName[1]));let prev=0,skip=null,h1=hs.filter(x=>x==1).length;for(const h of hs){if(h>prev+1&&!skip)skip=`h${prev}→h${h}`;prev=h}
   if(skip||h1!=1)hd.push(`${pg}: ${skip||''} h1×${h1}`);}
  ok(`${th}: no horizontal overflow (${PAGES.length} pages × 6 widths)`,!bad.length,bad.join(' '));
  ok(`${th}: one h1 and no skipped heading levels`,!hd.length,hd.join(' | '));
  ok(`${th}: no JS errors`,!errs.length,errs.slice(0,3).join(' | '));await c.close();}
 console.log(`${fails} failed of ${n}`);await b.close();process.exit(fails?1:0)})();
