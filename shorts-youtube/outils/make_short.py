#!/usr/bin/env python3
"""Fabrique un Short YouTube vertical (1080x1920, 30 i/s, H.264) à partir d'un fichier spec.json.

Usage : python3 make_short.py <dossier-du-short>      (lit <dossier>/spec.json, écrit <dossier>/short.mp4 et cover.jpg)

Format du spec.json :
{
  "slug": "mots-de-passe-top",
  "beats": [
    {"duree": 3.0, "kicker": "ASTUCE", "num": null, "lignes": ["Ton mot de passe", "est dans *cette liste* ?"], "sous": ["Texte secondaire (Inter)"]},
    ...
  ]
}
- « *mot* » met le mot en vert. « num » = numéro dans une pastille (1, 2, 3...). Pas de son : une piste silencieuse est ajoutée.
Identité mode.parano : fond #070D0A, texte #F5F7F6, vert #00C46A, Poppins Bold + Inter Regular.
Zones de sécurité Shorts : texte entre y=330 et y=1380, marges de 90 px (l'interface YouTube couvre le bas et la droite).
"""
import json, re, subprocess, sys, pathlib
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
BG = (7, 13, 10); WH = (245, 247, 246); GR = (0, 196, 106); GY = (130, 140, 135)
B = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
R = "/usr/share/fonts/opentype/inter/Inter-Regular.otf"
F_MAIN = ImageFont.truetype(B, 88); F_KICK = ImageFont.truetype(B, 38)
F_SUB = ImageFont.truetype(R, 52); F_NUM = ImageFont.truetype(B, 64); F_BRAND = ImageFont.truetype(R, 36)

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

def base_frame():
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    w = d.textlength("@mode.parano", font=F_BRAND)
    d.text(((W - w) / 2, 1450), "@mode.parano", font=F_BRAND, fill=GY)
    return im

def main(dossier):
    dossier = pathlib.Path(dossier)
    spec = json.loads((dossier / "spec.json").read_text(encoding="utf-8"))
    beats = spec["beats"]
    total = sum(b["duree"] for b in beats)
    layers = [beat_layer(b) for b in beats]
    base = base_frame()
    out = dossier / "short.mp4"; tmp = dossier / "short.tmp.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
           "-vf", "setsar=1,format=yuv420p", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "96k", "-shortest", "-movflags", "+faststart", str(tmp)]
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
        if not cover_done and lt > 0.5:
            frame.convert("RGB").save(dossier / "cover.jpg", quality=92); cover_done = True
        p.stdin.write(frame.tobytes())
    p.stdin.close(); p.wait()
    if p.returncode == 0: tmp.rename(out)
    else: sys.exit("ffmpeg a échoué")
    print(f"OK {out} ({total:.1f} s)")

if __name__ == "__main__":
    main(sys.argv[1])
