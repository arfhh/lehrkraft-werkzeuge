#!/usr/bin/env python3
"""piepton_splice.py — ersetzt in einer Vorlese-Aufnahme jedes gesprochene Wort
"Lücke" durch einen Piepton (Lückentext-Audio, siehe medien.md, Abschnitt
"Lückentexte vorlesen: Piepton-Splice").

    python3 piepton_splice.py EINGABE.mp3 ERWARTETE_LUECKEN AUSGABE.mp3 [--wort Lücke]

Benötigt: ffmpeg, numpy, `pip install sherpa-onnx --break-system-packages`
und ein deutsches CTC-Modell (Wort-Zeitstempel, kein vosk nötig):
    sherpa-onnx-nemo-fast-conformer-ctc-en-de-es-fr-14288-int8
    (GitHub-Release "asr-models" von k2-fsa/sherpa-onnx; huggingface ist gesperrt,
     github.com/…/releases/download/… ist erreichbar)
Modellordner: Umgebungsvariable PIEP_MODELL oder ~/w/asr/sherpa-onnx-nemo-*.
Der Piepton liegt neben dem Skript (beep-880hz-0.8s.mp3).

Ablauf: 16-kHz-Kopie erkennen -> Token-Zeitstempel -> Token-Folge "L ü ck e"
suchen -> Schnittpunkte am Energieminimum -> Segmente + Piepton per ffmpeg
concat. Bei abweichender Trefferzahl wird NICHT geschnitten (Exit 2).
Danach Gegenprobe: die Ausgabe wird erneut erkannt, "Lücke" darf nicht mehr
vorkommen. Ausgabetext wird zum Gegenlesen gedruckt.
"""
import argparse, glob, os, subprocess, sys, tempfile, wave
from pathlib import Path
import numpy as np

HIER = Path(__file__).resolve().parent
VOR = float(os.environ.get('PIEP_VOR','0.24'))     # wie weit vor dem Wortanfang nach dem Schnittpunkt gesucht wird
NACH = float(os.environ.get('PIEP_NACH','0.45'))   # wie weit nach dem Wortende

def modell():
    d = os.environ.get('PIEP_MODELL')
    if not d:
        c = glob.glob(os.path.expanduser('~/w/asr/sherpa-onnx-nemo-*'))
        d = c[0] if c else None
    if not d: sys.exit('Modell nicht gefunden (PIEP_MODELL setzen)')
    return d

def laden(pfad):
    with tempfile.TemporaryDirectory() as t:
        w = Path(t)/'x.wav'
        subprocess.run(['ffmpeg','-y','-loglevel','error','-i',pfad,'-ar','16000','-ac','1',str(w)],check=True)
        f = wave.open(str(w))
        return np.frombuffer(f.readframes(f.getnframes()),dtype=np.int16).astype(np.float32)/32768

_REC = None
def erkennen(x):
    global _REC
    import sherpa_onnx
    if _REC is None:
        d = modell()
        _REC = sherpa_onnx.OfflineRecognizer.from_nemo_ctc(model=d+'/model.int8.onnx',tokens=d+'/tokens.txt',num_threads=4)
    r = _REC
    s = r.create_stream(); s.accept_waveform(16000,x); r.decode_stream(s)
    return s.result

def suche(res, wort):
    """Liefert (start_token_idx, end_token_idx) je Treffer; Token-Text zusammensetzen."""
    toks = res.tokens
    treffer = []
    ziel = wort.lower()
    i = 0
    while i < len(toks):
        if toks[i].startswith(' ') and toks[i].strip():
            acc = ''
            for j in range(i, min(i+8, len(toks))):
                if j > i and toks[j].startswith(' '): break
                acc += toks[j].strip()
                if acc.lower() == ziel:
                    treffer.append((i, j)); i = j; break
        i += 1
    return treffer

def energie(x, sr=16000, hop=160):
    n = len(x)//hop
    return np.sqrt((x[:n*hop].reshape(n,hop)**2).mean(axis=1))

def minimum(e, von, bis, sr=16000, hop=160):
    a = max(0,int(von*sr/hop)); b = min(len(e)-1,int(bis*sr/hop))
    if b <= a: return von
    return (a+int(np.argmin(e[a:b+1])))*hop/sr

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('eingabe'); ap.add_argument('erwartet',type=int); ap.add_argument('ausgabe')
    ap.add_argument('--wort',default='Lücke')
    ap.add_argument('--pause',type=float,default=0.45,help='Stille (Sekunden) nach jedem Piepton, damit es nicht gehetzt klingt')
    ap.add_argument('--rand',type=float,default=0.05,help='Schnittende so viel frueher (s), damit der Anfang des Folgeworts (ein) nicht angeschnitten wird')
    ap.add_argument('--rand-start',type=float,default=0.0,help='Schnittanfang so viel spaeter (s); >0 laesst Reste von "Lue" hoerbar')
    ap.add_argument('--stille',action='store_true',help='Testlauf: statt Piepton Stille einsetzen (Gegenprobe ohne Piep-Artefakte)')
    a = ap.parse_args()
    x = laden(a.eingabe); dauer = len(x)/16000
    res = erkennen(x); ts = list(res.timestamps)
    print('Erkannt:', res.text)
    tr = suche(res, a.wort)
    print(f'Treffer: {len(tr)} (erwartet {a.erwartet})')
    if len(tr) != a.erwartet:
        sys.exit(2)
    schnitte = []
    import difflib, re as _re
    # Wortliste mit Startzeiten aus den Token (Token mit führendem Leerzeichen beginnt ein Wort)
    woerter = []   # (text, start)
    for tok, t in zip(res.tokens, ts):
        if tok.startswith(' ') or not woerter:
            woerter.append([tok.strip(), t])
        else:
            woerter[-1][0] += tok
    def norm(txt): return _re.sub(r'[^a-zäöüß ]','',txt.lower()).split()
    wtxt = [norm(w[0])[0] if norm(w[0]) else '' for w in woerter]
    def lokal(s_, en, k_vor, k_nach, t_vor, t_nach):
        teil = np.concatenate([x[int(t_vor*16000):int(s_*16000)], np.zeros(int(0.15*16000),dtype=np.float32), x[int(en*16000):int(t_nach*16000)]])
        return ' '.join(norm(erkennen(teil).text))
    for (i,j) in tr:
        t0 = ts[i]; t1 = ts[j]
        # Index des Wortes "Lücke" in der Wortliste
        k = min(range(len(woerter)), key=lambda q: abs(woerter[q][1]-t0))
        vor = [w for w in wtxt[max(0,k-3):k] if w]
        nach = [w for w in wtxt[k+1:k+4] if w]
        exp = ' '.join(vor + nach)
        t_vor = woerter[max(0,k-len(vor))][1] - 0.10 if vor else max(0.0,t0-0.8)
        t_vor = max(0.0, t_vor)
        t_nach = min(dauer, (woerter[k+len(nach)+1][1] if k+len(nach)+1 < len(woerter) else dauer) + 0.05)
        best = []
        for v in np.arange(t0-0.20, t0+0.11, 0.02):
            for b in np.arange(t1-0.05, t1+0.41, 0.03):
                got = lokal(v, b, 0, 0, t_vor, t_nach)
                sc = difflib.SequenceMatcher(None, exp, got).ratio()
                best.append((sc, float(v), float(b)))
        top = max(b[0] for b in best)
        gute = [b for b in best if b[0] >= top - 1e-9]
        ms = float(np.median([g[1] for g in gute])); me = float(np.median([g[2] for g in gute]))
        # knappster Schnitt unter den gleich guten: schneidet Nachbarwoerter (Und, ein) am wenigsten an
        sc, s_, en = min(gute, key=lambda g: (g[2]-g[1]))
        print(f'  Lücke bei {t0:.2f}s: Score {sc:.2f}, {len(gute)} gleich gute Schnitte, erwartet "{exp}"')
        schnitte.append((s_ + a.rand_start, max(s_ + a.rand_start + 0.1, en - a.rand)))
    print('Schnitte:', [(round(s,2),round(en,2)) for s,en in schnitte])
    with tempfile.TemporaryDirectory() as t:
        t = Path(t); teile = []; pos = 0.0
        beep = HIER/'beep-880hz-0.8s.mp3'
        def seg(von,bis,k):
            p = t/f'{k}.mp3'
            subprocess.run(['ffmpeg','-y','-loglevel','error','-i',a.eingabe,'-ss',f'{von:.3f}','-to',f'{bis:.3f}','-ar','44100','-ac','1','-codec:a','libmp3lame','-qscale:a','2',str(p)],check=True); return p
        k = 0
        for s,en in schnitte:
            teile.append(seg(pos,s,k)); k+=1
            b = t/f'b{k}.mp3'
            if a.stille:
                subprocess.run(['ffmpeg','-y','-loglevel','error','-f','lavfi','-i','anullsrc=r=44100:cl=mono','-t','0.8','-codec:a','libmp3lame','-qscale:a','2',str(b)],check=True)
            else:
                subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(beep),'-ar','44100','-ac','1','-codec:a','libmp3lame','-qscale:a','2',str(b)],check=True)
            teile.append(b); pos = en
            if a.pause > 0:
                p_ = t/f'p{k}.mp3'
                subprocess.run(['ffmpeg','-y','-loglevel','error','-f','lavfi','-i','anullsrc=r=44100:cl=mono','-t',str(a.pause),'-codec:a','libmp3lame','-qscale:a','2',str(p_)],check=True)
                teile.append(p_)
        teile.append(seg(pos,dauer,k+1))
        (t/'liste.txt').write_text(''.join(f"file '{p}'\n" for p in teile))
        subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(t/'liste.txt'),'-codec:a','libmp3lame','-qscale:a','2',a.ausgabe],check=True)
    # Gegenprobe
    r2 = erkennen(laden(a.ausgabe))
    print('Gegenprobe:', r2.text)
    rest = len(suche(r2, a.wort))
    print(f'"{a.wort}" nach dem Schnitt noch {rest}x erkannt')
    sys.exit(0 if rest == 0 else 3)

if __name__ == '__main__':
    main()
