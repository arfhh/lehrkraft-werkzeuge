#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Baut aus handschriftlich bearbeiteten Abgaben EINEN Kontaktbogen.

(c) 2026 A. Spielhoff - lizenziert unter CC BY 4.0

Alle Abgaben desselben Formulars werden gerendert, der gedruckte Vordruck
wird abgezogen (er ist bei allen gleich und laesst sich als Medianbild
berechnen), auf den Antwortbereich zugeschnitten und nebeneinander in ein
einziges beschriftetes Bild gesetzt.

Warum: Eine Seite als Bild kostet rund 1900 Token. Fuenfzehn Abgaben einzeln
anzusehen kostet knapp 30000. Derselbe Inhalt als ein Kontaktbogen kostet
rund 2800 - und macht ausserdem sichtbar, was im Einzelblatt nie auffaellt:
zwei Abgaben mit derselben ungewoehnlichen Loesung.

  python3 kontaktbogen.py <wurzel> <dateiname-muster> [-o bogen.png]
       [--dpi 100] [--spalten 3] [--breite 430] [--bereich x0,x1,y0,y1]

  --bereich  Ausschnitt in Pixeln bei der gewaehlten Aufloesung. Ohne Angabe
             wird der Bereich automatisch bestimmt: alles, worin sich
             mindestens zwei Abgaben vom Vordruck unterscheiden.

Braucht poppler-utils (pdftoppm), numpy und Pillow.
"""
import sys, os, glob, subprocess, tempfile, argparse
import numpy as np
from PIL import Image, ImageDraw

def seite(pdf, dpi, ordner, name):
    ziel = os.path.join(ordner, name)
    subprocess.run(['pdftoppm', '-gray', '-r', str(dpi), '-png', '-singlefile',
                    '-f', '1', '-l', '1', pdf, ziel], capture_output=True)
    return ziel + '.png'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('wurzel'); ap.add_argument('muster')
    ap.add_argument('-o', default='kontaktbogen.png')
    ap.add_argument('--dpi', type=int, default=100)
    ap.add_argument('--spalten', type=int, default=3)
    ap.add_argument('--breite', type=int, default=430)
    ap.add_argument('--bereich', default=None)
    ap.add_argument('--schwelle', type=int, default=55)
    a = ap.parse_args()

    dateien = sorted(glob.glob(os.path.join(a.wurzel, '*', a.muster)))
    if not dateien:
        print('Keine Datei passt auf das Muster.'); return
    tmp = tempfile.mkdtemp()
    bilder = {}
    for f in dateien:
        person = os.path.basename(os.path.dirname(f))
        bilder[person] = np.array(Image.open(seite(f, a.dpi, tmp, person)).convert('L'))

    h = min(x.shape[0] for x in bilder.values()); w = min(x.shape[1] for x in bilder.values())
    stapel = np.stack([x[:h, :w] for x in bilder.values()])
    vordruck = np.median(stapel, axis=0).astype('uint8')

    if a.bereich:
        X0, X1, Y0, Y1 = [int(v) for v in a.bereich.split(',')]
    else:
        abw = (np.abs(stapel.astype(int) - vordruck.astype(int)) > a.schwelle).sum(axis=0)
        ys, xs = np.where(abw >= 2)
        if len(xs) == 0:
            print('Keine Abweichung vom Vordruck gefunden - nichts bearbeitet?'); return
        rand = int(a.dpi * 0.05)
        X0, X1 = max(0, xs.min() - rand), min(w, xs.max() + rand)
        Y0, Y1 = max(0, ys.min() - rand), min(h, ys.max() + rand)
    print('Antwortbereich: x %d-%d, y %d-%d' % (X0, X1, Y0, Y1))

    zellen = {}
    for k, bild in bilder.items():
        d = np.abs(bild[:h, :w].astype(int) - vordruck.astype(int))
        tinte = (d > a.schwelle)[Y0:Y1, X0:X1]
        im = Image.fromarray(np.where(tinte, 0, 255).astype('uint8'))
        hoehe = max(1, int(im.size[1] * a.breite / im.size[0]))
        zellen[k] = im.resize((a.breite, hoehe), Image.LANCZOS)

    bw, bh = a.breite, list(zellen.values())[0].size[1]
    besch = 18
    reihen = (len(zellen) + a.spalten - 1) // a.spalten
    bogen = Image.new('L', (a.spalten * bw, reihen * (bh + besch)), 255)
    zeichner = ImageDraw.Draw(bogen)
    for i, k in enumerate(sorted(zellen)):
        sx = (i % a.spalten) * bw; sy = (i // a.spalten) * (bh + besch)
        zeichner.text((4 + sx, sy + 3), k, fill=0)
        bogen.paste(zellen[k], (sx, sy + besch))
        zeichner.rectangle([sx, sy, sx + bw - 1, sy + bh + besch - 1], outline=160)
    bogen.save(a.o)
    tok = bogen.size[0] * bogen.size[1] // 750
    print('%s  %dx%d  ~%d Token  (einzeln waeren es ~%d)'
          % (a.o, bogen.size[0], bogen.size[1], tok, len(zellen) * 1900))

if __name__ == '__main__':
    main()
