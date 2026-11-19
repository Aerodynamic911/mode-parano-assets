// Génère les carrousels "5 réglages" (1080x1350). Usage : node gen_reglages.js
const {chromium}=require('playwright');const fs=require('fs');
const SETS={
'14-reglages-facebook':{kw:'FACEBOOK',cover:{k:'FACEBOOK',h:'5 réglages à changer sur Facebook',p:'4 minutes, rien à installer. Tout se fait dans tes paramètres.'},
steps:[
['Lance le contrôle de confidentialité','Dans les paramètres, cherche « Contrôle de confidentialité ». Facebook te fait revoir qui voit quoi et la sécurité de ton compte.'],
['Active la double authentification','Espace Comptes, Mot de passe et sécurité. Choisis de préférence une application d’authentification plutôt que le SMS.'],
['Active les alertes de connexion','Tu es prévenu si quelqu’un se connecte. Déconnecte aussi les appareils que tu ne reconnais pas.'],
['Choisis qui voit tes publications','Mets l’audience par défaut sur « Amis » plutôt que « Public », et limite l’audience de tes anciennes publications.'],
['Retire les applis que tu n’utilises plus','Paramètres, Applications et sites web. Supprime les anciens jeux et applis qui ont encore accès à ton compte.']],
cta:['Combien tu en avais déjà faits ?','Commente un chiffre de 0 à 5. Enregistre le post pour les faire ce soir.','Guide gratuit : mode-parano.com']},
'15-reglages-amazon':{kw:'AMAZON',cover:{k:'AMAZON',h:'5 réglages à changer sur ton compte Amazon',p:'4 minutes. Adresse, paiement, historique : protège tout ça.'},
steps:[
['Crée une clé d’accès','Connexion et sécurité, puis « Configurer » à côté de Clés d’accès. Tu te connectes avec ton empreinte, ton visage ou le code du téléphone.'],
['Active la vérification en deux étapes','Choisis de préférence une application d’authentification plutôt que le SMS. Garde les codes de secours hors ligne.'],
['Fais le tri dans tes moyens de paiement','Supprime les cartes que tu n’utilises plus. Vérifie si le paiement en un clic est activé et décide si tu le gardes.'],
['Nettoie ton historique de navigation','Supprime les articles que tu ne veux pas voir dans les recommandations, ou désactive l’historique.'],
['Règle la confidentialité d’Alexa','Dans l’application Alexa, supprime les enregistrements vocaux ou fais-les effacer automatiquement.']],
cta:['Combien tu en avais déjà faits ?','Commente un chiffre de 0 à 5. Enregistre le post pour les faire ce soir.','Guide gratuit : mode-parano.com']}};
const css=`*{margin:0;box-sizing:border-box}body{width:1080px;height:1350px;background:#070D0A;color:#F5F7F6;font-family:Inter;position:relative}
.br{position:absolute;top:70px;width:100%;text-align:center;font:700 30px Poppins;color:#00C46A}
.dots{position:absolute;bottom:62px;width:100%;display:flex;justify-content:center;gap:12px}.dots i{width:14px;height:14px;border-radius:50%;background:#3a403d}.dots i.on{background:#00C46A}
.c{position:absolute;left:80px;right:80px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center}.ctr{text-align:center;align-items:center}
.k{font:700 28px Poppins;color:#00C46A;letter-spacing:.06em;margin-bottom:34px}h1{font:700 78px/1.12 Poppins;margin-bottom:34px}p{font:400 40px/1.45 Inter;color:#c9cfcc}
.n{font:700 150px/1 Poppins;color:#00C46A;margin-bottom:20px}.st h1{font-size:62px}
.b{white-space:nowrap;margin-top:60px;color:#00C46A;font:700 40px/1.3 Poppins;border-top:3px solid #1d3a2a;padding-top:36px;max-width:820px}
.sw{margin-top:70px;border:3px solid #00C46A;color:#00C46A;font:700 32px Poppins;padding:14px 40px;border-radius:999px}`;
(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1080,height:1350}});
for(const [dir,s] of Object.entries(SETS)){fs.mkdirSync(dir,{recursive:true});
const slides=[{t:'cover',...s.cover},...s.steps.map((x,i)=>({t:'step',n:'0'+(i+1),h:x[0],p:x[1]})),{t:'cta',h:s.cta[0],p:s.cta[1],b:s.cta[2]}];
const dots=i=>slides.map((_,j)=>`<i class="${j==i?'on':''}"></i>`).join('');
for(let i=0;i<slides.length;i++){const x=slides[i];
const body=`${x.t!='step'?'<div class="br">mode.parano</div>':''}<div class="c ${x.t=='step'?'st':'ctr'}">`+
(x.t=='cover'?`<div class="k">${x.k}</div><h1>${x.h}</h1><p>${x.p}</p><div class="sw">SWIPE  ›</div>`:x.t=='step'?`<div class="n">${x.n}</div><h1>${x.h}</h1><p>${x.p}</p>`:`<h1>${x.h}</h1><p>${x.p}</p><div class="b">${x.b}</div>`)+`</div><div class="dots">${dots(i)}</div>`;
await pg.setContent(`<html><body><style>${css}</style>${body}</body></html>`);await pg.waitForTimeout(150);
await pg.screenshot({path:`${dir}/0${i+1}.jpg`,type:'jpeg',quality:92});}}
await b.close()})();
