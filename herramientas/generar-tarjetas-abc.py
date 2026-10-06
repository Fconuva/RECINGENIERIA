"""Tres alternativas REC, texto vectorial y sangrado de 3 mm.

Ejecutar con py -3.12 -X utf8 herramientas/generar-tarjetas-abc.py.
Los originales del cliente no se modifican ni se publican.
"""
from pathlib import Path
import json
import hashlib
import fitz
import zxingcpp
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'materiales_comerciales/tarjetas-ABC'
MM = 72 / 25.4
NAVY, BLUE, CYAN = '#0C2235', '#123A62', '#78B6D4'
PAPER, WHITE, MUTED, COPPER = '#F7F6F2', '#F8FAFC', '#526574', '#9B5C3E'
URL = 'https://recingenieria.com/'
EMAIL = 'richard.castro@recltda.cl'
PHONE = '+34 611 437 071'
SPECIALTIES = [
    ['Inspección civil de obras (ITO)'],
    ['Geotecnia y mecánica de suelos'],
    ['Memorias de cálculo', 'y análisis estructurales'],
    ['Riego y fertirriego tecnificado'],
    ['Ingeniería con inteligencia artificial'],
]
for name, filename in {
    'OutfitBold': 'Outfit-Bold.ttf', 'Outfit': 'Outfit-Regular.ttf',
    'Instrument': 'InstrumentSans-Regular.ttf',
    'InstrumentBold': 'InstrumentSans-Bold.ttf', 'Mono': 'DMMono-Regular.ttf',
    'Serif': 'DMSerifDisplay-Regular.ttf',
}.items():
    pdfmetrics.registerFont(TTFont(name, str(ROOT / 'materiales_comerciales/fuentes' / filename)))

measurements = []


class Card:
    def __init__(self, letter, title, width=91, height=61):
        self.letter, self.title = letter, title
        self.w, self.h = width, height
        self.path = OUT / f'REC-opcion-{letter}-imprimir.pdf'
        self.c = canvas.Canvas(str(self.path), pagesize=(width*MM, height*MM), pageCompression=1)
        self.c.setAuthor('REC Ingeniería')
        self.c.setCreator('REC Ingeniería')
        self.c.setTitle(f'REC Ingeniería | Opción {letter}: {title}')
        self.c.setSubject(f'Dos caras; corte {width-6} × {height-6} mm; sangrado 3 mm')
        self.face = 0

    def rect(self, x, y, w, h, color):
        self.c.setFillColor(HexColor(color))
        self.c.rect(x*MM, (self.h-y-h)*MM, w*MM, h*MM, fill=1, stroke=0)

    def line(self, x1, y1, x2, y2, color, width=.15):
        self.c.setStrokeColor(HexColor(color))
        self.c.setLineWidth(width*MM)
        self.c.line(x1*MM, (self.h-y1)*MM, x2*MM, (self.h-y2)*MM)

    def text(self, s, x, y, size, font='Instrument', color=NAVY,
             tracking=0, essential=True, align='left'):
        tw = (pdfmetrics.stringWidth(s, font, size) + tracking*(len(s)-1))/MM
        if align == 'right':
            x -= tw
        elif align == 'center':
            x -= tw/2
        assert x >= 7 and x+tw <= self.w-7, (self.letter, s, x, tw)
        assert 8 <= y <= self.h-7, (self.letter, s, y)
        assert not essential or size >= 7, (s, size)
        self.c.setFillColor(HexColor(color))
        obj = self.c.beginText(x*MM, (self.h-y)*MM)
        obj.setFont(font, size)
        obj.setCharSpace(tracking)
        obj.textOut(s)
        self.c.drawText(obj)
        measurements.append({'opcion': self.letter, 'cara': self.face+1,
                             'texto': s, 'x_mm': x, 'y_mm': y,
                             'ancho_mm': tw, 'pt': size})

    def art(self, path, x, y, w, h):
        self.c.saveState()
        clip = self.c.beginPath()
        clip.rect(x*MM, (self.h-y-h)*MM, w*MM, h*MM)
        self.c.clipPath(clip, fill=0, stroke=0)
        with Image.open(path) as im:
            iw, ih = im.size
        ratio = max(w/iw, h/ih)
        aw, ah = iw*ratio, ih*ratio
        self.c.drawImage(str(path), (x+(w-aw)/2)*MM,
                         (self.h-y-h+(h-ah)/2)*MM, aw*MM, ah*MM)
        self.c.restoreState()

    def mark(self, x, y, scale=7, color=BLUE):
        for points, stroke in [
            ([(0,10),(0,2),(7.4,2),(7.4,10)], .042),
            ([(0,4.3),(7.4,4.3)], .042), ([(3.7,4.3),(3.7,10)], .042),
            ([(0,2),(2.2,0),(9.6,0),(9.6,8),(7.4,10)], .027),
            ([(7.4,2),(9.6,0)], .027), ([(7.4,4.3),(9.6,2.3)], .027),
        ]:
            for a,b in zip(points, points[1:]):
                self.line(x+a[0]*scale/10, y+a[1]*scale/10,
                          x+b[0]*scale/10, y+b[1]*scale/10, color, stroke*scale)

    def brand(self, x=8, y=9, color=BLUE):
        self.mark(x, y, 7, color)
        self.text('REC', x+9, y+7, 20, 'OutfitBold', color, tracking=-.4)
        self.text('Ingeniería · REC Ltda.', x+9, y+11, 7, 'Instrument', color)

    def code(self, x, y, size=22):
        assert x >= 7 and y >= 7 and x+size <= self.w-7 and y+size <= self.h-7
        self.rect(x, y, size, size, '#FFFFFF')
        widget = qr.QrCodeWidget(URL, barLevel='M', barBorder=4)
        b = widget.getBounds()
        self.c.saveState()
        self.c.translate(x*MM, (self.h-y-size)*MM)
        scale = size*MM/(b[2]-b[0])
        self.c.scale(scale, scale)
        draw = Drawing(b[2]-b[0], b[3]-b[1]); draw.add(widget)
        renderPDF.draw(draw, self.c, -b[0], -b[1])
        self.c.restoreState()
        self.link(URL, x, y, x+size, y+size)

    def link(self, uri, x1, y1, x2, y2):
        self.c.linkURL(uri, (x1*MM, (self.h-y2)*MM, x2*MM, (self.h-y1)*MM))

    def contacts(self, x, phone_y, email_y, color=BLUE, phone_size=11, email_size=7.7):
        self.text(PHONE, x, phone_y, phone_size, 'InstrumentBold', color)
        self.text(EMAIL, x, email_y, email_size, 'Instrument', color)
        self.link('https://wa.me/34611437071', x, phone_y-4, x+42, phone_y+1)
        self.link('mailto:'+EMAIL, x, email_y-3, x+42, email_y+1)

    def page(self):
        self.c.showPage(); self.face += 1

    def finish(self):
        self.c.save()
        doc = fitz.open(self.path)
        metadata = doc.metadata; metadata['producer'] = 'REC Ingeniería'
        doc.set_metadata(metadata)
        for page in doc:
            page.set_trimbox(fitz.Rect(3*MM, 3*MM, (self.w-3)*MM, (self.h-3)*MM))
            page.set_bleedbox(page.mediabox)
        doc.saveIncr()
        for n, page in enumerate(doc):
            page.get_pixmap(dpi=600, alpha=False).save(OUT / f'opcion-{self.letter}-{["frente","reverso"][n]}.png')
        doc.close()


def specialties(card, starts, color=NAVY, number_color=BLUE, size=8.4, x=15):
    for n, (lines, y) in enumerate(zip(SPECIALTIES, starts), 1):
        card.text(f'{n:02}', 8, y, 7, 'Mono', number_color)
        for j, s in enumerate(lines):
            card.text(s, x, y+j*3.8, size, 'Instrument', color)


# A conserva la dirección visual anterior, con la información original completa.
a = Card('A', 'Materia precisa')
a.art(ROOT/'materiales_comerciales/imagenes/estructura-editorial.png', 0, 0, 91, 61)
a.rect(0, 0, 55.5, 61, NAVY)
a.brand(color=WHITE)
a.text('Richard', 8, 29, 17, 'OutfitBold', WHITE)
a.text('Castro Núñez', 8, 36, 17, 'OutfitBold', WHITE, tracking=-.2)
a.text('Ingeniero Industrial', 8, 41.5, 7.6, color=WHITE)
a.text('Arquitecto Técnico', 8, 45, 7.6, color=WHITE)
a.contacts(8, 50, 54, WHITE, 9.4, 7.2)
a.code(61, 29, 22)
a.rect(59, 51.1, 27, 5.1, NAVY)
a.text('recingenieria.com', 72, 54, 7, 'InstrumentBold', WHITE, align='center')
a.page()
a.rect(0, 0, 91, 61, PAPER)
a.rect(0, 0, 4.5, 61, BLUE)
a.text('NUESTRA', 8, 12, 7, 'Mono', MUTED, tracking=.7)
a.text('Especialización', 8, 19, 16, 'OutfitBold', BLUE)
a.mark(73, 9, 9)
specialties(a, [27, 33.2, 39.4, 48, 54], size=8.4)
a.page(); a.finish()


# B expresa planos técnicos con geometría vectorial original.
b = Card('B', 'Plano técnico')
b.rect(0, 0, 91, 61, PAPER)
b.rect(0, 0, 91, 3.6, BLUE)
b.brand(y=7)
b.text('Richard Castro Núñez', 8, 28, 17, 'OutfitBold', BLUE, tracking=-.3)
b.text('Ingeniero Industrial - Arquitecto Técnico', 8, 34, 7.5, color=MUTED)
b.line(8, 38.5, 52, 38.5, BLUE, .2)
b.contacts(8, 46, 52, BLUE, 11.2, 7.7)
b.code(61, 30, 22)
b.text('recingenieria.com', 72, 54, 7, 'InstrumentBold', BLUE, align='center')
b.page()
b.rect(0, 0, 91, 61, NAVY)
for x in range(3, 92, 4):
    b.line(x, 0, x, 61, '#153448', .055)
for y in range(1, 62, 4):
    b.line(0, y, 91, y, '#153448', .055)
# Pórtico esquemático, sin medidas ni carácter de proyecto construido.
for x in [69, 74, 79, 84]:
    b.line(x, 8, x, 20, '#31596E', .2)
    b.line(x, 8, x+3, 5, '#31596E', .2)
b.line(69, 8, 84, 8, '#31596E', .3)
b.line(72, 5, 87, 5, '#31596E', .3)
b.line(69, 20, 84, 20, '#31596E', .3)
b.text('NUESTRA ESPECIALIZACIÓN', 8, 14, 10.4, 'OutfitBold', WHITE)
b.line(8, 19, 61, 19, CYAN, .22)
specialties(b, [26, 32.5, 39, 47.5, 54], WHITE, CYAN, size=8.5)
b.page(); b.finish()


# C: vertical editorial, con arte conceptual creado para este encargo en Higgsfield.
c = Card('C', 'Luz y materia', 61, 91)
c.art(OUT/'imagenes/arquitectura-calida.png', 0, 0, 61, 48)
c.rect(0, 0, 61, 23, NAVY)
c.brand(color=WHITE)
c.rect(0, 45, 61, 46, PAPER)
c.line(8, 45, 53, 45, COPPER, .5)
c.text('Richard', 8, 54, 20, 'Serif', BLUE)
c.text('Castro Núñez', 8, 62, 20, 'Serif', BLUE, tracking=-.4)
c.text('Ingeniero Industrial', 8, 68, 8, color=MUTED)
c.text('Arquitecto Técnico', 8, 72, 8, color=MUTED)
c.contacts(8, 78.5, 84, BLUE, 11, 8)
c.page()
c.rect(0, 0, 61, 91, PAPER)
c.rect(0, 0, 61, 4, COPPER)
c.text('NUESTRA', 8, 12.5, 7, 'Mono', COPPER, tracking=.6)
c.text('Especialización', 8, 20, 15, 'Serif', BLUE)
vertical = [
    ['Inspección civil de', 'obras (ITO)'],
    ['Geotecnia y mecánica', 'de suelos'],
    ['Memorias de cálculo', 'y análisis estructurales'],
    ['Riego y fertirriego', 'tecnificado'],
    ['Ingeniería con', 'inteligencia artificial'],
]
for n, (lines, y) in enumerate(zip(vertical, [27, 34.5, 42, 49.5, 57]), 1):
    c.text(f'{n:02}', 8, y, 7, 'Mono', COPPER)
    for j, s in enumerate(lines):
        c.text(s, 15, y+j*3.6, 8, color=BLUE)
c.code(33, 64, 20)
c.mark(8, 66, 8, BLUE)
c.text('REC Ltda.', 8, 78, 7, 'OutfitBold', BLUE)
c.text('recingenieria.com', 8, 84, 7, 'InstrumentBold', BLUE)
c.page(); c.finish()


# Presentación comparativa con texto vectorial, dos caras por página.
PW, PH = 1200, 760
comp = OUT/'REC-opciones-A-B-C.pdf'
p = canvas.Canvas(str(comp), pagesize=(PW, PH), pageCompression=1)
p.setAuthor('REC Ingeniería'); p.setCreator('REC Ingeniería')
p.setTitle('REC Ingeniería | Opciones de tarjeta A, B y C')
titles = {'A': ('Materia precisa', 'Imagen arquitectónica · Azul profundo · Horizontal'),
          'B': ('Plano técnico', 'Geometría de planos · Contraste limpio · Horizontal'),
          'C': ('Luz y materia', 'Texturas arquitectónicas · Tipografía editorial · Vertical')}
rects = {}
for letter in 'ABC':
    title, desc = titles[letter]
    p.setFillColor(HexColor('#E8E7E3')); p.rect(0,0,PW,PH,fill=1,stroke=0)
    p.setFillColor(HexColor(BLUE)); p.setFont('Mono', 12)
    p.drawString(58, 705, f'REC INGENIERÍA / OPCIÓN {letter}')
    p.setFont('OutfitBold', 30); p.drawString(58, 660, title)
    p.setFillColor(HexColor(MUTED)); p.setFont('Instrument', 13)
    p.drawString(58, 632, desc)
    if letter != 'C':
        boxes = [fitz.Rect(58, 201, 579, 201+521*55/85),
                 fitz.Rect(621, 201, 1142, 201+521*55/85)]
    else:
        boxes = [fitz.Rect(266, 170, 521, 170+255*85/55),
                 fitz.Rect(678, 170, 933, 170+255*85/55)]
    rects[letter] = boxes
    for n, box in enumerate(boxes):
        p.setFillColor(HexColor('#CFCFCB'))
        p.rect(box.x0+7, PH-box.y1-8, box.width, box.height, fill=1, stroke=0)
        p.setFillColor(HexColor(MUTED)); p.setFont('Mono', 10)
        p.drawString(box.x0, PH-box.y1-30, ['FRENTE', 'REVERSO'][n])
    p.setFillColor(HexColor(BLUE)); p.setFont('Instrument', 12)
    p.drawString(58, 65, 'Richard Castro Núñez · +34 611 437 071 · richard.castro@recltda.cl')
    p.setFillColor(HexColor(MUTED)); p.setFont('Instrument', 10)
    p.drawString(58, 43, 'QR: recingenieria.com  |  Propuesta para elegir modelo  |  Vista ampliada de ambas caras')
    p.showPage()
p.save()
presentation = fitz.open(comp)
meta = presentation.metadata; meta['producer'] = 'REC Ingeniería'
presentation.set_metadata(meta)
for n, letter in enumerate('ABC'):
    source = fitz.open(OUT/f'REC-opcion-{letter}-imprimir.pdf')
    for k, dest in enumerate(rects[letter]):
        presentation[n].show_pdf_page(dest, source, k, clip=source[k].trimbox)
    source.close()
presentation.saveIncr()
for n, page in enumerate(presentation):
    page.get_pixmap(matrix=fitz.Matrix(2,2), alpha=False).save(OUT/f'REC-opcion-{"ABC"[n]}-vista.png')
presentation.close()


# Comprobaciones sobre los artefactos definitivos, no una maqueta intermedia.
proof = {'autor': 'REC Ingeniería', 'fecha': '2026-10-06', 'qr': URL,
         'telefono_unico': PHONE, 'correo': EMAIL, 'sangrado_mm': 3,
         'png_ppp': 600, 'opciones': [], 'tipografia': measurements}
required = ['REC Ltda.', 'Richard Castro Núñez', 'Ingeniero Industrial',
            'Arquitecto Técnico', PHONE, EMAIL, 'recingenieria.com']
required += [' '.join(s) for s in SPECIALTIES]
for letter in 'ABC':
    path = OUT/f'REC-opcion-{letter}-imprimir.pdf'
    doc = fitz.open(path)
    body = ' '.join(' '.join(p.get_text().split()) for p in doc)
    for s in required:
        assert s in body, (letter, s)
    assert '+56' not in body and 'www.recltda.cl' not in body
    assert len(doc) == 2 and doc.metadata['author'] == 'REC Ingeniería'
    links = [l['uri'] for page in doc for l in page.get_links()]
    assert URL in links and 'https://wa.me/34611437071' in links
    qr_found = []
    for n, page in enumerate(doc):
        for dpi in [600, 200]:
            pix = page.get_pixmap(dpi=dpi, clip=page.trimbox, alpha=False)
            img = Image.frombytes('RGB', [pix.width,pix.height], pix.samples)
            values = [x.text for x in zxingcpp.read_barcodes(img)]
            if URL in values:
                qr_found.append({'cara':n+1, 'dpi':dpi})
    assert any(x['dpi']==200 for x in qr_found), (letter, qr_found)
    proof['opciones'].append({'opcion':letter, 'archivo':path.name,
        'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'corte_mm':[round(doc[0].trimbox.width/MM),round(doc[0].trimbox.height/MM)],
        'enlaces':links, 'qr_decodificado':qr_found,
        'fuentes': sorted({f[3] for p in doc for f in p.get_fonts()})})
    doc.close()
(ROOT/'documentacion/evidencias/tarjetas-abc.json').write_text(
    json.dumps(proof, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({k:v for k,v in proof.items() if k!='tipografia'},ensure_ascii=False))
