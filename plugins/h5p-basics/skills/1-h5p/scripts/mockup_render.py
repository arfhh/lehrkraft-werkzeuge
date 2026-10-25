#!/usr/bin/env python3
"""Mock-up-Render + Scroll-Check fuer CoursePresentation-Folien.

Aufruf im entpackten Arbeitsverzeichnis `x/` (mit x/content/content.json):
    python3 mockup_render.py
Schriften (Regular/Bold) in ./fonts/ ablegen. Rechnet Folien mit 1000x562 px,
Grundschrift 20 px. Ausgabe je Folie: Index, Titel (keyword), unterste
Textkante in px (offsetTop+scrollHeight). Wert > ca. 545 = Folie wuerde
scrollen -> Text kuerzen / Elemente verschieben. Erzeugt sNN.png/sNN.html.
Voraussetzung: playwright + chromium. Nur Naeherung des Editors.
"""
import json,re,sys,os
from playwright.sync_api import sync_playwright
c=json.load(open('x/content/content.json'))
def slides(o):
    if isinstance(o,dict):
        if 'elements' in o and 'slideBackgroundSelector' in o: yield o
        for v in o.values(): yield from slides(v)
    elif isinstance(o,list):
        for v in o: yield from slides(v)
def el_html(e):
    a=e['action'];lib=a['library'].split()[0];p=a['params']
    st='position:absolute;left:%s%%;top:%s%%;width:%s%%;height:%s%%;box-sizing:border-box;overflow:hidden;'%(e['x'],e['y'],e['width'],e['height'])
    if lib=='H5P.Image':
        return '<img style="%sobject-fit:fill" src="x/content/%s">'%(st,p['file']['path'])
    if lib=='H5P.AdvancedText':
        return '<div style="%s" class=t>%s</div>'%(st+'overflow:visible;',p['text'])
    if lib=='H5P.Blanks':
        t=p['text']+''.join(re.sub(r'\*([^*:/]*)[^*]*\*',lambda m:'<u>&nbsp;%s&nbsp;</u>'%m.group(1),q) for q in p['questions'])
        return '<div style="%soverflow:visible;border:1px dashed #999" class=t>%s</div>'%(st,t)
    return '<div style="%sborder:1px dashed #c00;background:#fee">%s</div>'%(st,lib)
CSS='@font-face{font-family:Nunito;src:url(fonts/Nunito-Regular.ttf)}@font-face{font-family:Nunito;font-weight:700;src:url(fonts/Nunito-Bold.ttf)}body{margin:0;font-family:Nunito;font-size:20px}.t{line-height:1.5}.t p{margin:0 0 .6em}.t ul{margin:0;padding-left:1.4em}'
cwd=os.getcwd()
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1000,'height':562})
    for i,s in enumerate(slides(c)):
        kw=s.get('keywords',[{}])[0].get('main','')
        body=''.join(el_html(e) for e in s['elements'])
        h='<html><head><style>%s</style></head><body><div style="position:relative;width:1000px;height:562px;background:#fff;overflow:hidden">%s</div></body></html>'%(CSS,body)
        f='s%02d.html'%i; open(f,'w').write(h); pg.goto('file://%s/%s'%(cwd,f))
        print(i,kw,pg.evaluate("Math.round(Math.max(0,...[...document.querySelectorAll('.t')].map(e=>(e.offsetTop+e.scrollHeight))))"))
        pg.screenshot(path='s%02d.png'%i,clip={'x':0,'y':0,'width':1000,'height':562})
    b.close()
