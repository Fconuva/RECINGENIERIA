"""Tarjeta REC: PDF con texto vectorial, SVG con contornos y PNG a 600 ppp.

Autor de los documentos: REC Ingeniería. La imagen es conceptual.
Requiere reportlab y PyMuPDF. Ejecutar con py -3.12 en el PC canónico.
"""
from pathlib import Path
import json
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.graphics.barcode import qr
import fitz

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'materiales_comerciales'
MM = 72 / 25.4
W, H = 91 * MM, 61 * MM
NAVY, BLUE, CYAN = '#0C2235', '#123A62', '#78B6D4'
WHITE, PAPER, MUTED = '#F8FAFC', '#F7F6F2', '#526574'
ART = OUT / 'imagenes/estructura-editorial.png'
URL = 'https://recingenieria.com/'
FONTS = {
    'OutfitBold': 'Outfit-Bold.ttf',
    'Outfit': 'Outfit-Regular.ttf',
    'Instrument': 'InstrumentSans-Regular.ttf',
    'InstrumentBold': 'InstrumentSans-Bold.ttf',
    'Mono': 'DMMono-Regular.ttf',
}
for name, file in FONTS.items():
    pdfmetrics.registerFont(TTFont(name, str(OUT / 'fuentes' / file)))

pdf = OUT / 'REC-tarjeta-91x61-con-sangrado.pdf'
c = canvas.Canvas(str(pdf), pagesize=(W, H), pageCompression=1)
c.setAuthor('REC Ingeniería')
c.setCreator('REC Ingeniería')
c.setTitle('REC Ingeniería | Tarjeta Materia precisa')
c.setSubject('Dos caras, corte 85 × 55 mm y sangrado de 3 mm')
measurements = []


def rect(x, y, w, h, fill, stroke=None, line=0.15):
    c.setFillColor(HexColor(fill))
    if stroke:
        c.setStrokeColor(HexColor(stroke))
        c.setLineWidth(line * MM)
    c.rect(x * MM, H - (y + h) * MM, w * MM, h * MM,
           fill=1, stroke=bool(stroke))


def line(x1, y1, x2, y2, color, width=0.15):
    c.setStrokeColor(HexColor(color))
    c.setLineWidth(width * MM)
    c.line(x1 * MM, H - y1 * MM, x2 * MM, H - y2 * MM)


def text(t, x, y, size, font='Instrument', color=NAVY, tracking=0,
         align='left', max_width=None, essential=True):
    width = pdfmetrics.stringWidth(t, font, size) / MM + tracking * (len(t)-1) / MM
    if align == 'center':
        x -= width / 2
    elif align == 'right':
        x -= width
    if max_width is not None:
        assert width <= max_width, (t, width, max_width)
    assert x >= 7.5 and x + width <= 83.5, (t, x, width)
    assert 7.5 <= y <= 54, (t, y)
    if essential:
        assert size >= 6.5, (t, size)
    c.setFillColor(HexColor(color))
    obj = c.beginText(x * MM, H - y * MM)
    obj.setFont(font, size)
    obj.setCharSpace(tracking)
    obj.textOut(t)
    c.drawText(obj)
    measurements.append({'texto': t, 'x_mm': round(x, 2), 'base_y_mm': y,
                         'ancho_mm': round(width, 2), 'puntos': size,
                         'esencial': essential})


def mark(x, y, scale=1, color=WHITE):
    # Mismo símbolo estructural de REC, geometría compartida con la web.
    def p(points, width):
        for a, b in zip(points, points[1:]):
            line(x + a[0]*scale/10, y + a[1]*scale/10,
                 x + b[0]*scale/10, y + b[1]*scale/10, color, width*scale)
    p([(0,10),(0,2),(7.4,2),(7.4,10)], .042)
    p([(0,4.3),(7.4,4.3)], .042)
    p([(3.7,4.3),(3.7,10)], .042)
    p([(0,2),(2.2,0),(9.6,0),(9.6,8),(7.4,10)], .027)
    p([(7.4,2),(9.6,0)], .027)
    p([(7.4,4.3),(9.6,2.3)], .027)


# Frente: toda la superficie es arte; el texto se sitúa en el espacio oscuro.
c.drawImage(str(ART), 0, 0, width=W, height=H, preserveAspectRatio=False)
mark(8.2, 8.8, scale=9)
text('REC', 19.7, 17.0, 29, 'OutfitBold', WHITE, tracking=-.7)
text('INGENIERÍA', 19.9, 21.0, 7.6, 'Outfit', WHITE, tracking=.95)
text('Del terreno', 8.0, 32.0, 18.6, 'Outfit', WHITE, tracking=-.25,
     max_width=43)
text('al proyecto.', 8.0, 39.2, 18.6, 'Outfit', WHITE, tracking=-.25,
     max_width=43)
line(8, 43.0, 18.0, 43.0, CYAN, .34)
text('Suelo y estructuras', 8.0, 47.0, 7.5, color=WHITE)
text('Seguimiento de obras', 8.0, 50.4, 7.5, color=WHITE)
text('Riego y fertirriego', 8.0, 53.8, 7.5, color=WHITE)
rect(66, 50.4, 19.5, 5.5, NAVY)
text('Visual conceptual', 83, 53.8, 5.0, 'Instrument', '#C4D6E1',
     align='right', essential=False)
c.linkURL(URL, (59*MM, 5*MM, 84*MM, 10*MM), relative=0)
c.showPage()

# Reverso: papel cálido, nombre completo en una sola línea y panel digital.
rect(0, 0, 91, 61, PAPER)
rect(58.5, 20.5, 32.5, 40.5, '#EAF0F2')
text('Richard Castro Núñez', 8.0, 13.0, 15.0, 'OutfitBold', NAVY,
     tracking=-.22, max_width=75)
text('REC Ingeniería · Apoyo técnico a estudios y empresas', 8.1, 17.3,
     6.8, 'Instrument', MUTED, max_width=62)
text('ESPAÑA', 83, 17.3, 6.5, 'Mono', BLUE, align='right')
line(8.0, 20.5, 83, 20.5, BLUE, .18)
text('WhatsApp España', 8, 26.1, 6.8, color=MUTED)
text('+34 611 437 071', 8, 31.4, 11.2, 'InstrumentBold', BLUE, max_width=45)
text('Correo electrónico', 8, 37.9, 6.8, color=MUTED)
text('richard.castro@recltda.cl', 8, 43.2, 7.7, 'Instrument', BLUE, max_width=45)
line(8, 46.3, 52, 46.3, '#C6CED0', .12)
text('Hablemos de su proyecto.', 8, 51.0, 8.0, 'Outfit', BLUE,
     max_width=45)
code = qr.QrCodeWidget(URL, barLevel='M', barBorder=4)
bd = code.getBounds()
qsize = 22 * MM
qscale = qsize / (bd[2]-bd[0])
rect(61, 23.4, 22, 22, '#FFFFFF')
c.saveState()
c.translate(61*MM, H-45.4*MM)
c.scale(qscale, qscale)
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
draw = Drawing(bd[2]-bd[0], bd[3]-bd[1])
draw.add(code)
renderPDF.draw(draw, c, -bd[0], -bd[1])
c.restoreState()
for x, y, sx, sy in [(60.3,22.7,1,1),(83.7,22.7,-1,1),
                     (60.3,46.1,1,-1),(83.7,46.1,-1,-1)]:
    line(x, y, x+1.3*sx, y, CYAN, .25)
    line(x, y, x, y+1.3*sy, CYAN, .25)
text('CONTACTO DIGITAL', 72, 49.4, 6.2, 'Outfit', BLUE, tracking=.3,
     align='center', essential=False)
text('recingenieria.com', 72, 53.5, 7.0, 'InstrumentBold', BLUE,
     align='center', max_width=23)
for url, box in [
    ('https://wa.me/34611437071', (8, 24, 53, 33)),
    ('mailto:richard.castro@recltda.cl', (8, 36, 53, 45)),
    (URL, (60, 22, 84, 55)),
]:
    x1,y1,x2,y2=box
    c.linkURL(url, (x1*MM, H-y2*MM, x2*MM, H-y1*MM), relative=0)
c.showPage()
c.save()

doc = fitz.open(pdf)
metadata=doc.metadata
metadata['producer']='REC Ingeniería'
doc.set_metadata(metadata)
for n, page in enumerate(doc):
    page.set_trimbox(fitz.Rect(3*MM, 3*MM, 88*MM, 58*MM))
    page.set_bleedbox(page.mediabox)
doc.saveIncr()
for n, page in enumerate(doc):
    name = ['tarjeta-frente', 'tarjeta-reverso'][n]
    pix = page.get_pixmap(dpi=600, alpha=False)
    pix.save(OUT / f'{name}.png')
    svg = page.get_svg_image(text_as_path=True)
    import re
    svg = re.sub(r'width="[^"]+" height="[^"]+"',
                 'width="91mm" height="61mm"', svg, count=1)
    svg = re.sub(r'(data:image/[^;]+;base64,)([^\"]+)',
                 lambda m: m.group(1) + re.sub(r'\s+', '', m.group(2)), svg)
    (OUT / f'{name}.svg').write_text(svg, encoding='utf-8')
doc.close()

# Lámina de revisión: ambas caras reales, cortadas al tamaño final.
# Se crea como documento; no se altera el recurso visual de Higgsfield.
preview = OUT / '.tarjeta-vista-documento.pdf'
PW, PH = 1200, 600
p = canvas.Canvas(str(preview), pagesize=(PW,PH))
p.setAuthor('REC Ingeniería')
p.setCreator('REC Ingeniería')
p.setFillColor(HexColor('#DDE4E7'))
p.rect(0,0,PW,PH,fill=1,stroke=0)
p.setFillColor(HexColor(NAVY))
p.setFont('OutfitBold', 23)
p.drawString(56, 539, 'REC Ingeniería')
p.setFillColor(HexColor(MUTED))
p.setFont('Instrument', 11)
p.drawString(56, 515, 'Materia precisa · Frente y reverso · 85 × 55 mm')
for name, x, y, width in [('tarjeta-frente', 56, 100, 530),
                           ('tarjeta-reverso', 614, 100, 530)]:
    height = width * 55/85
    p.setFillColor(HexColor('#C2CED3'))
    p.rect(x+7, y-7, width, height, fill=1, stroke=0)
    p.saveState()
    path=p.beginPath(); path.rect(x,y,width,height)
    p.clipPath(path,stroke=0,fill=0)
    # Se respeta el corte a 3 mm, sin estirar la proporción de la tarjeta.
    unit=width/85
    p.drawImage(str(OUT/f'{name}.png'),x-3*unit,y-3*unit,
                width=91*unit,height=61*unit)
    p.restoreState()
p.showPage();p.save()
pr=fitz.open(preview)
pr[0].get_pixmap(matrix=fitz.Matrix(2,2),alpha=False).save(OUT/'REC-tarjeta-vista.png')
pr.close();preview.unlink()

# Comprobaciones de salida con el PDF y sus imágenes definitivos.
import zxingcpp
from PIL import Image
decoded=zxingcpp.read_barcodes(Image.open(OUT/'tarjeta-reverso.png'))
assert any(x.text == URL for x in decoded), decoded
doc=fitz.open(pdf)
assert len(doc)==2
assert doc.metadata['author']=='REC Ingeniería'
body='\n'.join(page.get_text() for page in doc)
for value in ['Richard Castro Núñez','+34 611 437 071',
              'richard.castro@recltda.cl','Suelo y estructuras',
              'Seguimiento de obras','Riego y fertirriego']:
    assert value in body, value
assert '+56' not in body and 'CHILE' not in body
assert not any('56971532583' in l.get('uri','') for page in doc for l in page.get_links())
proof={'identidad':'REC Ingeniería','version':'Materia precisa, 6 octubre 2026',
       'paginas':2,'corte_mm':[85,55],'sangrado_mm':3,'png_ppp':600,
       'qr_destino':URL,'texto_vectorial':True,
       'fuentes_pdf':sorted({f[3] for page in doc for f in page.get_fonts()}),
       'enlaces_pdf':[l['uri'] for page in doc for l in page.get_links()],
       'tipografia':measurements}
(ROOT/'documentacion/evidencias/tarjeta-materia-precisa.json').write_text(
    json.dumps(proof,ensure_ascii=False,indent=2),encoding='utf-8')
doc.close()
print(json.dumps({k:v for k,v in proof.items() if k!='tipografia'},ensure_ascii=False))
