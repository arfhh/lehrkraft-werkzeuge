#!/usr/bin/env python3
"""Basiskonzept-Folien in H5P-Büchern setzen oder neu einfügen.

  fix    <in> <out> <Seite> <alt> [mp3]   vorhandene Basiskonzept-Folie auf neue Buchseite umstellen
         (Umgebungsvariable BK_TEXT_WEG=1: Textkasten der Folie entfernen, Vollbild setzen)
  insert <in> <out> <Seite> <alt> <nach-Folie> [mp3] [kapitel=0]
         neue Basiskonzept-Folie hinter Folie <nach-Folie> der Kurspräsentation einfügen
  version <in>                              nur "Version: TT.MM.JJ" auf das Datum im Dateinamen setzen (in place)

<Seite> = Pfad relativ zu Import/Basiskonzepte ohne .jpg (MP3 gleichen Namens, sonst [mp3] angeben).
Buch-Link: apps.zum.de/h5p/46325/embed. Muster wie 5.1.1: Bild Vollbild, Audio x87.9/y3.1, Link x94.2/y3.7.
Setzt immer die Version auf das Datum im Ausgabe-Dateinamen. Löst am Ende testzip() aus.
"""
import zipfile, json, os, sys, re, uuid, io
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
import basiskonzept_audit as A
BK = A.ROOT + 'Import/Basiskonzepte/'
BOOK = 'https://apps.zum.de/apps/46325'

def date_of(name):
    m = re.findall(r'(\d\d\.\d\d\.\d\d)(?!\d)', name)
    return m[-1] if m else None

def set_version(c, d):
    n = 0
    def w(o):
        nonlocal n
        if isinstance(o, dict):
            for k, v in o.items():
                if isinstance(v, str) and 'Version' in v:
                    nv = re.sub(r'(Version:?\s*(?:</?[^>]+>\s*)*)\d\d\.\d\d\.\d{2,4}', lambda m: m.group(1) + d, v)
                    if nv != v: o[k] = nv; n += 1
                else: w(v)
        elif isinstance(o, list):
            for v in o: w(v)
    w(c); return n

def audio_el(apath):
    return {'x': 87.91208791208791, 'y': 3.1010756856284525, 'width': 5.038734243697479, 'height': 9.95331344832058,
            'action': {'library': 'H5P.Audio 1.5', 'params': {'fitToWrapper': True, 'playerMode': 'minimalistic', 'controls': True, 'autoplay': False,
                'playAudio': 'Audio abspielen', 'pauseAudio': 'Audio pausieren', 'contentName': 'Audio',
                'audioNotSupported': 'Dein Browser unterstützt diese Tondatei nicht.',
                'files': [{'path': apath, 'mime': 'audio/mpeg', 'copyright': {'license': 'U'}}]},
                'metadata': {'contentType': 'Audio', 'license': 'CC0 1.0', 'title': 'Vorlesetext: Basiskonzept der Chemie',
                    'authors': [{'name': 'A.Spielhoff', 'role': 'Author'}, {'name': 'https://aistudio.google.com/generate-speech', 'role': 'Licensee'}],
                    'source': 'https://aistudio.google.com/generate-speech'}, 'subContentId': str(uuid.uuid4())},
            'alwaysDisplayComments': False, 'backgroundOpacity': 0, 'displayAsButton': False, 'buttonSize': 'big', 'goToSlideType': 'specified', 'invisible': False, 'solution': ''}

def image_el(ipath, im, alt, title):
    return {'x': 0, 'y': 0, 'width': 99.9994683513303, 'height': 99.94964861619766,
            'action': {'library': 'H5P.Image 1.1', 'params': {'decorative': False, 'contentName': 'Bild', 'expandImage': 'Bild vergrößern', 'minimizeImage': 'Bild verkleinern',
                'file': {'path': ipath, 'mime': 'image/jpeg', 'copyright': {'license': 'U'}, 'width': im.size[0], 'height': im.size[1]}, 'alt': alt},
                'metadata': {'contentType': 'Image', 'license': 'CC BY', 'title': title, 'authors': [{'name': 'A.Spielhoff', 'role': 'Author'}],
                    'licenseVersion': '4.0', 'source': BOOK}, 'subContentId': str(uuid.uuid4())},
            'alwaysDisplayComments': False, 'backgroundOpacity': 0, 'displayAsButton': False, 'buttonSize': 'big', 'goToSlideType': 'specified', 'invisible': False, 'solution': ''}

def link_el():
    return {'x': 94.19152276295134, 'y': 3.721290822754143, 'width': 40, 'height': 40,
            'action': {'library': 'H5P.Link 1.3', 'params': {'linkWidget': {'protocol': 'https://', 'url': 'apps.zum.de/h5p/46325/embed'}, 'title': 'Überblick über die Basiskonzepte der Chemie'},
                'metadata': {'contentType': 'Link', 'license': 'U', 'title': 'Link: Basiskonzepte der Chemie'}, 'subContentId': str(uuid.uuid4())},
            'alwaysDisplayComments': False, 'backgroundOpacity': 0, 'displayAsButton': True, 'buttonSize': 'big', 'goToSlideType': 'specified', 'invisible': False, 'solution': ''}

def media(page, mp3name):
    jpg = open(BK + page + '.jpg', 'rb').read()
    mp = BK + (mp3name or page + '.mp3')
    mp3 = open(mp, 'rb').read() if os.path.exists(mp) else None
    if mp3 is None: print('WARNUNG: keine MP3 gefunden', mp)
    return jpg, mp3, Image.open(io.BytesIO(jpg))

def write(zin, dst, c, extra):
    txt = json.dumps(c, ensure_ascii=False)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zo:
        for it in zin.infolist():
            if it.is_dir(): continue
            if it.filename == 'content/content.json': zo.writestr(it.filename, txt); continue
            if it.filename.startswith(('content/images/', 'content/audios/')) and it.filename.split('content/', 1)[1] not in txt: continue  # verwaist
            zo.writestr(it.filename, zin.read(it.filename))
        for k, v in extra.items(): zo.writestr('content/' + k, v)
    assert zipfile.ZipFile(io.BytesIO(buf.getvalue())).testzip() is None
    open(dst, 'wb').write(buf.getvalue())  # Überschreiben erlaubt, Löschen nicht

def finish(zin, dst, c, extra):
    d = date_of(os.path.basename(dst))
    v = set_version(c, d) if d else 0
    write(zin, dst, c, extra)
    z = zipfile.ZipFile(dst); assert z.testzip() is None; json.loads(z.read('content/content.json'))
    print('OK', os.path.basename(dst), '| Version-Treffer:', v)

def fix(src, dst, page, alt, mp3name=None):
    zin = zipfile.ZipFile(src); c = json.loads(zin.read('content/content.json'))
    jpg, mp3, im = media(page, mp3name); tag = uuid.uuid4().hex[:13]
    ipath = f'images/file-{tag}.jpg'; apath = f'audios/files-{tag}.mp3'
    title = 'Basiskonzept der Chemie: ' + os.path.basename(page).strip(); n = 0
    for path, s in A.slides(c):
        els = s['elements']; li = None; ii = None
        for i, e in enumerate(els):
            if e['action']['library'].startswith('H5P.Link') and re.search(r'zum\.de/h5p/(30866|46325)', (e['action']['params'].get('linkWidget') or {}).get('url', '')): li = i
        if li is None: continue
        if os.environ.get('BK_TEXT_WEG'): els[:] = [x for x in els if not x['action']['library'].startswith('H5P.AdvancedText')]
        for i, e in enumerate(els):
            if e['action']['library'].startswith('H5P.Image ') and e['width'] > 60 and (e['x'] < 1 or os.environ.get('BK_TEXT_WEG')): ii = i
        if ii is None: print('kein Bild in', path); continue
        els[:] = [x for x in els if not x['action']['library'].startswith(('H5P.Link', 'H5P.Audio'))] if mp3 else [x for x in els if not x['action']['library'].startswith('H5P.Link')]
        ii = [k for k, x in enumerate(els) if x['action']['library'].startswith('H5P.Image ') and x['width'] > 60][0]
        new = image_el(ipath, im, alt, title); old = els[ii]
        new['subContentId'] = old['action'].get('subContentId', new['action']['subContentId']) if False else new['action']['subContentId']
        els[ii] = new; els.append(link_el())
        if mp3: els.append(audio_el(apath))
        n += 1
    assert n == 1, f'{n} Basiskonzept-Folien gefunden'
    ex = {ipath: jpg}
    if mp3: ex[apath] = mp3
    finish(zin, dst, c, ex)

def find_cp(c, kapitel):
    for path, s in A.slides(c['chapters'][kapitel]): pass
    sl = None
    def w(o):
        nonlocal sl
        if isinstance(o, dict):
            if 'presentation' in o and 'slides' in o['presentation'] and sl is None: sl = o['presentation']['slides']
            for v in o.values(): w(v)
        elif isinstance(o, list):
            for v in o: w(v)
    w(c['chapters'][kapitel]); return sl

def insert(src, dst, page, alt, after, mp3name=None, kapitel=0):
    after = int(after); kapitel = int(kapitel)
    zin = zipfile.ZipFile(src); c = json.loads(zin.read('content/content.json'))
    jpg, mp3, im = media(page, mp3name); tag = uuid.uuid4().hex[:13]
    ipath = f'images/file-{tag}.jpg'; apath = f'audios/files-{tag}.mp3'
    title = 'Basiskonzept der Chemie: ' + os.path.basename(page).strip()
    slides = find_cp(c, kapitel)
    els = [image_el(ipath, im, alt, title), link_el()]
    if mp3: els.append(audio_el(apath))
    slides.insert(after + 1, {'elements': els, 'slideBackgroundSelector': {}, 'keywords': [{'main': 'Basiskonzept'}]})
    shifted = 0
    for i, s in enumerate(slides):
        for e in s['elements']:
            g = e.get('goToSlide')
            if isinstance(g, int) and g > after + 1 and i != after + 1: e['goToSlide'] = g + 1; shifted += 1
    ex = {ipath: jpg}
    if mp3: ex[apath] = mp3
    finish(zin, dst, c, ex)
    print('Folie eingefügt als Nr.', after + 1, '| goToSlide verschoben:', shifted)

def version_only(src):
    zin = zipfile.ZipFile(src); c = json.loads(zin.read('content/content.json'))
    finish(zin, src, c, {})

if __name__ == '__main__':
    m, a = sys.argv[1], sys.argv[2:]
    {'fix': fix, 'insert': insert, 'version': version_only}[m](*a)
