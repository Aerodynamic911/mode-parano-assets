#!/usr/bin/env python3
"""Fabrique un Short YouTube vertical (1080x1920, 30 i/s, H.264) à partir d'un fichier spec.json.

Usage : python3 make_short.py <dossier-du-short> [fichier-de-sortie]      (lit <dossier>/spec.json, écrit <dossier>/short.mp4 et cover.jpg ;
        avec un 2e argument (ex. short-musique.mp4), n'écrit que ce fichier : pour garder le short.mp4 déjà publié)

Format du spec.json :
{
  "slug": "mots-de-passe-top",
  "beats": [
    {"duree": 3.0, "kicker": "ASTUCE", "num": null, "lignes": ["Ton mot de passe", "est dans *cette liste* ?"], "sous": ["Texte secondaire (Inter)"]},
    ...
  ]
}
- « *mot* » met le mot en vert. « num » = numéro dans une pastille (1, 2, 3...).
- Musique (depuis le 27/11/2026) : chaque vidéo porte un passage de musique de Solauw Sound (dossier ../musique/, voir morceaux.json).
  Clé facultative « musique » du spec.json : "Eclipse" (un des 6 titres : Liftoff, Overload, Eclipse, Friction, Apogee, Flow) ou false pour une vidéo sans musique.
  Si la clé manque, le titre est choisi automatiquement (même vidéo = même titre). Fondu d'entrée 0,3 s, fondu de sortie 1,3 s, niveau -18 LUFS.
  Le clin d'œil à l'artiste (« ♪ Solauw Sound · Titre ») est dessiné en bas de l'image. Pour une vidéo déjà faite : outils/ajoute_musique.py.
Identité mode.parano : fond #070D0A, texte #F5F7F6, vert #00C46A, Poppins Bold + Inter Regular.
Zones de sécurité Shorts : texte entre y=330 et y=1380, marges de 90 px (l'interface YouTube couvre le bas et la droite).
"""
import json, re, subprocess, sys, pathlib, zlib
from PIL import Image, ImageDraw, ImageFont

MUSIQUE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent / "musique"
FONDU_ENTREE, FONDU_SORTIE = 0.3, 1.3

def morceaux():
    return json.loads((MUSIQUE_DIR / "morceaux.json").read_text(encoding="utf-8"))

def choisir_morceau(spec):
    """Titre de musique d'un spec : valeur de « musique », ou choix automatique stable à partir du slug ; None si false."""
    m = spec.get("musique", "auto")
    if m is False or m is None: return None
    liste = sorted(morceaux())
    if m == "auto": return liste[zlib.crc32(spec.get("slug", "").encode()) % len(liste)]
    if m not in liste: sys.exit(f"Morceau inconnu : {m} (choix : {', '.join(liste)})")
    return m

W, H, FPS = 1080, 1920, 30
BG = (7, 13, 10); WH = (245, 247, 246); GR = (0, 196, 106); GY = (130, 140, 135)
B = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
R = "/usr/share/fonts/opentype/inter/Inter-Regular.otf"
F_MAIN = ImageFont.truetype(B, 88); F_KICK = ImageFont.truetype(B, 38)
F_SUB = ImageFont.truetype(R, 52); F_NUM = ImageFont.truetype(B, 64); F_BRAND = ImageFont.truetype(R, 36)
F_CREDIT = ImageFont.truetype(R, 30); GR_DISCRET = (70, 150, 110)

def parse(line):
    """'texte *vert* texte' -> [(texte, couleur)]"""
    parts, out = re.split(r"(\*[^*]+\*)", line), []
    for p in parts:
        if not p: continue
        out.append((p[1:-1], GR) if p.startswith("*") else (p, WH))
    return out

def width(segs, font):
    _d = ImageDraw.Draw(Image.new("L", (1, 1)))
    return sum(_d.textlength(t, font=font) for t, _ in segs)

def draw_segs(d, segs, font, y, center=W / 2):
    x = center - width(segs, font) / 2
    for t, c in segs:
        d.text((x, y), t, font=font, fill=c)
        x += d.textlength(t, font=font)

def beat_layer(b):
    """Calque RGBA d'un beat (texte centré dans la zone de sécurité)."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    lignes = [parse(l) for l in b["lignes"]]
    global F_MAIN
    taille = 88
    while taille > 56 and max(width(l, ImageFont.truetype(B, taille)) for l in lignes) > 900:
        taille -= 2                                  # le texte doit tenir dans 900 px (marges Shorts)
    F_MAIN = ImageFont.truetype(B, taille)
    sous = b.get("sous", [])
    h = len(lignes) * 112 + (len(sous) * 72 + 50 if sous else 0)
    if b.get("kicker"): h += 80
    if b.get("num"): h += 150
    y = 855 - h // 2
    if b.get("num"):
        cx = W // 2
        d.ellipse((cx - 62, y, cx + 62, y + 124), outline=GR, width=7)
        s = str(b["num"]); w = d.textlength(s, font=F_NUM)
        d.text((cx - w / 2, y + 22), s, font=F_NUM, fill=GR)
        y += 160
    if b.get("kicker"):
        w = d.textlength(b["kicker"], font=F_KICK)
        d.text(((W - w) / 2, y), b["kicker"], font=F_KICK, fill=GR); y += 80
    for segs in lignes:
        draw_segs(d, segs, F_MAIN, y); y += 112
    if sous:
        y += 40
        for s in sous:
            draw_segs(d, [(s, (225, 230, 228))], F_SUB, y); y += 72
    return layer

def credit_texte(morceau):
    return f"Solauw Sound · {morceau}"

def dessine_note(d, x, y, h, couleur):
    """Petite croche dessinée à la main (indépendante des polices) : tête ovale, hampe, crochet. (x, y) = coin haut gauche."""
    r = h * 0.17
    cx, cy = x + r, y + h - r
    d.ellipse((cx - r * 1.25, cy - r, cx + r * 1.25, cy + r), fill=couleur)
    hx = cx + r * 1.2
    d.rectangle((hx - h * 0.045, y, hx + h * 0.045, cy), fill=couleur)
    d.polygon([(hx, y), (hx + h * 0.34, y + h * 0.28), (hx + h * 0.30, y + h * 0.46), (hx, y + h * 0.22)], fill=couleur)

def base_frame(morceau=None):
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    w = d.textlength("@mode.parano", font=F_BRAND)
    d.text(((W - w) / 2, 1450), "@mode.parano", font=F_BRAND, fill=GY)
    if morceau:                                      # clin d'œil à l'artiste, discret, au-dessus du nom du compte
        t = credit_texte(morceau); w = d.textlength(t, font=F_CREDIT); ic = 30; gap = 12
        x0 = (W - (ic + gap + w)) / 2
        dessine_note(d, x0, 1399, ic, GR_DISCRET)
        d.text((x0 + ic + gap, 1398), t, font=F_CREDIT, fill=GR_DISCRET)
    return im

def main(dossier, sortie="short.mp4"):
    dossier = pathlib.Path(dossier)
    spec = json.loads((dossier / "spec.json").read_text(encoding="utf-8"))
    beats = spec["beats"]
    total = sum(b["duree"] for b in beats)
    layers = [beat_layer(b) for b in beats]
    morceau = choisir_morceau(spec)
    base = base_frame(morceau)
    out = dossier / sortie; tmp = dossier / (sortie + ".tmp.mp4")
    if morceau:
        info = morceaux()[morceau]
        if total > info["duree_s"] - 0.5: sys.exit(f"Vidéo de {total:.1f} s : passage de {morceau} trop court ({info['duree_s']} s)")
        audio_in = ["-i", str(MUSIQUE_DIR / info["fichier"])]
        af = f"afade=t=in:st=0:d={FONDU_ENTREE},afade=t=out:st={total - FONDU_SORTIE:.2f}:d={FONDU_SORTIE}"
    else:                                            # sans musique : piste silencieuse
        audio_in = ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100"]; af = "anull"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-"] + audio_in + [
           "-map", "0:v", "-map", "1:a", "-vf", "setsar=1,format=yuv420p", "-af", af, "-t", f"{total:.3f}",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k" if morceau else "96k", "-ar", "44100", "-movflags", "+faststart", str(tmp)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    nframes = int(round(total * FPS)); t0 = 0.0; idx = 0
    starts = []
    for b in beats: starts.append(t0); t0 += b["duree"]
    cover_done = False
    for f in range(nframes):
        t = f / FPS
        while idx + 1 < len(beats) and t >= starts[idx + 1]: idx += 1
        lt = t - starts[idx]; dur = beats[idx]["duree"]
        a = min(1.0, lt / 0.25)                       # fondu d'entrée
        if idx < len(beats) - 1 and dur - lt < 0.15:  # fondu de sortie
            a = min(a, max(0.0, (dur - lt) / 0.15))
        rise = int(24 * (1 - min(1.0, lt / 0.25)))    # petite montée
        frame = base.copy()
        d = ImageDraw.Draw(frame)
        d.rectangle((90, 130, 90 + int((W - 180) * (t / total)), 138), fill=GR)   # barre de progression
        d.rectangle((90, 130, W - 90, 138), outline=None)
        lay = layers[idx]
        if a < 1.0:
            r, g, bl, al = lay.split(); al = al.point(lambda v: int(v * a)); lay = Image.merge("RGBA", (r, g, bl, al))
        frame.paste(lay, (0, rise), lay)
        if sortie == "short.mp4" and not cover_done and lt > 0.5:
            frame.convert("RGB").save(dossier / "cover.jpg", quality=92); cover_done = True
        p.stdin.write(frame.tobytes())
    p.stdin.close(); p.wait()
    if p.returncode == 0: tmp.rename(out)
    else: sys.exit("ffmpeg a échoué")
    print(f"OK {out} ({total:.1f} s, musique : {morceau or 'aucune'})")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "short.mp4")
