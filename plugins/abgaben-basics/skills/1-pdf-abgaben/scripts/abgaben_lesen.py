#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Liest einen Satz gleichartiger PDF-Abgaben tokensparsam aus.

(c) 2026 A. Spielhoff - lizenziert unter CC BY 4.0

Erwartet eine Ordnerstruktur <wurzel>/<person>/<datei>.pdf und gibt je Person
den eigenen Anteil aus: Seitentext, Formularfeldwerte und Anmerkungstexte,
abzueglich des gedruckten Vordrucks. Zusaetzlich je Datei eine Pruefsumme.

Braucht nur poppler-utils (pdftotext, pdftoppm) und qpdf - keine Python-Pakete.

  python3 abgaben_lesen.py <wurzel>              Text je Person
  python3 abgaben_lesen.py <wurzel> --json       Maschinenlesbar
  python3 abgaben_lesen.py <wurzel> --leer       Nur: was ist unbearbeitet
  python3 abgaben_lesen.py <wurzel> --dubletten  Gleiche Inhalte finden
"""
import subprocess, json, sys, os, glob, re, collections, hashlib, tempfile, difflib
import statistics, unicodedata

def seitentext(f):
    return subprocess.run(['pdftotext', '-q', f, '-'],
                          capture_output=True, text=True).stdout

def _qpdf(f, key):
    try:
        return json.loads(subprocess.run(['qpdf', '--json', '--json-key=' + key, f],
                                         capture_output=True, text=True).stdout)
    except Exception:
        return {}

def formularfelder(f):
    j = _qpdf(f, 'acroform')
    out = []
    for x in j.get('acroform', {}).get('fields', []):
        v = (x.get('value') or '').strip()
        if v:
            out.append(v)
    return out

def anmerkungen(f):
    j = _qpdf(f, 'objects')
    out = []
    for o in j.get('objects', {}).values():
        if isinstance(o, dict) and o.get('/Type') == '/Annot' and o.get('/Subtype') == '/FreeText':
            c = o.get('/Contents')
            if isinstance(c, str) and c.strip():
                out.append(c.strip())
    return out

def pruefsumme(f):
    h = hashlib.sha256()
    with open(f, 'rb') as fh:
        for b in iter(lambda: fh.read(65536), b''):
            h.update(b)
    return h.hexdigest()

def norm(s):
    return re.sub(r'\s+', ' ', s).strip()

def namensschluessel(dateiname):
    """Wortmenge eines Dateinamens, fuer den Abgleich mit einer Loesungsdatei.

    WICHTIG: zuerst nach NFC normalisieren. macOS legt Dateinamen in NFD ab
    (o + kombinierendes Trema), dann greift eine Umlaut-Ersetzung nicht und
    der Abgleich schlaegt still fehl.
    """
    s = unicodedata.normalize('NFC', os.path.splitext(dateiname)[0]).lower()
    for a, b in (('ae', 'ae'), ('oe', 'oe')):
        pass
    s = s.replace('ae', 'ae')
    s = s.replace('\u00e4', 'ae').replace('\u00f6', 'oe').replace('\u00fc', 'ue').replace('\u00df', 'ss')
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    aus = {'loesung', 'aufgabe', 'speichern', 'kopie', 'final'}
    return {t for t in re.split(r'[^a-z]+', s) if len(t) > 3 and t not in aus}

def kurzantwort_blatt(werte, schwelle=25):
    """True, wenn die Einzelantworten dieses Blattes kurz sind.

    Luecken-, Rechen- und Zuordnungsaufgaben haben genau eine richtige
    Antwort je Feld. Dort sind alle richtigen Abgaben zwangslaeufig sehr
    aehnlich - eine Aehnlichkeitspruefung erzeugt dort nur Fehlalarme und
    wird deshalb ausgesetzt. Gemessen an echten Saetzen: Lueckentext Median
    6 bis 12 Zeichen, Freitextaufgabe Median 140 bis 365.
    """
    laengen = [len(x) for x in werte if x]
    return bool(laengen) and statistics.median(laengen) < schwelle

def tintenanteil(f, seite):
    """Anteil dunkler Pixel im mittleren Bereich einer Seite, in Prozent.

    Damit laesst sich eine Zeichenaufgabe ohne Bildansicht auf 'unbearbeitet'
    pruefen: das leere Formular liefert einen festen Grundwert, jede
    Bearbeitung liegt deutlich darueber.
    """
    d = tempfile.mkdtemp()
    subprocess.run(['pdftoppm', '-gray', '-r', '40', '-f', str(seite), '-l', str(seite),
                    f, os.path.join(d, 's')], capture_output=True)
    treffer = glob.glob(os.path.join(d, 's*.pgm'))
    if not treffer:
        return None
    raw = open(treffer[0], 'rb').read()
    kopf, i = [], 2
    while len(kopf) < 3 and i < len(raw):
        j = raw.index(b'\n', i)
        kopf += [int(x) for x in raw[i:j].split()]
        i = j + 1
    w, h = kopf[0], kopf[1]
    px = raw[i:i + w * h]
    y0, y1 = int(h * 0.15), int(h * 0.78)
    x0, x1 = int(w * 0.08), int(w * 0.95)
    dunkel = gesamt = 0
    for y in range(y0, y1):
        zeile = px[y * w:(y + 1) * w]
        for x in range(x0, x1, 2):
            gesamt += 1
            if zeile[x] < 200:
                dunkel += 1
    return 100.0 * dunkel / max(gesamt, 1)

def blattname(dateiname):
    """Haengt der Browser oder das Betriebssystem beim zweiten Herunterladen ein
    " 2", " 3" an den Namen, ist es trotzdem DASSELBE Arbeitsblatt. Ohne diese
    Entdoppelung landen die Abgaben in verschiedenen Gruppen und ein Duplikat
    bleibt unentdeckt - belegt an einem echten Satz: zwei wortgleiche Abgaben
    wurden nicht gemeldet, weil eine " 2" im Namen trug.
    """
    stamm, endung = os.path.splitext(dateiname)
    return re.sub(r'[ _-]\d{1,2}$', '', stamm).strip() + endung


def einlesen(wurzel):
    docs = {}
    for f in sorted(glob.glob(os.path.join(wurzel, '*', '*.pdf'))):
        person = os.path.basename(os.path.dirname(f))
        blatt = blattname(os.path.basename(f))
        docs.setdefault(person, {})[blatt] = {
            'pfad': f,
            'seite': seitentext(f),
            'felder': formularfelder(f),
            'anmerkungen': anmerkungen(f),
            'pruefsumme': pruefsumme(f),
        }
    return docs

def vordruck(docs, mindestens=3, anteil=0.5):
    """Zeilen, die bei mindestens der Haelfte der Abgaben desselben Blattes
    wortgleich vorkommen, sind der gedruckte Rahmen."""
    proBlatt = collections.defaultdict(dict)
    for person, m in docs.items():
        for blatt, d in m.items():
            proBlatt[blatt][person] = d['seite']
    vd = {}
    for blatt, m in proBlatt.items():
        z = collections.Counter()
        for t in m.values():
            for x in {y.strip() for y in t.splitlines() if y.strip()}:
                z[x] += 1
        vd[blatt] = {x for x, n in z.items()
                     if len(m) >= mindestens and n >= len(m) * anteil} if len(m) >= mindestens else set()
    return vd

def eigenanteil(d, vd_blatt):
    eig = [x.strip() for x in d['seite'].splitlines()
           if x.strip() and x.strip() not in vd_blatt]
    gesehen = {norm(x).lower() for x in eig}
    extra = [a for a in d['anmerkungen'] if norm(a).lower() not in gesehen]
    return d['felder'], eig, extra

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    wurzel = sys.argv[1]
    flags = set(sys.argv[2:])
    docs = einlesen(wurzel)
    vd = vordruck(docs)

    if '--dubletten' in flags:
        # Blaetter mit kurzen Einzelantworten von der Aehnlichkeitspruefung ausnehmen.
        proBlattFelder = collections.defaultdict(list)
        for person, m in docs.items():
            for blatt, d in m.items():
                proBlattFelder[blatt].extend(d['felder'])
        ausgenommen = {b for b, w in proBlattFelder.items() if kurzantwort_blatt(w)}
        if ausgenommen:
            print('Von der Aehnlichkeitspruefung ausgenommen (kurze Einzelantworten,')
            print('dort ist hohe Aehnlichkeit fachlich erwartbar):')
            for b in sorted(ausgenommen):
                print('  ' + b)
            print('')

        texte = {}
        for person, m in docs.items():
            for blatt, d in m.items():
                fe, eig, ex = eigenanteil(d, vd.get(blatt, set()))
                texte[(person, blatt)] = norm(' '.join(fe + eig + ex)).lower()
        nachHash = collections.defaultdict(list)
        for (p, b), t in texte.items():
            if len(t) >= 80 and b not in ausgenommen:
                nachHash[(b, hashlib.sha256(t.encode()).hexdigest())].append(p)
        print('Identische Inhalte:')
        gab = False
        for (b, _), ps in nachHash.items():
            if len(ps) > 1:
                print('  %s -> %s' % (b, ', '.join(sorted(ps)))); gab = True
        if not gab:
            print('  keine')
        print('\nAehnlichkeit ab 70 Prozent (Graubereich, inhaltlich beurteilen):')
        gab = False
        proBlatt = collections.defaultdict(dict)
        for (p, b), t in texte.items():
            if b not in ausgenommen:
                proBlatt[b][p] = t
        for b, m in proBlatt.items():
            ps = sorted(m)
            for i in range(len(ps)):
                for j in range(i + 1, len(ps)):
                    a, c = m[ps[i]], m[ps[j]]
                    if len(a) < 120 or len(c) < 120:
                        continue
                    r = difflib.SequenceMatcher(None, a, c).ratio()
                    if r >= 0.70:
                        print('  %s  %s <-> %s  %.1f%%' % (b, ps[i], ps[j], r * 100)); gab = True
        if not gab:
            print('  keine')
        return

    if '--leer' in flags:
        print('Ohne jeden Text (Zeichnung oder Scan - Bildansicht noetig):')
        for person in sorted(docs):
            for blatt, d in sorted(docs[person].items()):
                if not d['felder'] and not d['anmerkungen'] and len(norm(d['seite'])) < 900:
                    print('  %s/%s' % (person, blatt))
        return

    ergebnis = {}
    for person in sorted(docs):
        ergebnis[person] = {}
        for blatt, d in sorted(docs[person].items()):
            fe, eig, ex = eigenanteil(d, vd.get(blatt, set()))
            ergebnis[person][blatt] = {
                'felder': fe, 'text': eig, 'anmerkungen': ex,
                'pruefsumme': d['pruefsumme'][:16],
            }

    if '--json' in flags:
        print(json.dumps(ergebnis, ensure_ascii=False, indent=1))
        return

    for person, m in ergebnis.items():
        print('\n##### %s' % person)
        for blatt, d in m.items():
            print('- %s' % blatt)
            if d['felder']:
                print('  FELDER: ' + ' | '.join(d['felder']))
            if d['text']:
                print('  TEXT: ' + ' / '.join(d['text']))
            if d['anmerkungen']:
                print('  ANMERK: ' + ' | '.join(norm(x) for x in d['anmerkungen']))
            if not d['felder'] and not d['text'] and not d['anmerkungen']:
                print('  (kein Text - Zeichnung oder Scan)')

if __name__ == '__main__':
    main()
