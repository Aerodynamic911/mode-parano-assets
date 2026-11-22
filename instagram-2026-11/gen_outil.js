// Carrousels « L'outil du mercredi » (rubrique créée le 22/11/2026). Usage : NODE_PATH=$(npm root -g) node instagram-2026-11/gen_outil.js (depuis la racine du dépôt)
const {chromium}=require('playwright');
const TOOLS={
 'instagram-2026-11/67-outil-hibp':{kicker:"L'OUTIL DU MERCREDI",title:"Ton e-mail a-t-il fuité&nbsp;?",sub:"Have I Been Pwned : gratuit, fiable, une minute.",
  steps:[["C'est quoi ?","Un site gratuit créé par Troy Hunt, en ligne depuis 2013. Il indique si ton adresse e-mail apparaît dans une fuite de données connue."],
  ["Comment l'utiliser","Va sur haveibeenpwned.com et tape ton adresse. Le site liste les fuites où elle apparaît. D'après lui, les recherches ne sont pas enregistrées."],
  ["Reste prévenu(e)","Avec « Notify Me », tu es averti(e) si ton adresse apparaît dans une future fuite."],
  ["Ton adresse apparaît ?","Ça ne prouve pas que tu es piraté(e). Change le mot de passe du compte concerné, ne le réutilise nulle part et active la double authentification."],
  ["Les limites","Le site ne connaît que les fuites qu'il a recensées : une adresse absente ne veut pas dire « aucun risque »."]],
  cta:["Enregistre ce post","Rendez-vous mercredi prochain à 12h30 pour un nouvel outil."]},
 'instagram-2026-12/68-outil-signal':{kicker:"L'OUTIL DU MERCREDI",title:"Une messagerie qui ne lit pas tes messages",sub:"Signal : gratuit, sans pub, chiffré par défaut.",
  steps:[["C'est quoi ?","Une messagerie gratuite, gérée par une association à but non lucratif. Elle existe sur Android, iPhone et ordinateur."],
  ["Chiffrée en permanence","Messages et appels sont toujours chiffrés de bout en bout. Signal dit ne pas pouvoir les lire."],
  ["Très peu de données","D'après Signal : ton numéro pour l'inscription, le minimum technique, pas de pub et pas de suivi. Ton historique reste sur ton appareil."],
  ["Pour démarrer","Installe l'appli depuis le magasin officiel, inscris-toi, puis invite un proche. Elle ne sert que si tes contacts l'utilisent aussi."],
  ["Les limites","Un numéro de téléphone est demandé à l'inscription, et tes données techniques peuvent être transférées vers les États-Unis et d'autres pays, selon sa politique."]],
  cta:["Enregistre ce post","Rendez-vous mercredi prochain à 12h30 pour un nouvel outil."]}};
const css=`*{margin:0;box-sizing:border-box}body{background:#070D0A;color:#F5F7F6;font-family:Inter;position:relative}
.br{position:absolute;top:70px;width:100%;text-align:center;font:700 30px Poppins;color:#00C46A}
.dots{position:absolute;bottom:62px;width:100%;display:flex;justify-content:center;gap:12px}.dots i{width:14px;height:14px;border-radius:50%;background:#3a403d}.dots i.on{background:#00C46A}
.c{position:absolute;left:80px;right:80px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center}.ctr{text-align:center;align-items:center}
.k{font:700 28px Poppins;color:#00C46A;letter-spacing:.06em;margin-bottom:34px}h1{font:700 78px/1.12 Poppins;margin-bottom:34px}p{font:400 40px/1.45 Inter;color:#c9cfcc}
.n{font:700 150px/1 Poppins;color:#00C46A;margin-bottom:20px}.st h1{font-size:60px}
.b{margin-top:60px;color:#00C46A;font:700 36px/1.3 Poppins;border-top:3px solid #1d3a2a;padding-top:36px}
.sw{margin-top:70px;border:3px solid #00C46A;color:#00C46A;font:700 32px Poppins;padding:14px 40px;border-radius:999px}`;
(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1080,height:1350}});
for(const [dir,T] of Object.entries(TOOLS)){
 const slides=[{t:'cover'},...T.steps.map((x,i)=>({t:'step',n:'0'+(i+1),h:x[0],p:x[1]})),{t:'cta'}];
 const dots=i=>slides.map((_,j)=>`<i class="${j==i?'on':''}"></i>`).join('');
 for(let i=0;i<slides.length;i++){const x=slides[i];
  const body=`${x.t!='step'?'<div class="br">mode.parano</div>':''}<div class="c ${x.t=='step'?'st':'ctr'}">`+
  (x.t=='cover'?`<div class="k">${T.kicker}</div><h1>${T.title}</h1><p>${T.sub}</p><div class="sw">SWIPE  ›</div>`:x.t=='step'?`<div class="n">${x.n}</div><h1>${x.h}</h1><p>${x.p}</p>`:`<h1>${T.cta[0]}</h1><p>${T.cta[1]}</p>`)+`</div><div class="dots">${dots(i)}</div>`;
  await pg.setContent(`<html><body style="width:1080px;height:1350px"><style>${css}</style>${body}</body></html>`);await pg.waitForTimeout(150);
  await pg.screenshot({path:`${dir}/0${i+1}.jpg`,type:'jpeg',quality:92});}}
await b.close()})();
