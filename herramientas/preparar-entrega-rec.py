"""Copias de entrega S003; conserva los documentos originales y sus revisiones."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import shutil
import json
import hashlib
import sys
import re
from html import escape
import fitz
from PIL import Image
import zxingcpp

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT/'06_SERVICIOS_REC/S003_2026-10-06_POSICIONAMIENTO_VALENCIA'
OUT = CASE/'05_ENTREGA_CORREO'
PUBLIC = ROOT/'materiales_comerciales'
OUT.mkdir(exist_ok=True)
QA = CASE/'02_TRABAJO/qa-entrega-correo'
QA.mkdir(exist_ok=True)

ALT_TEXT = {
    'suelo': 'Imagen conceptual de ingeniería geotécnica y estudio del suelo',
    'logo': 'Marca REC Ingeniería',
    'obra': 'Imagen conceptual de inspección y construcción de obras',
    'riego': 'Imagen conceptual de riego tecnificado y fertirriego',
}

def clean_slide_alt(raw):
    def replace(match):
        path = match.group(1)
        if not re.match(r'[A-Za-z]:[\\/]', path):
            return match.group(0)
        description = next((text for key, text in ALT_TEXT.items() if key in path.lower()),
                           'Imagen conceptual de servicios de REC Ingeniería')
        return 'descr="' + escape(description, quote=True) + '"'
    return re.sub(r'descr="([^"]*)"', replace, raw.decode('utf-8')).encode('utf-8')


def optimize(source, dest):
    with fitz.open(source) as doc:
        original_text = [p.get_text() for p in doc]
        original_links = [[x.get('uri') for x in p.get_links()] for p in doc]
        boxes = [(p.mediabox, p.trimbox, p.bleedbox) for p in doc]
        # Solo compresión documental de fotografías. Texto y QR siguen vectoriales.
        # Mantener dimensiones/resolución y excluir imágenes bitonales/QR.
        doc.rewrite_images(quality=92, bitonal=False, gray=False, dpi_target=0)
        doc.save(dest, garbage=4, deflate=True)
    with fitz.open(dest) as doc:
        assert [p.get_text() for p in doc] == original_text
        assert [[x.get('uri') for x in p.get_links()] for p in doc] == original_links
        assert [(p.mediabox,p.trimbox,p.bleedbox) for p in doc] == boxes
        for n, page in enumerate(doc):
            page.get_pixmap(dpi=150,alpha=False).save(QA/f'{dest.stem}-{n+1:02}.png')
        if 'tarjeta-' in dest.name:
            decoded=[]
            for n, page in enumerate(doc):
                for dpi in [200,600]:
                    pix=page.get_pixmap(dpi=dpi,clip=page.trimbox,alpha=False)
                    im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
                    values=[r.text for r in zxingcpp.read_barcodes(im)]
                    if 'https://recingenieria.com/' in values:
                        decoded.append((n+1,dpi))
            assert any(dpi==200 for _,dpi in decoded), dest


if '--exported' not in sys.argv:
    for extension in ['pdf','docx']:
        source=CASE/'04_ENTREGA_PARA_REVISION'/f'REC-estrategia-comercial-Rev02.{extension}'
        shutil.copy2(source, OUT/source.name)
    slide=CASE/'02_TRABAJO/presentacion-espana-Rev02/slide8.xml'
    target=OUT/'REC-presentacion-comercial-Rev02.pptx'
    with ZipFile(PUBLIC/'REC-presentacion-comercial.pptx') as source, ZipFile(target,'w',ZIP_DEFLATED) as dest:
        for item in source.infolist():
            raw=slide.read_bytes() if item.filename=='ppt/slides/slide8.xml' else source.read(item.filename)
            if re.fullmatch(r'ppt/slides/slide\d+\.xml', item.filename):
                raw = clean_slide_alt(raw)
            dest.writestr(item,raw)
    with ZipFile(target) as archive:
        assert archive.testzip() is None
        slides=' '.join(archive.read(f'ppt/slides/slide{i}.xml').decode('utf-8') for i in range(1,9))
        assert '+56' not in slides and '7153' not in slides
        assert '+34 611 437 071' in slides
    for letter in 'ABC':
        optimize(PUBLIC/f'tarjetas-ABC/REC-opcion-{letter}-imprimir.pdf',
                 OUT/f'REC-tarjeta-{letter}-imprimir.pdf')
        shutil.copy2(PUBLIC/f'tarjetas-ABC/REC-opcion-{letter}-vista.png',OUT/f'REC-tarjeta-{letter}-vista.png')
    optimize(PUBLIC/'tarjetas-ABC/REC-opciones-A-B-C.pdf',OUT/'REC-tarjetas-comparador-A-B-C.pdf')
else:
    deck=OUT/'REC-presentacion-comercial-Rev02.pdf'
    with fitz.open(deck) as doc:
        assert len(doc)==8
        text=' '.join(p.get_text() for p in doc)
        assert '+56' not in text and '7153' not in text and '+34 611 437 071' in text
        meta=doc.metadata
        meta.update(author='REC Ingeniería',creator='REC Ingeniería',producer='REC Ingeniería',
                    title='REC Ingeniería | Presentación comercial Rev02',
                    subject='Presentación comercial; contacto España')
        doc.set_metadata(meta);doc.saveIncr()
    with fitz.open(deck) as doc:
        for n,p in enumerate(doc):
            p.get_pixmap(dpi=130,alpha=False).save(QA/f'presentacion-{n+1:02}.png')
    files=[x for x in OUT.iterdir() if x.is_file() and x.suffix.lower() in ['.pdf','.docx','.pptx','.png','.txt']]
    data={'fecha':'2026-10-06','remitente':'fconuva@gmail.com','destinatario':'richard.castro@recltda.cl',
          'enviado':False,'archivos':[{'nombre':p.name,'bytes':p.stat().st_size,
              'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(files)],
          'total_bytes':sum(p.stat().st_size for p in files)}
    (CASE/'02_TRABAJO/MANIFIESTO_ENTREGA_CORREO.json').write_text(
        json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(data,ensure_ascii=False))

print(json.dumps({'carpeta':str(OUT),'archivos':[{'nombre':p.name,'bytes':p.stat().st_size} for p in OUT.iterdir() if p.is_file()]},ensure_ascii=False))
