#!/usr/bin/env python3
"""Ajoute un passage de musique de Solauw Sound (et le clin d'œil « ♪ Solauw Sound · Titre ») à une vidéo verticale DÉJÀ faite.

Usage : python3 ajoute_musique.py <video-entree.mp4> <video-sortie.mp4> [Titre|auto]
  Titre : Liftoff, Overload, Eclipse, Friction, Apogee ou Flow (défaut : auto = choix stable selon le nom du fichier d'entrée).
Pour une vidéo neuve fabriquée par make_short.py, ne pas utiliser cet outil : la musique est déjà intégrée (clé « musique » du spec.json).

Ce que fait l'outil : remplace la piste son (même passage et même niveau que make_short.py : -18 LUFS, fondu d'entrée 0,3 s,
fondu de sortie 1,3 s), dessine le crédit en bas de l'image (même place que make_short.py, au-dessus de « @mode.parano »),
ré-encode l'image en H.264. La vidéo ne doit pas dépasser 27 s.
"""
import subprocess, sys, pathlib, zlib, tempfile
from PIL import Image, ImageDraw
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import make_short as ms


def infos(chemin):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:format=duration",
                        "-of", "default=nw=1:nk=1", str(chemin)], capture_output=True, text=True, check=True).stdout.split()
    return int(r[0]), int(r[1]), float(r[2])


def main(entree, sortie, titre="auto"):
    entree, sortie = pathlib.Path(entree), pathlib.Path(sortie)
    liste = sorted(ms.morceaux())
    if titre == "auto":
        titre = liste[zlib.crc32(entree.stem.encode()) % len(liste)]
    if titre not in liste:
        sys.exit(f"Morceau inconnu : {titre} (choix : {', '.join(liste)})")
    w, h, duree = infos(entree)
    info = ms.morceaux()[titre]
    if duree > info["duree_s"] - 0.5:
        sys.exit(f"Vidéo de {duree:.1f} s : passage de {titre} trop court ({info['duree_s']} s)")
    # calque du crédit, dessiné en 1080x1920 puis mis à l'échelle de la vidéo
    calque = Image.new("RGBA", (ms.W, ms.H), (0, 0, 0, 0)); d = ImageDraw.Draw(calque)
    t = ms.credit_texte(titre); largeur = d.textlength(t, font=ms.F_CREDIT); ic, gap = 30, 12
    x0 = (ms.W - (ic + gap + largeur)) / 2
    ms.dessine_note(d, x0, 1399, ic, ms.GR_DISCRET)
    d.text((x0 + ic + gap, 1398), t, font=ms.F_CREDIT, fill=ms.GR_DISCRET)
    if (w, h) != (ms.W, ms.H):
        calque = calque.resize((w, h), Image.LANCZOS)
    tmp_png = pathlib.Path(tempfile.mkdtemp()) / "credit.png"; calque.save(tmp_png)
    tmp = sortie.with_suffix(".tmp.mp4")
    af = f"afade=t=in:st=0:d={ms.FONDU_ENTREE},afade=t=out:st={duree - ms.FONDU_SORTIE:.2f}:d={ms.FONDU_SORTIE}"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(entree), "-i", str(ms.MUSIQUE_DIR / info["fichier"]), "-i", str(tmp_png),
           "-filter_complex", f"[0:v][2:v]overlay=0:0,format=yuv420p[v];[1:a]{af}[a]", "-map", "[v]", "-map", "[a]",
           "-t", f"{duree:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-movflags", "+faststart", str(tmp)]
    subprocess.run(cmd, check=True)
    tmp.rename(sortie)
    print(f"OK {sortie} ({duree:.1f} s, musique : {titre})")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "auto")
