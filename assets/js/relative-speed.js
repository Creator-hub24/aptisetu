/* Relative Speed interactive explainer (AptiSetu / @edumaths360) */
/* ---------- Scene engine ---------- */
const cv=document.getElementById('cv'),ctx=cv.getContext('2d');
const W=720,H=400,L=96;
const NAVY='#0B1F3A',GOLD='#C9A227',BLUE='#5BC0EB',MUTE='#9FB3CC',WHITE='#fff';
function fitCanvas(){const d=Math.min(window.devicePixelRatio||1,2);cv.width=W*d;cv.height=H*d;ctx.setTransform(d,0,0,d,0,0);}
fitCanvas();

const S={vA:40,vB:60,dir:'opp',gap0:300,t:0,playing:false,stopAt:null,rate:0.5,view:'ground',trails:true,msg:'',onStop:null,finAt:0,px:1,cam0:0,tick:50};
const rel=()=>S.dir==='opp'?S.vA+S.vB:S.vB-S.vA;
const posA=t=>S.vA*t;
const posB=t=>S.dir==='opp'?S.gap0-S.vB*t:-S.gap0+S.vB*t;
const gapAt=t=>S.dir==='opp'?posB(t)-posA(t):posA(t)-posB(t);
const tEnd=()=>rel()>0?S.gap0/rel():Infinity;
function tLimit(){const r=rel();if(r>0)return S.gap0/r;if(r<0)return S.gap0/(-r);return 3;}
const fmt=n=>{const v=Math.round(n*10)/10;return (Math.abs(v)<0.05?0:v).toString();};
const fmtT=t=>(Math.round(t*100)/100).toString();
function niceStep(v){const p=Math.pow(10,Math.floor(Math.log10(Math.max(v,1e-6))));const m=v/p;return (m<1.5?1:m<3.5?2:m<7.5?5:10)*p;}

function setup(o){
  Object.assign(S,o);S.t=0;S.playing=false;S.msg='';S.onStop=null;S.stopAt=null;S.finAt=0;
  const T=tLimit();const xs=[posA(0),posA(T),posB(0),posB(T)];
  const mn=Math.min(...xs),mx=Math.max(...xs);
  S.px=(W-240)/Math.max(mx-mn,1);S.cam0=(mn+mx)/2;S.tick=niceStep((mx-mn)/30);
}
function play(stopAt,cb){
  if(S.t>=tLimit()-1e-6){S.t=0;}
  S.stopAt=(stopAt==null)?null:stopAt;S.onStop=cb||null;
  let r=tLimit()/6;if(S.stopAt!=null&&S.stopAt-S.t<=1.01)r=Math.min(r,0.5);
  S.rate=r;S.msg='';S.finAt=0;S.playing=true;
}
function resetScene(){S.t=0;S.playing=false;S.msg='';S.finAt=0;S.onStop=null;}
function finish(){
  const r=rel(),lim=tLimit();
  if(r>0&&S.t>=lim-1e-6){S.msg=(S.dir==='opp'?'Mil gayi! ':'Pakad liya! ')+fmtT(S.t)+' ghante mein';S.finAt=performance.now();}
  else if(r<0&&S.t>=lim-1e-6){S.msg='Gap badhta ja raha hai…';}
  else if(r===0&&S.t>=lim-1e-6){S.msg='Gap bilkul nahi badla!';}
  const cb=S.onStop;S.onStop=null;if(cb)cb();
}

function rr(x,y,w,h,r){ctx.beginPath();ctx.moveTo(x+r,y);ctx.arcTo(x+w,y,x+w,y+h,r);ctx.arcTo(x+w,y+h,x,y+h,r);ctx.arcTo(x,y+h,x,y,r);ctx.arcTo(x,y,x+w,y,r);ctx.closePath();}
function text(s,x,y,size,color,align='center',weight=600){ctx.font=`${weight} ${size}px Poppins, system-ui, sans-serif`;ctx.fillStyle=color;ctx.textAlign=align;ctx.textBaseline='alphabetic';ctx.fillText(s,x,y);}
function arrow(x,y,len,dir,col){if(len<6)return;const x2=x+dir*len;ctx.strokeStyle=col;ctx.fillStyle=col;ctx.lineWidth=4;ctx.lineCap='round';
  ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x2-dir*8,y);ctx.stroke();ctx.beginPath();ctx.moveTo(x2,y);ctx.lineTo(x2-dir*12,y-7);ctx.lineTo(x2-dir*12,y+7);ctx.closePath();ctx.fill();}
function train(left,col,letter,faceRight,alpha=1){
  ctx.save();ctx.globalAlpha=alpha;const y=184,h=44;
  ctx.fillStyle=col;rr(left,y,L,h,12);ctx.fill();
  ctx.fillStyle='rgba(11,31,58,.85)';for(let i=0;i<3;i++){rr(left+12+i*26,y+8,18,15,4);ctx.fill();}
  ctx.fillStyle='rgba(11,31,58,.3)';ctx.fillRect(left,y+29,L,4);
  text(letter,faceRight?left+L-14:left+14,y+24,15,NAVY,'center',700);
  if(alpha>0.5){ctx.save();ctx.fillStyle='#FFF3B0';ctx.shadowColor='#FFF3B0';ctx.shadowBlur=12;ctx.beginPath();ctx.arc(faceRight?left+L-5:left+5,y+36,4,0,7);ctx.fill();ctx.restore();}
  [18,40,L-40,L-18].forEach(o=>{ctx.fillStyle='#0A1A30';ctx.beginPath();ctx.arc(left+o,y+h+3,7,0,7);ctx.fill();ctx.strokeStyle=MUTE;ctx.lineWidth=2;ctx.stroke();});
  ctx.restore();
}
function tree(x){ctx.fillStyle='#16304f';ctx.fillRect(x-2,214,4,22);ctx.beginPath();ctx.moveTo(x,170);ctx.lineTo(x-14,220);ctx.lineTo(x+14,220);ctx.closePath();ctx.fill();}

function draw(){
  const opp=S.dir==='opp',px=S.px,cam=S.view==='A'?S.cam0+posA(S.t):S.cam0;
  const X=x=>W/2+(x-cam)*px;
  const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#11294b');g.addColorStop(1,NAVY);ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
  ctx.fillStyle='#08182d';ctx.fillRect(0,240,W,H-240);
  // trees + sleepers fixed to the ground (world)
  const wl=cam-W/2/px,wr=cam+W/2/px;
  const tStep=S.tick*4;
  for(let k=Math.floor(wl/tStep)-1;k<=Math.ceil(wr/tStep)+1;k++)tree(X(k*tStep+tStep/2));
  ctx.fillStyle='#2B4468';ctx.fillRect(0,234,W,4);ctx.fillRect(0,240,W,2);
  ctx.fillStyle='#1d3557';
  for(let k=Math.floor(wl/S.tick)-1;k<=Math.ceil(wr/S.tick)+1;k++){ctx.fillRect(X(k*S.tick)-3,242,6,8);}
  const a=posA(S.t),b=posB(S.t);
  const aLeft=opp?X(a)-L:X(a),bLeft=opp?X(b):X(b)-L;
  // ghosts of start positions
  if(S.t>0&&S.view==='ground'){train(opp?X(posA(0))-L:X(posA(0)),BLUE,'A',true,.16);train(opp?X(posB(0)):X(posB(0))-L,GOLD,'B',!opp,.16);}
  train(aLeft,BLUE,'A',true);train(bLeft,GOLD,'B',!opp);
  // speed tags
  const clampX=x=>Math.max(90,Math.min(W-90,x));
  if(S.view==='ground'){
    const ax=clampX(aLeft+L/2),bx=clampX(bLeft+L/2);
    text(`A · ${S.vA} km/h`,ax,108,24,BLUE,'center',700);arrow(ax-Math.min(S.vA,120)*0.45,130,Math.min(S.vA,120)*0.9,1,BLUE);
    text(`B · ${S.vB} km/h`,bx,108,24,GOLD,'center',700);const bd=opp?-1:1;arrow(bx-bd*Math.min(S.vB,120)*0.45,132,Math.min(S.vB,120)*0.9,bd,GOLD);
  }else{
    const ax=clampX(aLeft+L/2),bx=clampX(bLeft+L/2);
    const rv=opp?-(S.vA+S.vB):S.vB-S.vA;
    text('A · ruki (tum)',ax,108,22,BLUE,'center',700);
    text(`B · ${Math.abs(rv)} km/h`,bx,108,24,GOLD,'center',700);
    const L2=Math.min(Math.abs(rv),150)*0.9;arrow(bx-Math.sign(rv)*L2/2,132,L2,Math.sign(rv)||1,GOLD);
    text(`Ped ← ${S.vA} km/h se peeche bhaagte dikhte hain`,16,300,20,MUTE,'left',600);
  }
  // gap bracket
  const n1=X(a),n2=X(b),lo=Math.min(n1,n2),hi=Math.max(n1,n2),gp=gapAt(S.t);
  if(hi-lo>3){ctx.strokeStyle=WHITE;ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(lo,160);ctx.lineTo(lo,174);ctx.moveTo(lo,167);ctx.lineTo(hi,167);ctx.moveTo(hi,160);ctx.lineTo(hi,174);ctx.stroke();
    if(hi-lo>90)text(`${fmt(Math.abs(gp))} km`,(lo+hi)/2,155,20,WHITE,'center',700);}
  // trails: how far each train went
  if(S.trails&&S.t>0&&S.view==='ground'){
    const bars=[[posA(0),a,BLUE,`A ne ${fmt(S.vA*S.t)} km`,260],[posB(0),b,GOLD,`B ne ${fmt(S.vB*S.t)} km`,294]];
    bars.forEach(([s,e,c,lab,y])=>{const x1=Math.min(X(s),X(e)),x2=Math.max(X(s),X(e)),w=x2-x1;if(w<1)return;
      ctx.fillStyle=c;rr(x1,y,w,26,8);ctx.fill();
      if(w>150)text(lab,x1+w/2,y+20,19,NAVY,'center',700);
      else text(lab,x2+6>W-150?x1-6:x2+6,y+20,19,c,x2+6>W-150?'right':'left',700);});
  }
  // HUD
  text(`t = ${fmtT(S.t)} ghanta`,16,36,26,WHITE,'left',700);
  text(`Gap = ${fmt(Math.abs(gp))} km`,W-16,36,26,WHITE,'right',700);
  if(S.view==='A'){ctx.fillStyle='rgba(201,162,39,.18)';rr(W/2-100,52,200,34,17);ctx.fill();text('👁 A ki nazar se',W/2,76,19,GOLD,'center',700);}
  // meeting flash
  if(S.finAt){const f=(performance.now()-S.finAt)/900;if(f<1){ctx.strokeStyle=GOLD;ctx.globalAlpha=1-f;ctx.lineWidth=6*(1-f)+1;ctx.beginPath();ctx.arc(n1,206,24+f*90,0,7);ctx.stroke();ctx.globalAlpha=1;}}
  if(S.msg){text(S.msg,W/2,372,34,GOLD,'center',700);}
}
let last=performance.now();
function loop(now){const dt=Math.min((now-last)/1000,0.05);last=now;
  if(S.playing){S.t+=dt*S.rate;const lim=S.stopAt!=null?Math.min(S.stopAt,tLimit()):tLimit();
    if(S.t>=lim){S.t=lim;S.playing=false;finish();}}
  draw();requestAnimationFrame(loop);}
requestAnimationFrame(loop);

/* ---------- Steps (script) ---------- */
const panel=document.getElementById('panel');
const $=s=>panel.querySelector(s);
function predict(box,opts,correct,feedback,onAnswer){
  box.innerHTML=opts.map((o,i)=>`<button class="opt" data-i="${i}">${o}</button>`).join('');
  let done=false;
  box.querySelectorAll('.opt').forEach(b=>b.onclick=()=>{if(done)return;done=true;const i=+b.dataset.i;
    b.classList.add(i===correct?'ok':'no');box.children[correct].classList.add('ok');
    box.querySelectorAll('.opt').forEach(x=>x.disabled=true);onAnswer(i===correct,feedback[i]);});
}
function seg(el,items,val,onChange){
  el.innerHTML=items.map(([v,l])=>`<button data-v="${v}" class="${v===val?'on':''}">${l}</button>`).join('');
  el.querySelectorAll('button').forEach(b=>b.onclick=()=>{el.querySelectorAll('button').forEach(x=>x.classList.remove('on'));b.classList.add('on');onChange(b.dataset.v);});
}

const steps=[
/* 1 — hook + definition */
()=>{setup({dir:'opp',vA:40,vB:60,gap0:300,view:'ground',trails:true});
panel.innerHTML=`<span class="tag">Shuruaat</span>
<h2>Do trains, ek sawaal</h2>
<p>Train <span class="blue">A</span> aur train <span class="gold">B</span> 300 km door hain. A 40 km/h se chal rahi hai, B 60 km/h se, aur dono ek dusre ki taraf aa rahi hain.</p>
<p>Kitne ghante mein milengi? Isse pehle ek simple baat samjho:</p>
<div class="def">Relative Speed = do cheezon ke beech ka gap har ghante kitna badalta hai.</div>
<div class="row"><button class="btn" id="go">▶ Trains chalao</button></div>
<div class="reveal" id="rv"><p>Upar dekho: trains <b>3 ghante</b> mein mil gayi. Par 3 hi kyun? Agle step mein ek-ek ghanta tod kar dekhte hain.</p></div>`;
$('#go').onclick=()=>play(null,()=>$('#rv').classList.add('show'));},

/* 2 — predict: opposite */
()=>{setup({dir:'opp',vA:40,vB:60,gap0:300,view:'ground',trails:true});
panel.innerHTML=`<span class="tag">Socho · Aamne-saamne</span>
<h2>1 ghante mein gap kitna kam hoga?</h2>
<p>A 40 km/h, B 60 km/h, ek dusre ki taraf. Gap abhi 300 km hai. Pehle andaaza lagao, phir trains khud chalengi.</p>
<div class="opts" id="o"></div><div class="fb" id="fb"></div>
<div class="reveal" id="rv">
<p>Gap 300 se 200 ho gaya, yaani <b>100 km kam</b>.</p>
<p>Neeche ki pattiyan dekho: <span class="blue">A ne 40 km</span> apni taraf se gap kam kiya, aur <span class="gold">B ne 60 km</span> apni taraf se. Dono ek hi gap ko do taraf se kha rahi hain.</p>
<div class="math">40 + 60 = <b>100 km/h</b></div>
<p>Isliye: <b>aamne-saamne ho to speeds jodo.</b></p>
<div class="row"><button class="btn ghost" id="more">▶ 1 ghanta aur</button></div></div>`;
predict($('#o'),['20 km','60 km','100 km'],2,[
 '20 tab hota jab dono ek hi taraf jaati. Yahan dono gap kam kar rahi hain.',
 '60 sirf B ka hissa hai. A bhi to gap kam kar rahi hai!',
 'Bilkul sahi! ✅'],(ok,m)=>{const f=$('#fb');f.textContent=m;f.className='fb '+(ok?'ok':'no');play(1,()=>$('#rv').classList.add('show'));});
$('#more').onclick=()=>play(S.t>=tLimit()-1e-6?1:S.t+1);},

/* 3 — predict: same direction */
()=>{setup({dir:'same',vA:40,vB:60,gap0:100,view:'ground',trails:true});
panel.innerHTML=`<span class="tag">Socho · Ek hi taraf</span>
<h2>Ab B, A ka peecha kar rahi hai</h2>
<p>A (40 km/h) 100 km aage hai. B (60 km/h) peeche se usi taraf aa rahi hai.</p>
<p>1 ghante mein gap kitna kam hoga?</p>
<div class="opts" id="o"></div><div class="fb" id="fb"></div>
<div class="reveal" id="rv">
<p>Gap 100 se 80 hua, yaani sirf <b>20 km kam</b>.</p>
<p><span class="gold">B 60 km aage badhi</span>, lekin <span class="blue">A bhi 40 km aage nikal gayi</span>. B ko sirf utna fayda hua jitni woh A se tez hai.</p>
<div class="math">60 − 40 = <b>20 km/h</b></div>
<p>Isliye: <b>ek hi taraf ho to speeds ghatao</b> (badi − chhoti).</p>
<div class="row"><button class="btn ghost" id="more">▶ Pakadne tak chalao</button></div></div>`;
predict($('#o'),['100 km','60 km','20 km'],2,[
 '100 tab hota jab A saamne se aati. Yahan A bhi aage bhaag rahi hai.',
 'B 60 km chali, par A bhi to 40 km aage nikal gayi!',
 'Sahi pakde! ✅'],(ok,m)=>{const f=$('#fb');f.textContent=m;f.className='fb '+(ok?'ok':'no');play(1,()=>$('#rv').classList.add('show'));});
$('#more').onclick=()=>play(null);},

/* 4 — frame of reference */
()=>{setup({dir:'opp',vA:40,vB:60,gap0:300,view:'A',trails:true});
panel.innerHTML=`<span class="tag">Naya nazariya</span>
<h2>Train A mein baith kar dekho</h2>
<p>Chalti train mein baitho to lagta hai tum ruke ho aur bahar ke ped peeche bhaag rahe hain.</p>
<p>Camera ab <span class="blue">A</span> par lock hai. A ruki dikhegi, aur <span class="gold">B</span> jis speed se paas aati dikhegi, <b>wahi relative speed hai</b>.</p>
<div class="seg" id="view"></div><div class="seg" id="dir"></div>
<div class="ro" id="ro"></div>
<div class="row"><button class="btn" id="go">▶ Chalao</button><button class="btn ghost" id="rs">↺ Reset</button></div>
<p class="small">Dono views mein trains utne hi ghante mein milti hain. Sirf dekhne ka nazariya badla hai, jawab nahi.</p>`;
const upd=()=>{$('#ro').innerHTML=S.dir==='opp'?'A ki nazar se B <b>40 + 60 = 100 km/h</b> se aati dikhti hai.':'A ki nazar se B sirf <b>60 − 40 = 20 km/h</b> se paas aati dikhti hai.';};
seg($('#view'),[['ground','🌍 Zameen se'],['A','👁 A ki nazar se']],'A',v=>{S.view=v;});
seg($('#dir'),[['opp','⇄ Aamne-saamne'],['same','⇉ Ek hi taraf']],'opp',v=>{setup({dir:v,gap0:v==='opp'?300:100});upd();});
upd();$('#go').onclick=()=>play(null);$('#rs').onclick=resetScene;},

/* 5 — shortcut */
()=>{setup({dir:'opp',vA:40,vB:60,gap0:300,view:'ground',trails:false});
panel.innerHTML=`<span class="tag">Shortcut</span>
<h2>Ab sawaal 10 second mein</h2>
<p>Relative speed batati hai ki gap har ghante kitna kam hota hai. To poora gap khatam hone mein lagega:</p>
<div class="def">Time = Gap ÷ Relative Speed</div>
<div class="mini"><h3>⇄ Aamne-saamne</h3><div class="math">300 ÷ (40 + 60) = <b>3 ghante</b></div><button class="btn ghost" id="c1">▶ Check karo</button></div>
<div class="mini"><h3>⇉ Ek hi taraf</h3><div class="math">100 ÷ (60 − 40) = <b>5 ghante</b></div><button class="btn ghost" id="c2">▶ Check karo</button></div>
<div class="rule"><div><b>+ jodo</b><span>aamne-saamne</span></div><div><b>− ghatao</b><span>ek hi taraf</span></div></div>
<p class="small">Formula ki bhasha mein: relative speed = |v₁ ± v₂|. Plus jab aamne-saamne, minus jab ek hi taraf.</p>`;
$('#c1').onclick=()=>{setup({dir:'opp',gap0:300});play(null);};
$('#c2').onclick=()=>{setup({dir:'same',gap0:100});play(null);};},

/* 6 — playground */
()=>{setup({dir:'opp',vA:40,vB:60,gap0:300,view:'ground',trails:true});
panel.innerHTML=`<span class="tag">Khud try karo</span>
<h2>Playground</h2>
<div class="seg" id="dir"></div><div class="seg" id="view"></div>
<label class="sl"><span class="blue">A ki speed</span><span id="lA"></span></label><input type="range" id="sA" min="0" max="120" step="5">
<label class="sl"><span class="gold">B ki speed</span><span id="lB"></span></label><input type="range" id="sB" min="0" max="120" step="5">
<label class="sl"><span>Shuru ka gap</span><span id="lG"></span></label><input type="range" id="sG" min="50" max="500" step="10">
<div class="ro" id="ro"></div>
<div class="row"><button class="btn" id="go">▶ Chalao</button><button class="btn ghost" id="rs">↺ Reset</button></div>
<div class="mini"><h3>🎯 Challenge</h3><p class="small" style="margin:0">Gap 300 km rakho, trains aamne-saamne. Aisi speeds set karo ki woh theek <b>2 ghante</b> mein milein.</p><div class="fb ok" id="ch"></div></div>`;
const sA=$('#sA'),sB=$('#sB'),sG=$('#sG');sA.value=S.vA;sB.value=S.vB;sG.value=S.gap0;
const upd=()=>{
  $('#lA').textContent=S.vA+' km/h';$('#lB').textContent=S.vB+' km/h';$('#lG').textContent=S.gap0+' km';
  const r=rel(),opp=S.dir==='opp';
  let h=opp?`Relative speed = ${S.vA} + ${S.vB} = <b>${r} km/h</b>`:`Relative speed = ${S.vB} − ${S.vA} = <b>${r} km/h</b>`;
  if(r>0)h+=`<br>Time = ${S.gap0} ÷ ${r} = <b>${fmtT(S.gap0/r)} ghante</b>`;
  else if(r<0)h+=`<br>Aage wali A tez hai, gap har ghante <b>${-r} km badhega</b>. B kabhi nahi pakdegi.`;
  else h+=opp?'<br>Dono ruki hain, gap nahi badlega.':'<br>Speeds barabar hain, <b>gap kabhi nahi badlega</b>.';
  if(!opp)h+='<br><span class="small">(B peeche hai, A aage)</span>';
  $('#ro').innerHTML=h;};
const re=()=>{setup({vA:+sA.value,vB:+sB.value,gap0:+sG.value});$('#ch').textContent='';upd();};
[sA,sB,sG].forEach(s=>s.oninput=re);
seg($('#dir'),[['opp','⇄ Aamne-saamne'],['same','⇉ Ek hi taraf']],'opp',v=>{S.dir=v;re();});
seg($('#view'),[['ground','🌍 Zameen se'],['A','👁 A ki nazar se']],'ground',v=>{S.view=v;});
upd();
$('#go').onclick=()=>play(null,()=>{if(S.dir==='opp'&&S.gap0===300&&rel()>0&&Math.abs(S.t-2)<1e-6)$('#ch').textContent='Challenge poora! 🎉 '+S.vA+' + '+S.vB+' = 150, aur 300 ÷ 150 = 2.';});
$('#rs').onclick=resetScene;},

/* 7 — quiz with visual check */
()=>{setup({dir:'opp',vA:30,vB:50,gap0:160,view:'ground',trails:true});
const Q=[
 {q:'Do cars 30 km/h aur 50 km/h se ek dusre ki taraf aa rahi hain. Relative speed?',o:['20 km/h','80 km/h','50 km/h'],c:1,e:'Aamne-saamne, to jodo: 30 + 50 = 80 km/h.',s:{dir:'opp',vA:30,vB:50,gap0:160}},
 {q:'Bus (A) 50 km/h se aage hai, peeche car (B) 70 km/h se usi taraf. Car kitni tezi se bus ke paas aa rahi hai?',o:['120 km/h','20 km/h','70 km/h'],c:1,e:'Ek hi taraf, to ghatao: 70 − 50 = 20 km/h.',s:{dir:'same',vA:50,vB:70,gap0:40}},
 {q:'Do trains 240 km door hain, 50 aur 70 km/h se aamne-saamne. Kitne ghante mein milengi?',o:['2 ghante','12 ghante','4.8 ghante'],c:0,e:'Time = 240 ÷ (50 + 70) = 240 ÷ 120 = 2 ghante.',s:{dir:'opp',vA:50,vB:70,gap0:240}},
 {q:'A 60 km/h se aage hai, B 45 km/h se peeche, same direction. Gap ka kya hoga?',o:['Ghatega','Badhega','Same rahega'],c:1,e:'Aage wali tez hai, to gap har ghante 60 − 45 = 15 km badhega. B kabhi nahi pakdegi.',s:{dir:'same',vA:60,vB:45,gap0:60}}];
let score=0,answered=0;
panel.innerHTML=`<span class="tag">Quiz</span><h2>Jawab do, phir upar dekho</h2><p class="small">Har jawab ke baad trains wahi situation chala kar dikhayengi.</p>`+
 Q.map((x,i)=>`<div class="q"><p class="qt">${i+1}. ${x.q}</p><div class="opts" id="q${i}"></div><div class="fb" id="f${i}"></div></div>`).join('')+
 `<div class="reveal" id="end"><div class="score" id="sc"></div><div class="def">Ek line yaad rakho: relative speed = gap kitni tezi se badalta hai. Aamne-saamne jodo, ek hi taraf ghatao.</div></div>`;
Q.forEach((x,i)=>predict($('#q'+i),x.o,x.c,x.o.map((_,j)=>j===x.c?'Sahi! ✅ '+x.e:'Galat. '+x.e),(ok,m)=>{
  const f=$('#f'+i);f.textContent=m;f.className='fb '+(ok?'ok':'no');if(ok)score++;answered++;
  setup(Object.assign({view:'ground',trails:true},x.s));play(null);
  if(answered===Q.length){$('#sc').textContent=`Score: ${score} / ${Q.length} ${score===Q.length?'🏆':''}`;$('#end').classList.add('show');}}));}
];

/* ---------- Navigation ---------- */
let cur=0;
function go(i){cur=(i+steps.length)%steps.length;steps[cur]();
  document.getElementById('prog').style.width=((cur+1)/steps.length*100)+'%';
  document.getElementById('count').textContent=`${cur+1} / ${steps.length}`;
  document.getElementById('prev').disabled=cur===0;
  document.getElementById('next').textContent=cur===steps.length-1?'Shuru se ↺':'Aage ▶';
  window.scrollTo({top:0,behavior:'smooth'});}
document.getElementById('prev').onclick=()=>go(cur-1);
document.getElementById('next').onclick=()=>go(cur+1);
go(0);
