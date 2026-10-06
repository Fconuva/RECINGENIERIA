from pathlib import Path
import json, zipfile, re
import fitz
import zxingcpp
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'materiales_comerciales'
WEB=ROOT/'00_SITIO_WEB_REC'
VCF=WEB/'richard-castro.vcf'
VCF.write_bytes(VCF.read_text(encoding='utf-8').replace('\r\n','\n').replace('\n','\r\n').encode('utf-8'))
results={}
for p in OUT.glob('*.pdf'):
    doc=fitz.open(p)
    if 'tarjeta' in p.name:
        mm=72/25.4
        for page in doc:
            r=page.mediabox; cx=(r.x0+r.x1)/2;cy=(r.y0+r.y1)/2
            page.set_trimbox(fitz.Rect(cx-42.5*mm,cy-27.5*mm,cx+42.5*mm,cy+27.5*mm))
        doc.saveIncr()
    results[p.name]={'paginas':len(doc),'autor':doc.metadata.get('author'),'asunto':doc.metadata.get('subject'),'tamaños_mm':[[round(page.rect.width/mm,2),round(page.rect.height/mm,2)] for page in doc] if 'tarjeta' in p.name else None}
    meta=json.dumps(doc.metadata,ensure_ascii=False)
    assert not re.search('Francisco|Valenzuela|PptxGenJS',meta,re.I),meta
    assert len(doc)==(2 if 'tarjeta' in p.name else 8)
    doc.close()
for p in OUT.glob('*.pptx'):
    with zipfile.ZipFile(p) as z:
        core=z.read('docProps/core.xml').decode()
        assert not re.search('Francisco|Valenzuela|PptxGenJS',core,re.I),core
qr=[]
for p in [WEB/'assets/qr-rec.png',OUT/'tarjeta-reverso.png']:
    decoded=zxingcpp.read_barcodes(Image.open(p))
    assert any(x.text=='https://recingenieria.com/' for x in decoded),str(p)
    qr.append({'archivo':p.name,'destino':decoded[0].text})
results['qr']=qr
html=(WEB/'index.html').read_text(encoding='utf-8')
assert 'https://wa.me/34611437071' in html and 'https://wa.me/56971532583' not in html
assert '+56971532583' not in VCF.read_text(encoding='utf-8')
assert 'richard.castro@recltda.cl' in html
assert not re.search('sin errores|eliminar cualquier error humano',html,re.I)
print(json.dumps(results,ensure_ascii=False,indent=2))
(ROOT/'documentacion/evidencias').mkdir(parents=True,exist_ok=True)
(ROOT/'documentacion/evidencias/verificacion-materiales.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
