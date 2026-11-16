
(function(){
var $=function(id){return document.getElementById(id);};
// ================= palms and Joshua trees seen from above, with all kinds of birds =================
var cv=$('forest'),ctx=cv.getContext('2d'),W,H,t=0,root=document.documentElement;
var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
function rnd(a,b){return a+Math.random()*(b-a);}
function wrap(a){while(a>Math.PI)a-=6.283;while(a<-Math.PI)a+=6.283;return a;}

// quiet colours, one set per theme
// each kind of tree is three greens (shade, mid, sunlit); jacarandas add a little lilac
var PALS={light:{kinds:[['#a3c39c','#b7d2ae','#cde0c2'],['#b3bf96','#c6d0a9','#d9e0c0'],['#a5c4b8','#bad5ca','#cfe2d9'],['#9cbd9f','#b0cdb0','#c6dcc3']],blooms:[['#e3d08a','#eddd9f','#f5e9bb'],['#e6b5bf','#efc8d0','#f7dce1']],wood:'#b9a78c',shade:'rgba(50,70,55,.13)',edge:'rgba(47,86,92,.28)'},
          dark:{kinds:[['#1c3a2f','#23483a','#2b5744'],['#2b3926','#35462d','#405436'],['#1e3a39','#264847','#2f5655'],['#1a3a33','#21483f','#29564b']],blooms:[['#4a4222','#5a502a','#6b6034'],['#4d2f3a','#5e3a47','#704655']],wood:'#3a3329',shade:'rgba(0,0,0,.32)',edge:'rgba(0,0,0,0)'}},P=PALS.light,DARK=false;
function readVars(){DARK=getComputedStyle(root).getPropertyValue('--flow').trim().indexOf('170')===0;P=DARK?PALS.dark:PALS.light;if(typeof trees!=='undefined')trees.forEach(buildTree);}
new MutationObserver(readVars).observe(root,{attributes:true,attributeFilter:['data-theme']});
matchMedia('(prefers-color-scheme: dark)').addEventListener('change',readVars);

// ---- San Diego time: night means sleep
var fmt=new Intl.DateTimeFormat('en-US',{timeZone:'America/Los_Angeles',hour:'numeric',minute:'2-digit',hourCycle:'h23'});
function nowH(){var p={};fmt.formatToParts(new Date()).forEach(function(x){p[x.type]=x.value;});return (+p.hour%24)+(+p.minute)/60;}
function label(h){var Hh=Math.floor(h)%24,M=Math.round((h-Math.floor(h))*60);if(M===60){M=0;Hh=(Hh+1)%24;}return (Hh%12||12)+':'+String(M).padStart(2,'0')+' '+(Hh<12?'am':'pm');}
var hour=12,preview=null,cap=$('cap'),slider=$('when'),reset=$('now');
function isNight(){return vzNight(hour);}
function clock(){hour=preview==null?nowH():preview;cap.textContent=(preview==null?'San Diego, ':'Preview, ')+label(hour)+(isNight()?', asleep':'');slider.value=hour;reset.hidden=preview==null;vzApplyTheme(hour);}
slider.oninput=function(){preview=+slider.value;clock();};reset.onclick=function(){preview=null;clock();};setInterval(clock,30000);

// ---- trees down both margins, seen from above; the middle stays open for reading.
// A canopy is an uneven outline filled with many small leaf dabs, lit from the upper left, with branches showing in the gaps.
var BLOOMS=['none','specks','full'],bloomMode='full';

var trees=[];
function seeded(s){return function(){s=(s*16807)%2147483647;return s/2147483647;};}
function buildTree(tr){var R=seeded(tr.seed),r=tr.r,d=Math.min(devicePixelRatio||1,2),pad=r*.3+8,size=(r+pad)*2;
  var c=tr.cv||(tr.cv=document.createElement('canvas'));c.width=c.height=Math.ceil(size*d);tr.size=size;
  var x=c.getContext('2d');x.setTransform(d,0,0,d,0,0);x.translate(size/2,size/2);
  var p1=R()*6.283,p2=R()*6.283,p3=R()*6.283,a1=.1+R()*.12,pal=(tr.bloom&&bloomMode==='full')?P.blooms[tr.bk]:P.kinds[tr.kind%P.kinds.length];
  function rad(th){return r*(.78+a1*Math.sin(th*2+p1)+.09*Math.sin(th*3+p2)+.06*Math.sin(th*5+p3));}
  function outline(k){x.beginPath();for(var i=0;i<=48;i++){var th=i/48*6.283,q=rad(th)*k;x[i?'lineTo':'moveTo'](Math.cos(th)*q,Math.sin(th)*q);}x.closePath();}
  x.save();x.translate(r*.06,r*.09);x.fillStyle=P.shade;outline(1.04);x.fill();x.restore();
  x.fillStyle=pal[0];outline(.9);x.fill();
  x.strokeStyle=P.wood;x.lineCap='round';x.globalAlpha=.75;var nb=5+(R()*3|0),b0=R()*6.283;
  for(var i=0;i<nb;i++){var th=b0+i/nb*6.283+(R()-.5)*.5,L=rad(th)*.74,mx=Math.cos(th+.25)*L*.5,my=Math.sin(th+.25)*L*.5;x.lineWidth=Math.max(1.2,r*.035);x.beginPath();x.moveTo(0,0);x.quadraticCurveTo(mx,my,Math.cos(th)*L,Math.sin(th)*L);x.stroke();
    var f=th+(R()<.5?.7:-.7);x.lineWidth=Math.max(1,r*.02);x.beginPath();x.moveTo(mx,my);x.lineTo(mx+Math.cos(f)*L*.4,my+Math.sin(f)*L*.4);x.stroke();}
  x.globalAlpha=1;
  var n=Math.round(40+r*.75),dabs=[];
  for(i=0;i<n;i++){var t2=R()*6.283,q=Math.pow(R(),.6)*rad(t2)*.98,dx=Math.cos(t2)*q,dy=Math.sin(t2)*q,light=(-dx*.6-dy*.8)/r+(R()-.5)*.7;
    dabs.push({x:dx,y:dy,a:r*(.1+R()*.085),b:.5+R()*.3,rot:R()*3.14,c:light>.22?2:light<-.25?0:1});}
  dabs.sort(function(m,k){return m.c-k.c;});
  dabs.forEach(function(q){x.fillStyle=pal[q.c];x.beginPath();x.ellipse(q.x,q.y,q.a,q.a*q.b,q.rot,0,6.283);x.fill();});
  if(tr.bloom&&bloomMode==='specks'){x.fillStyle=P.blooms[tr.bk][DARK?2:0];x.beginPath();var ns=Math.round(r*1.1);for(i=0;i<ns;i++){var t3=R()*6.283,q3=Math.sqrt(R())*rad(t3)*.92,sx=Math.cos(t3)*q3-r*.06,sy=Math.sin(t3)*q3-r*.08,sr=1+R()*1.2;x.moveTo(sx+sr,sy);x.arc(sx,sy,sr,0,6.283);}x.fill();}}
(function(){var el=document.getElementById('pick');if(!el)return;
  function paint(){el.innerHTML='Blossom: '+BLOOMS.map(function(n){return '<button data-s="'+n+'"'+(n===bloomMode?' class="on"':'')+'>'+n+'</button>';}).join('');}
  el.addEventListener('click',function(e){var n=e.target.getAttribute&&e.target.getAttribute('data-s');if(!n)return;bloomMode=n;try{localStorage.setItem('vz-bloom',n);}catch(x){}trees.forEach(buildTree);paint();if(reduce)frame();});paint();})();
function makeTrees(){trees=[];var R=seeded(11),lane=(W-760)/2,wide=lane>120,id=0;
  function tree(x,y,r){var t0={x:x,y:y,r:r,seed:1000+(id++)*7919,kind:(R()*4)|0,bloom:R()<.26,bk:id%2};trees.push(t0);}
  if(wide){var n=Math.ceil(H/190)+1,maxR=Math.min(112,lane*.5);
    for(var side=0;side<2;side++)for(var i=0;i<n;i++){var r=maxR*(.6+R()*.4),inset=R()*Math.max(0,lane-r*1.9),x=side?W-r*.55-inset:r*.55+inset;tree(x,(i+.2+R()*.6)/n*H*1.06-20,r);}
    if(lane>330)for(side=0;side<2;side++)for(i=0;i<3;i++){r=34+R()*26;tree(side?W-lane+70+R()*50:lane-70-R()*50,(i+.5+R()*.4)/3*H,r);}
  }else{tree(0,H*.16,84);tree(W,H*.36,78);tree(-4,H*.62,90);tree(W+4,H*.86,84);}
  trees.sort(function(a,b){return b.r-a.r;});
  trees.forEach(function(tr){tr.spots=[[0,0],[tr.r*.32,tr.r*.1],[-tr.r*.25,tr.r*.28],[tr.r*.05,-tr.r*.34],[-tr.r*.3,-tr.r*.15]];tr.px=tr.x;tr.py=tr.y;tr.pr=tr.r*.5;if(!wide){tr.px=tr.x<W/2?15:W-15;tr.pr=10;tr.spots=[[0,0],[-3,-tr.r*.3],[3,-tr.r*.13],[-2,tr.r*.14],[2,tr.r*.3]].map(function(s){return [tr.px-tr.x+s[0],s[1]];});}buildTree(tr);});}
function drawTrees(){trees.forEach(function(tr){ctx.drawImage(tr.cv,tr.x-tr.size/2,tr.y-tr.size/2,tr.size,tr.size);});}

// ---- birds from above, in the pond style: an oval, a round head, a small beak. Muted so they sit quietly.
var KIND={
  gray: {s:1.3, body:'#a6abb0',wing:'#8d9399',head:'#b3b4a8',beak:'#8f9499',cheek:'#e8935c',crest:'#7c838a',bar:'#eeece6',label:'Ashe',tail:22,span:25,flap:15},
  pearl:{s:1.3, body:'#f7f4ec',wing:'#e3dfd3',head:'#f0e2a4',beak:'#cfc5b4',crest:'#e2c96c',fold:'#f1ecdd',pearl:'#ead88f',outline:true,label:'Pearl',tail:22,span:25,flap:15},
  keet: {s:.85,body:'#8fbd84',wing:'#6f9c6b',head:'#ecd98a',beak:'#cfa25a',stripe:'#4f5f47',label:'Kiwi',tail:18,span:22,flap:18}};
var birds=[],mouse={x:-9999,y:-9999};
function spot(tr){var s=tr.spots[(Math.random()*tr.spots.length)|0];return {x:tr.x+s[0]+rnd(-5,5),y:tr.y+s[1]+rnd(-5,5),tr:tr};}
function visibleTrees(){var v=trees.filter(function(tr){return tr.r>50&&tr.px>10&&tr.px<W-10&&tr.y>40&&tr.y<H-40;});return v.length?v:trees;}
function makeBirds(){birds=[];var kinds=['gray','pearl','keet'],vis=visibleTrees();
  kinds.forEach(function(k,i){var sp=spot(vis[i%vis.length]);birds.push({k:k,x:sp.x,y:sp.y,a:rnd(0,6.28),v:0,home:sp,fly:false,wait:rnd(6,40),ph:rnd(0,6),tuck:0,alt:0,look:rnd(0,6.28),mate:null,delay:-1,hops:0,lift:0,hop:null});});
  }
function go(b,target,fast){b.hop=null;b.hops=0;b.lift=0;b.home=target;b.fly=true;b.fast=fast;b.tuck=0;}
function pick(b,scared){var vis=visibleTrees(),night=isNight();
  if(night){var rt=vis.slice().sort(function(p,q){return Math.abs(p.y-H*.38)+Math.abs(p.x-W*.84)*.3-(Math.abs(q.y-H*.38)+Math.abs(q.x-W*.84)*.3);})[0],k=birds.indexOf(b)-(birds.length-1)/2;return {x:(rt.px===rt.x?rt.x+k*15:(rt.px<W/2?34:W-34)+k*13),y:rt.py+Math.abs(k)*3,tr:rt,night:true};}
  var side=b.x<W/2,c=vis.filter(function(tr){return tr!==b.home.tr&&((tr.x<W/2)===side)===(Math.random()<(scared?.5:.8));});
  if(!c.length)c=vis.filter(function(tr){return tr!==b.home.tr;});if(!c.length)c=vis;
  return spot(c[(Math.random()*c.length)|0]);}
function step(){t+=1/60;var night=isNight();
  birds.forEach(function(b){
    if(b.fly){var dx=b.home.x-b.x,dy=b.home.y-b.y,dist=Math.hypot(dx,dy),want=Math.atan2(dy,dx);
      var turn=dist<70?.16:.06;b.a+=Math.max(-turn,Math.min(turn,wrap(want-b.a)));
      var top=(b.fast?2.8:2),goal=Math.min(top,.5+dist*.04);b.v+=(goal-b.v)*.06;
      b.x+=Math.cos(b.a)*b.v;b.y+=Math.sin(b.a)*b.v;b.alt+=((dist<50?dist/50:1)-b.alt)*.08;
      if(dist<5){b.fly=false;b.v=0;b.wait=rnd(4,12);b.look=b.home.night?-1.5708:b.a;}
      return;}
    b.alt*=.86;
    if(b.hop){var h=b.hop;h.u=Math.min(1,h.u+1/15);var e=h.u*h.u*(3-2*h.u);b.x=h.x0+(h.x1-h.x0)*e;b.y=h.y0+(h.y1-h.y0)*e;b.lift=Math.sin(h.u*3.1416);
      if(h.u>=1){b.hop=null;b.lift=0;b.home={x:b.x,y:b.y,tr:b.home.tr};b.wait=b.hops>0?rnd(.2,.5):rnd(4,12);}return;}
    var sleepy=night&&b.home.night;b.tuck+=((sleepy?1:0)-b.tuck)*.03;
    if(b.poke){b.poke=false;var sp=pick(b,true);sp.night=night;go(b,sp,true);birds.forEach(function(o){if(o.mate===b&&!o.fly)o.delay=.3;});return;}
    if(b.delay>=0){b.delay-=1/60;if(b.delay<0){var m=b.mate,s2=spot(m.home.tr);s2.night=m.home.night;go(b,s2,m.fast);}return;}
    b.a+=wrap(b.look-b.a)*.03;
    if(b.speaking)return;
    b.wait-=1/60;
    if(b.wait<0){
      if(night){if(b.home.night){b.wait=999;}else{var r=pick(b);r.night=true;go(b,r,false);}}
      else if(b.hops>0||Math.random()<.5){ // a few quick hops across the same treetop
        if(!(b.hops>0))b.hops=1+(Math.random()*3|0);b.hops--;var tr=b.home.tr,ha=b.a+rnd(-.9,.9),hd=rnd(13,24),hx=b.x+Math.cos(ha)*hd,hy=b.y+Math.sin(ha)*hd;
        if(Math.hypot(hx-tr.px,hy-tr.py)>tr.pr){ha=Math.atan2(tr.py-b.y,tr.px-b.x)+rnd(-.5,.5);hx=b.x+Math.cos(ha)*hd;hy=b.y+Math.sin(ha)*hd;}
        b.a=b.look=ha;b.hop={x0:b.x,y0:b.y,x1:hx,y1:hy,u:0};}
      else if(Math.random()<.3){b.look=b.a+rnd(-1.2,1.2);b.wait=rnd(4,10);}
      else if(birds.filter(function(o){return o.fly;}).length>0){b.wait=rnd(3,8);}   // one flight at a time keeps the page calm
      else{var nx=pick(b);go(b,nx,false);birds.forEach(function(o){if(o.mate===b&&!o.fly)o.delay=rnd(.4,.8);});}
    }});}
function wing(g,span,sw){ // rounded leading edge and tip, then a scalloped row of flight feathers back to the body
  var pts=[[-3.2-sw,.9],[-5.6-sw*.8,.74],[-7.4-sw*.6,.56],[-8.4-sw*.4,.38],[-8.6,.2]],px=-.5-sw,py=1;
  ctx.beginPath();ctx.moveTo(5,g*3);ctx.bezierCurveTo(8-sw*.2,g*span*.42,5-sw*.6,g*span*.94,px,g*span);
  pts.forEach(function(q){ctx.quadraticCurveTo((px+q[0])/2-1.7,g*span*((py+q[1])/2+.05),q[0],g*span*q[1]);px=q[0];py=q[1];});
  ctx.lineTo(-6.5,g*3);ctx.closePath();ctx.fill();}
function drawBird(b){var c=KIND[b.k],s=c.s*(1+b.alt*.1),tk=b.tuck,bob=1;
  var lift=b.lift||0,flap=Math.sin(t*c.flap+b.ph),open=Math.max(Math.min(1,b.alt*1.4),lift*.45),sp=c.span;s*=1+lift*.1;
  if(lift>.05&&b.alt<=.03){ctx.save();ctx.translate(b.x+3*lift,b.y+5*lift);ctx.rotate(b.a);ctx.scale(c.s,c.s);ctx.fillStyle=P.shade;ctx.beginPath();ctx.ellipse(-2,0,11,5.5,0,0,6.283);ctx.fill();ctx.restore();}
  if(b.alt>.03){ctx.save();ctx.translate(b.x+5*b.alt,b.y+8*b.alt);ctx.rotate(b.a);ctx.scale(c.s,c.s);ctx.fillStyle=P.shade;
    ctx.beginPath();ctx.ellipse(-2,0,12,5.5,0,0,6.283);ctx.fill();wing(1,(7+(sp-7)*open)*(.78+.22*flap),4);wing(-1,(7+(sp-7)*open)*(.78+.22*flap),4);ctx.restore();}
  ctx.save();ctx.translate(b.x,b.y);ctx.rotate(b.a);ctx.scale(s*bob,s*bob);
  ctx.fillStyle=c.wing;var tl=c.tail;ctx.beginPath();ctx.moveTo(-6,-2.4-open);ctx.quadraticCurveTo(-7-tl*.6,-2-open*2.2,-7-tl,-.9-open*1.6);ctx.quadraticCurveTo(-8.6-tl,0,-7-tl,.9+open*1.6);ctx.quadraticCurveTo(-7-tl*.6,2+open*2.2,-6,2.4+open);ctx.closePath();ctx.fill();
  if(open>.05){var span=(7+(sp-7)*open)*(.76+.24*flap),sweep=3+3*(1-flap);ctx.fillStyle=c.wing;wing(1,span,sweep);wing(-1,span,sweep);}
  ctx.fillStyle=c.body;ctx.beginPath();ctx.ellipse(0,0,10,6.2,0,0,6.283);ctx.fill();if(c.outline&&!DARK){ctx.strokeStyle=P.edge;ctx.lineWidth=.5;ctx.stroke();}
  if(open<=.6){ctx.globalAlpha=1-open/.6;ctx.fillStyle=c.fold||c.wing;var wy=c.fold?2.9:3.6,wr=c.fold?2.1:2.5,wl=c.fold?6.2:7;ctx.beginPath();ctx.ellipse(-2.2,wy,wl,wr,-.12,0,6.283);ctx.fill();ctx.beginPath();ctx.ellipse(-2.2,-wy,wl,wr,.12,0,6.283);ctx.fill();
    if(c.bar){ctx.fillStyle=c.bar;ctx.beginPath();ctx.ellipse(-1.5,5.5,5.2,.8,-.12,0,6.283);ctx.fill();ctx.beginPath();ctx.ellipse(-1.5,-5.5,5.2,.8,.12,0,6.283);ctx.fill();}
    if(c.pearl){ctx.fillStyle=c.pearl;ctx.beginPath();[[-6.2,2.4],[-4.2,3.4],[-2,2.5],[.2,3.5],[2.2,2.7],[-6.2,-2.4],[-4.2,-3.4],[-2,-2.5],[.2,-3.5],[2.2,-2.7],[-5,0]].forEach(function(d){ctx.moveTo(d[0]+.55,d[1]);ctx.arc(d[0],d[1],.55,0,6.283);});ctx.fill();}
    if(c.stripe){ctx.strokeStyle=c.stripe;ctx.lineWidth=.42;ctx.lineCap='round';ctx.beginPath();[-7.2,-5.6,-4,-2.4,-.8,.8,2.4].forEach(function(d){[1,-1].forEach(function(g){ctx.moveTo(d+.5,g*1.9);ctx.quadraticCurveTo(d-.5,g*3.6,d+.1,g*5.3);});});ctx.stroke();}
    ctx.globalAlpha=1;}
  var hx=8.2-8*tk,hy=2*tk;
  if(tk<.7){ctx.globalAlpha=1-tk/.7;ctx.fillStyle=c.beak;
    if(c.bill){ctx.beginPath();ctx.moveTo(hx+3,hy-.8);ctx.lineTo(hx+4+c.bill,hy);ctx.lineTo(hx+3,hy+.8);ctx.fill();}
    else{ctx.beginPath();ctx.ellipse(hx+4.3,hy,2.1,1.5,0,0,6.283);ctx.fill();}
    if(c.knot){ctx.beginPath();ctx.arc(hx+3.4,hy-3.6,1.5,0,6.283);ctx.fill();}
    ctx.globalAlpha=1;}
  ctx.fillStyle=c.head;ctx.beginPath();ctx.arc(hx,hy,4.3,0,6.283);ctx.fill();
  if(c.stripe){ctx.strokeStyle=c.stripe;ctx.lineWidth=.42;ctx.lineCap='round';ctx.save();ctx.beginPath();ctx.arc(hx,hy,4.3,0,6.283);ctx.clip();ctx.beginPath();[-.2,-1.4,-2.6,-3.8].forEach(function(d){ctx.moveTo(hx+d,hy-4.4);ctx.quadraticCurveTo(hx+d-1.3,hy,hx+d,hy+4.4);});ctx.stroke();ctx.restore();}
  if(c.cheek){ctx.save();ctx.beginPath();ctx.arc(hx,hy,4.3,0,6.283);ctx.clip();ctx.fillStyle=c.cheek;ctx.beginPath();ctx.arc(hx-.6,hy-4.5,2.3,0,6.283);ctx.fill();ctx.beginPath();ctx.arc(hx-.6,hy+4.5,2.3,0,6.283);ctx.fill();ctx.restore();} // cheek patch seen from above: a half circle on each side of the head
  if(c.crest){ctx.fillStyle=c.crest;ctx.beginPath();ctx.moveTo(hx+1.8,hy);ctx.quadraticCurveTo(hx-1.5,hy-1.5,hx-10.5,hy);ctx.quadraticCurveTo(hx-1.5,hy+1.5,hx+1.8,hy);ctx.closePath();ctx.fill();}
  ctx.restore();
  var na=(1-Math.min(1,b.alt*3))*(1-tk);if(c.label&&na>.02){var ga=ctx.globalAlpha;ctx.globalAlpha=ga*na*.8;ctx.font='600 10.5px Manrope,system-ui,sans-serif';ctx.textAlign='center';ctx.textBaseline='middle';ctx.lineJoin='round';ctx.lineWidth=3;ctx.strokeStyle=DARK?'rgba(20,23,26,.75)':'rgba(255,253,248,.8)';ctx.fillStyle=DARK?'#e8e6e1':'#3a4340';ctx.strokeText(c.label,b.x,b.y+17*c.s);ctx.fillText(c.label,b.x,b.y+17*c.s);ctx.globalAlpha=ga;}}
function frame(){ctx.clearRect(0,0,W,H);var faint=(W-760)/2<=120;ctx.globalAlpha=faint?.45:1;
  drawTrees();
  placeSay();
  birds.filter(function(b){return !b.fly;}).forEach(drawBird);birds.filter(function(b){return b.fly;}).forEach(drawBird);
  ctx.globalAlpha=1;}

// ---- each bird is a small language model: an n-gram model that has only ever heard the words on this page.
// Click one and it says a sentence, one word at a time.
var LM={keet:{n:1,T:1.25,name:'Kiwi the parakeet',what:'bigram model · remembers 1 word back, so it rambles'},
        pearl:{n:2,T:1,name:'Pearl the cockatiel',what:'trigram model · remembers 2 words back'},
        gray:{n:3,T:.8,name:'Ashe the cockatiel',what:'4-gram model · remembers 3 words back, nearly quotes'}},toks=[],tab=[{},{},{},{}],starts=[];
var HEARD=[
  'Victoria works on representation learning.',
  'Victoria works on retrieval and vector search at billion scale.',
  'Victoria is an ML research scientist.',
  'Victoria defended her Ph.D. at UC San Diego.',
  'Victoria was at Google and at Meta.',
  'Victoria is open to research scientist roles in 2026.',
  'She works on LLMs and how LLMs locate items in a list.',
  'She works on multimodal foundation models and language models.',
  'She works on self-supervised learning and generative models.',
  'She trains models for robust generalization under distribution shift.',
  'She trains models for few-shot and zero-shot decoding.',
  'She decodes handwriting for the Meta Neural Band.',
  'She learns nested embeddings for multiscale clustering.',
  'She draws and takes pictures of the sky.',
  'She lives with three birds and the birds are small language models.',
  'The birds work on seeds.'
];
(function train(){toks=HEARD.join(' ').split(' ');
  for(var i=0;i<toks.length;i++){if(i===0||(ends(toks[i-1])&&/^[A-Z]/.test(toks[i])))starts.push(i);
    for(var k=1;k<=3&&i-k>=0;k++){if(toks.slice(i-k,i).some(function(w,q,arr){return q<arr.length-1&&ends(w);}))continue;var key=toks.slice(i-k,i).join(' '),m=tab[k][key]||(tab[k][key]={});m[toks[i]]=(m[toks[i]]||0)+1;}}})();
function ends(w){return /[.!?]$/.test(w)&&!/^(Ph\.D\.|Dr\.|M\.S\.|B\.S\.|e\.g\.|i\.e\.)$/.test(w);}
function nextTok(ctx,n,T){for(var k=Math.min(n,ctx.length);k>=1;k--){var m=tab[k][ctx.slice(-k).join(' ')];if(!m)continue;
    var ws=Object.keys(m),sum=0,p=ws.map(function(w){var v=Math.pow(m[w],1/T);sum+=v;return v;}),r=Math.random()*sum;for(var i=0;i<ws.length;i++){r-=p[i];if(r<=0)return ws[i];}return ws[ws.length-1];}
  return null;}
var say=document.getElementById('say'),sayText=document.getElementById('sayText'),sayMeta=document.getElementById('sayMeta'),talker=null,sayT=null;
function hush(fly){clearTimeout(sayT);say.classList.remove('on');if(talker){talker.speaking=false;if(fly)talker.poke=true;talker=null;}}
function speak(b){hush(false);talker=b;b.speaking=true;var m=LM[b.k],out=[],night=b.tuck>.5;
  sayMeta.textContent=m.name+' · '+m.what;sayText.textContent='';say.classList.add('on');
  if(night){sayText.textContent='zzz';sayT=setTimeout(function(){hush(false);},1800);return;}
  out.push(toks[starts[(Math.random()*starts.length)|0]]);
  (function more(){sayText.textContent=out.join(' ');var last=out[out.length-1];
    if(out.length>=22||(ends(last)&&out.length>4)){sayT=setTimeout(function(){hush(true);},3200);return;}
    var w=nextTok(out,m.n,m.T);if(!w){sayT=setTimeout(function(){hush(true);},3200);return;}out.push(w);sayT=setTimeout(more,95);})();}
function birdAt(x,y){var best=null,bd=30;birds.forEach(function(b){var d=Math.hypot(b.x-x,b.y-y);if(d<bd&&!b.fly){bd=d;best=b;}});return best;}
addEventListener('click',function(e){if(e.target.closest&&e.target.closest('a,button,input,.say'))return;var b=birdAt(e.clientX,e.clientY);if(b)speak(b);else if(talker)hush(false);});
addEventListener('pointermove',function(e){root.style.cursor=birdAt(e.clientX,e.clientY)?'pointer':'';});
function placeSay(){if(!talker)return;var x=Math.max(12,Math.min(W-292,talker.x+18)),y=talker.y-18;say.style.left=x+'px';say.style.bottom=Math.max(12,H-y)+'px';}

function resize(){var d=Math.min(devicePixelRatio||1,2);W=innerWidth;H=innerHeight;cv.width=W*d;cv.height=H*d;ctx.setTransform(d,0,0,d,0,0);}
function settle(){if(!isNight())return;birds.forEach(function(b){var sp=pick(b);sp.night=true;b.home=sp;b.x=sp.x;b.y=sp.y;b.fly=false;b.tuck=1;b.wait=999;b.a=b.look=-1.5708;});}
addEventListener('pointermove',function(e){mouse.x=e.clientX;mouse.y=e.clientY;});
addEventListener('pointerdown',function(e){mouse.x=e.clientX;mouse.y=e.clientY;});
document.addEventListener('pointerleave',function(){mouse.x=mouse.y=-9999;});
var rz;addEventListener('resize',function(){clearTimeout(rz);rz=setTimeout(function(){if(innerWidth===W&&Math.abs(innerHeight-H)<160){resize();if(reduce)frame();return;}resize();makeTrees();makeBirds();settle();if(reduce)frame();},150);});
var qh=new URLSearchParams(location.search).get('hour');if(qh!==null)preview=+qh;
resize();readVars();clock();makeTrees();makeBirds();settle();
if(reduce)frame();else (function loop(){step();frame();requestAnimationFrame(loop);})();
})();
