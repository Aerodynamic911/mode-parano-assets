# Shorts YouTube — chaîne « Mode Parano » (@mode.parano)

Contenus faits pour YouTube Shorts (vertical 1080x1920, 15 à 25 s, avec un passage de musique de Solauw Sound depuis le 27/11/2026 (avant : sans son), accroche dès la première seconde, question finale pour les commentaires).
Chaque dossier `AAAA-MM-JJ-sujet/` (date de publication) contient `short.mp4`, `cover.jpg`, `spec.json` (texte et durées), `publication.json` (titre, description, tags, sources, identifiant Metricool).
Générateur : `python3 outils/make_short.py <dossier>` (mode d'emploi en tête du fichier). Planification : tâche mensuelle du 2 à 15h23 ; lot du 15/11/2026 jusqu'au 02/12/2026.
Programmation Metricool : `youtubeData` = {title, type "short", privacy "public", tags, category, madeForKids false, isAiGeneratedContent false}. Catégorie `EDUCATION` acceptée par Metricool (test du 15/11).

| Date | Sujet | Dossier | Id Metricool | Statut |
|---|---|---|---|---|
| 2026-11-15 12:42 | 5 réglages urgents à changer sur ton téléphone | `2026-11-15-5-reglages-urgents` | 428807109 | programmé |
| 2026-11-15 13:12 | Ton téléphone t'écoute-t-il vraiment ? | `2026-11-15-telephone-ecoute` | 428807951 | programmé |
| 2026-11-15 13:42 | « Maman, j'ai un problème » : l'arnaque au faux proche | `2026-11-15-maman-probleme` | 428807971 | programmé |
| 2026-11-15 14:12 | Objets connectés : 3 réflexes pour les sécuriser | `2026-11-15-objets-connectes` | 428807998 | programmé |
| 2026-11-15 14:42 | Ta box Wi-Fi est-elle une passoire ? | `2026-11-15-box-wifi` | 428808023 | programmé |
| 2026-11-15 15:12 | VPN gratuit : qui paie vraiment ? | `2026-11-15-vpn-gratuit` | 428808032 | programmé |
| 2026-11-16 | Ton mot de passe est-il dans la liste des pires ? | `2026-11-16-mots-de-passe-top` | 429087524 | programmé |
| 2026-11-18 | Un mot de passe ne suffit plus : active la double authentification | `2026-11-18-double-authentification` | 429087648 | programmé |
| 2026-11-20 | Wi-Fi public : 3 règles pour ne pas se faire pirater | `2026-11-20-wifi-public` | 429087696 | programmé |
| 2026-11-22 | Faux SMS : 3 signes pour repérer le piège | `2026-11-22-faux-sms` | 429087738 | programmé |
| 2026-11-24 | Black Friday : 3 réflexes contre les arnaques | `2026-11-24-black-friday` | 429087790 | programmé |
| 2026-11-26 | Pourquoi tu dois faire tes mises à jour | `2026-11-26-mises-a-jour` | 429087835 | programmé |
| 2026-11-28 | Tes vieux comptes sont une porte ouverte | `2026-11-28-comptes-oublies` | 429087868 | programmé |
| 2026-11-30 | Sauvegarde : la règle 3-2-1 expliquée en 20 secondes | `2026-11-30-sauvegarde-3-2-1` | 429087914 | programmé |
| 2026-12-02 | Cette appli a-t-elle besoin de ton micro ? | `2026-12-02-permissions-applis` | 429087963 | programmé |

Lot 0 du 15/11 : 6 Shorts tirés des 6 sujets les plus vus sur Instagram (posts.json du tableau de bord), publiés dès le 15/11 à la demande de Julien pour remplir la chaîne.
Miniatures : chaque Short a une `miniature.jpg` (1080x1920, outil `outils/make_miniature.py`), envoyée à Metricool avec `videoThumbnailUrl` ; Metricool l'a acceptée le 15/11 (reste à voir si YouTube l'applique à la publication). Les 6 Shorts du 15/11 ont eu leur miniature ajoutée à la main par Julien dans Studio.
Notes : chaque Short se termine par un appel à s'abonner (décision de Julien, 15/11). Aucun lien d'affiliation sur YouTube sauf demande. Tout garder dans ce dépôt, ne rien supprimer.

## Musique (depuis le 27/11/2026)
Passages de 28 s de Solauw Sound dans `../musique/` (voir `../musique/README.md`). `make_short.py` les intègre (clé « musique » du spec.json, sinon choix automatique) et dessine « ♪ Solauw Sound · Titre » en bas de l'image ; `ajoute_musique.py` fait la même chose sur une vidéo déjà faite. Description YouTube : ajouter la ligne « Musique : Solauw Sound – Titre ».
Vidéos refaites avec musique le 27/11 (fichier `short-musique.mp4`, le `short.mp4` d'origine est gardé) et reprogrammées dans Metricool : Reel IG 28/11 12h30 (faux proche, Liftoff) ; Shorts YouTube 28/11 comptes-oublies (Eclipse), 30/11 sauvegarde-3-2-1 (Flow), 02/12 permissions-applis (Friction) ; TikTok 28/11 mots-de-passe-top (Overload), 30/11 double-authentification (Apogee), 02/12 telephone-ecoute (Eclipse), 04/12 maman-probleme (Liftoff).
