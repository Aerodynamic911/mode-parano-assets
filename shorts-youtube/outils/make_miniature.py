#!/usr/bin/env python3
"""Miniature verticale 1080x1920 d'un Short : python3 make_miniature.py <dossier> "<kicker>" "<ligne1>" "<ligne2>" ["<sous-titre>"]
« *mot* » = mot en vert. Écrit <dossier>/miniature.jpg (moins de 2 Mo). Identité : #070D0A / #F5F7F6 / #00C46A, Poppins Bold + Inter."""
import sys, re, os
from PIL import Image, ImageDraw, ImageFont
BG,FG,GR=(7,13,10),(245,247,246),(0,196,106)
PB="/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"; IN="/usr/share/fonts/opentype/inter/Inter-Regular.otf"
def parts(s): return [(p.strip("*"),p.startswith("*")) for p in re.findall(r"\*[^*]+\*|[^*]+",s)]
def width(d,ps,f): return sum(d.textlength(t,font=f) for t,_ in ps)
def line(d,ps,f,y):
    x=(1080-width(d,ps,f))/2
    for t,g in ps:
        d.text((x,y),t,font=f,fill=GR if g else FG); x+=d.textlength(t,font=f)
def main(dossier,kicker,lines,sub=None):
    im=Image.new("RGB",(1080,1920),BG); d=ImageDraw.Draw(im)
    size=150
    while size>70:
        f=ImageFont.truetype(PB,size)
        if all(width(d,parts(l),f)<=900 for l in lines): break
        size-=4
    f=ImageFont.truetype(PB,size); lh=int(size*1.25)
    total=lh*len(lines); y0=960-total//2-40
    k=ImageFont.truetype(PB,54); kw=d.textlength(kicker,font=k)
    d.rounded_rectangle((540-kw/2-36,y0-170,540+kw/2+36,y0-70),radius=50,outline=GR,width=5)
    d.text((540-kw/2,y0-160),kicker,font=k,fill=GR)
    for i,l in enumerate(lines): line(d,parts(l),f,y0+i*lh)
    yb=y0+total+40
    d.rounded_rectangle((440,yb,640,yb+12),radius=6,fill=GR)
    if sub:
        s=ImageFont.truetype(IN,58); sw=d.textlength(sub,font=s); d.text((540-sw/2,yb+60),sub,font=s,fill=(190,200,195))
    b=ImageFont.truetype(PB,46); bw=d.textlength("@mode.parano",font=b); d.text((540-bw/2,1500),"@mode.parano",font=b,fill=(120,135,128))
    out=os.path.join(dossier,"miniature.jpg"); im.save(out,quality=92); print(out,os.path.getsize(out)//1024,"Ko")
if __name__=="__main__":
    a=sys.argv; main(a[1],a[2],[x for x in a[3:5]],a[5] if len(a)>5 else None)
