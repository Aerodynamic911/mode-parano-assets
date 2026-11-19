// Carrousel, story et épingle "checklist" (19/11/2026). Usage : node gen_checklist.js (depuis ce dossier)
const {chromium}=require('playwright');const fs=require('fs');
const STEPS=[['Verrouille ta boîte mail','Active la double authentification, de préférence avec une application plutôt que par SMS.'],
['Un mot de passe long et unique par compte important','Un gestionnaire de mots de passe t’évite de tout retenir.'],
['Active les mises à jour automatiques','Téléphone, ordinateur, box internet : elles ferment des failles connues.'],
['Vérifie les appareils connectés à tes comptes','Déconnecte ceux que tu ne reconnais pas.'],
['Cache les aperçus de messages sur l’écran verrouillé','Les codes reçus par SMS ne s’affichent plus sans déverrouiller le téléphone.']];
const css=`*{margin:0;box-sizing:border-box}body{background:#070D0A;color:#F5F7F6;font-family:Inter;position:relative}
.br{position:absolute;top:70px;width:100%;text-align:center;font:700 30px Poppins;color:#00C46A}
.dots{position:absolute;bottom:62px;width:100%;display:flex;justify-content:center;gap:12px}.dots i{width:14px;height:14px;border-radius:50%;background:#3a403d}.dots i.on{background:#00C46A}
.c{position:absolute;left:80px;right:80px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center}.ctr{text-align:center;align-items:center}
.k{font:700 28px Poppins;color:#00C46A;letter-spacing:.06em;margin-bottom:34px}h1{font:700 78px/1.12 Poppins;margin-bottom:34px}p{font:400 40px/1.45 Inter;color:#c9cfcc}
.n{font:700 150px/1 Poppins;color:#00C46A;margin-bottom:20px}.st h1{font-size:60px}
.b{white-space:nowrap;margin-top:60px;color:#00C46A;font:700 40px/1.3 Poppins;border-top:3px solid #1d3a2a;padding-top:36px}
.sw{margin-top:70px;border:3px solid #00C46A;color:#00C46A;font:700 32px Poppins;padding:14px 40px;border-radius:999px}
ol{list-style:none;margin-top:30px;text-align:left}li{font:600 36px/1.3 Poppins;margin:22px 0;padding-left:56px;position:relative}li:before{content:'';position:absolute;left:0;top:6px;width:34px;height:34px;border:4px solid #00C46A;border-radius:8px}`;
(async()=>{const b=await chromium.launch();
// carrousel
let pg=await b.newPage({viewport:{width:1080,height:1350}});const dir='instagram-2026-11/66-checklist';
const slides=[{t:'cover'},...STEPS.map((x,i)=>({t:'step',n:'0'+(i+1),h:x[0],p:x[1]})),{t:'cta'}];
const dots=i=>slides.map((_,j)=>`<i class="${j==i?'on':''}"></i>`).join('');
for(let i=0;i<slides.length;i++){const x=slides[i];
const body=`${x.t!='step'?'<div class="br">mode.parano</div>':''}<div class="c ${x.t=='step'?'st':'ctr'}">`+
(x.t=='cover'?`<div class="k">CHECKLIST GRATUITE</div><h1>5 réglages à faire ce soir</h1><p>10 minutes, rien à installer. Reçois-la en PDF.</p><div class="sw">SWIPE  ›</div>`:x.t=='step'?`<div class="n">${x.n}</div><h1>${x.h}</h1><p>${x.p}</p>`:`<h1>Commente CHECKLIST</h1><p>Je t’envoie la checklist gratuite en message privé.</p><div class="b">mode-parano.com/checklist</div>`)+`</div><div class="dots">${dots(i)}</div>`;
await pg.setContent(`<html><body style="width:1080px;height:1350px"><style>${css}</style>${body}</body></html>`);await pg.waitForTimeout(150);
await pg.screenshot({path:`${dir}/0${i+1}.jpg`,type:'jpeg',quality:92});}
// story 1080x1920
pg=await b.newPage({viewport:{width:1080,height:1920}});
await pg.setContent(`<html><body style="width:1080px;height:1920px"><style>${css}.c{top:200px;bottom:380px}h1{font-size:84px}</style><div class="br" style="top:120px">mode.parano</div><div class="c ctr"><div class="k">CHECKLIST GRATUITE</div><h1>5 réglages à faire ce soir</h1><p>10 minutes, rien à installer.</p><ol>${STEPS.map(s=>`<li>${s[0]}</li>`).join('')}</ol><div class="sw" style="margin-top:60px">LIEN CI-DESSOUS  ↓</div></div></body></html>`);await pg.waitForTimeout(150);
await pg.screenshot({path:'stories-2026-11/19-11-checklist.png'});
// épingle 1000x1500
pg=await b.newPage({viewport:{width:1000,height:1500}});
await pg.setContent(`<html><body style="width:1000px;height:1500px"><style>${css}.c{top:0;bottom:0;left:70px;right:70px}h1{font-size:76px}li{font-size:34px}</style><div class="br" style="top:90px">mode.parano</div><div class="c ctr"><div class="k">CHECKLIST GRATUITE</div><h1>5 réglages à faire ce soir</h1><p>10 minutes, rien à installer.</p><ol>${STEPS.map(s=>`<li>${s[0]}</li>`).join('')}</ol><div class="b" style="margin-top:50px;font-size:34px">mode-parano.com/checklist</div></div></body></html>`);await pg.waitForTimeout(150);
await pg.screenshot({path:'pinterest-2026-11/11-20-checklist.png'});
await b.close()})();
