// WCAG AA text-contrast sweep in light + dark. Checks every visible text node against its effective background.
const {chromium}=require('playwright');const B=process.env.BASE||'http://localhost:8765/';
const SC=[['home','index.html'],['cat','cat.html'],['hub','cat-quant-sets.html'],['set','set.html?sec=qa&set=1'],
 ['set-quiz','set.html?sec=qa&set=1',async p=>{await p.click('#c-start');await p.waitForTimeout(300);await p.click('#c-answer .opt[data-i="1"]');await p.waitForTimeout(300)}],
 ['practice-quiz','cat-practice.html',async p=>{await p.click('#c-start');await p.waitForTimeout(300);await p.locator('#c-answer .opt').first().click();await p.waitForTimeout(300);const s=p.locator('button',{hasText:/^Submit|Check/});if(await s.count())await s.first().click().catch(()=>{});await p.waitForTimeout(300)}],
 ['practice','practice.html'],['quant','quant.html',async p=>{await p.$$eval('details',d=>d.forEach(x=>x.open=true))}],['login','login.html'],['cuet','cuet.html'],['quant-lab','quant-lab.html'],['faq','faq.html'],['after12','after12.html']];
(async()=>{const b=await chromium.launch();let total=0;const out=[];
for(const th of ['light','dark']){for(const [k,u,act] of SC){const c=await b.newContext({viewport:{width:390,height:844}});await c.addInitScript(t=>localStorage.setItem('aptisetu.theme',t),th);const p=await c.newPage();
 await p.goto(B+u);await p.waitForTimeout(500);if(act)try{await act(p)}catch(e){out.push(`${th} ${k}: action failed ${e.message.slice(0,80)}`)}
 const r=await p.evaluate(()=>{const P=s=>{const m=s.match(/[\d.]+/g);if(!m)return null;let v=m.map(Number);if(/^color\(srgb/.test(s)){const a=s.includes('/')?v[3]:1;v=[v[0]*255,v[1]*255,v[2]*255,a]}return v};
  const L=([r,g,b])=>{const f=v=>(v/=255)<=.03928?v/12.92:((v+.055)/1.055)**2.4;return .2126*f(r)+.7152*f(g)+.0722*f(b)};
  const blend=(fg,bg)=>{const a=fg[3]??1;return [0,1,2].map(i=>fg[i]*a+bg[i]*(1-a))};
  const bgOf=el=>{const stack=[];for(let e=el;e;e=e.parentElement){const s=getComputedStyle(e);if(s.backgroundImage!=='none'&&/gradient|url/.test(s.backgroundImage))return {img:true};const c=P(s.backgroundColor);if(c&&(c[3]??1)>0){stack.push(c);if((c[3]??1)>=1)break}}
   let bg=[255,255,255];for(let i=stack.length-1;i>=0;i--)bg=blend(stack[i],bg);return {bg}};
  const res=[];const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;
  while(n=w.nextNode()){const t=n.textContent.trim();if(!t||!/[A-Za-z0-9]/.test(t))continue;const el=n.parentElement;const r=el.getBoundingClientRect();if(!r.width||!el.checkVisibility({opacityProperty:true,visibilityProperty:true}))continue;
   if(el.closest('.skip-link,svg,canvas,[aria-hidden="true"]'))continue;const s=getComputedStyle(el);const b=bgOf(el);if(b.img)continue;
   const fg=blend(P(s.color),b.bg);const l1=L(fg),l2=L(b.bg);const cr=(Math.max(l1,l2)+.05)/(Math.min(l1,l2)+.05);
   const fs=parseFloat(s.fontSize),big=fs>=24||(fs>=18.66&&+s.fontWeight>=700);const need=big?3:4.5;
   if(cr<need&&!el.closest('[disabled],.disabled'))res.push(`${cr.toFixed(2)}<${need} "${t.slice(0,28)}" ${el.tagName.toLowerCase()}.${(el.className+'').slice(0,30)} fg=${s.color} bg=rgb(${b.bg.map(Math.round)})`)}
  return [...new Set(res)]});
 total+=r.length;r.forEach(x=>out.push(`${th} ${k}: ${x}`));await c.close()}}
console.log(out.join('\n'));console.log(`${total} contrast failures`);await b.close();process.exit(total?1:0)})();
