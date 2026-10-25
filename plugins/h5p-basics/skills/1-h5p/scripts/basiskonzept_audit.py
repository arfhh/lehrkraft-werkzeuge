#!/usr/bin/env python3
"""Basiskonzepte-Audit: prüft in H5P-Dateien alle Folien mit Basiskonzept-Bild/-Link.
Soll: Link = apps.zum.de/h5p/46325/embed (Buch "Überblick über die Basiskonzepte"),
Bild = Seite aus Import/Basiskonzepte/**.jpg (Abgleich per Bildähnlichkeit).
Aufruf: basiskonzept_audit.py <h5p-Datei oder Ordner> ...
"""
import zipfile,glob,os,sys,json,re,io
from PIL import Image
ROOT=os.path.expanduser('~/mnt/Unterrichtsmaterial/')
NEW='apps.zum.de/h5p/46325/embed'
_ref={}
def refs():
    if not _ref:
        for p in glob.glob(ROOT+'Import/Basiskonzepte/**/*.jpg',recursive=True):
            _ref[p.split('Basiskonzepte/')[1]]=list(Image.open(p).convert('RGB').resize((64,32)).getdata())
    return _ref
def near(d):
    px=list(Image.open(io.BytesIO(d)).convert('RGB').resize((64,32)).getdata())
    return sorted((round(sum(abs(a-b) for x,y in zip(px,v) for a,b in zip(x,y))/len(px)/3,1),k) for k,v in refs().items())[0]
def slides(o,path=()):
    if isinstance(o,dict):
        if 'elements' in o and isinstance(o['elements'],list) and 'slideBackgroundSelector' in o: yield path,o
        for k,v in o.items(): yield from slides(v,path+(k,))
    elif isinstance(o,list):
        for i,v in enumerate(o): yield from slides(v,path+(i,))
def audit(f):
    z=zipfile.ZipFile(f); c=json.loads(z.read('content/content.json')); res=[]
    for path,s in slides(c):
        link=img=None
        for e in s['elements']:
            a=e.get('action',{}); lib=a.get('library',''); p=a.get('params',{})
            if lib.startswith('H5P.Link'):
                u=(p.get('linkWidget') or {}).get('url','')
                if re.search(r'zum\.de/h5p/(30866|46325)',u) or re.search('konzept',p.get('title',''),re.I): link=(p.get('title'),u)
            if lib.startswith('H5P.Image '):
                t=(a.get('metadata',{}).get('title','')+p.get('alt',''))
                if re.search('konzept',t,re.I) or re.search('konzept',s.get('keywords',[{}])[0].get('main','') if s.get('keywords') else '',re.I):
                    try: img=(a['metadata'].get('title'),p['file']['path'],near(z.read('content/'+p['file']['path'])))
                    except Exception as ex: img=(str(ex),)
        if link:
            ok_l=link[1].rstrip('/')==NEW
            res.append((path,(s.get('keywords') or [{}])[0].get('main',''),link,img,ok_l))
    return res
if __name__=='__main__':
    fs=[]
    for a in sys.argv[1:]:
        fs+= glob.glob(a+'/**/*.h5p',recursive=True) if os.path.isdir(a) else [a]
    for f in sorted(fs):
        for path,kw,link,img,ok in audit(f):
            print(('OK  ' if ok else 'FEHLER'),os.path.basename(f),'| Folie:',kw,'| Link:',link[1],'| Bild:',img[1:] if img else None)
