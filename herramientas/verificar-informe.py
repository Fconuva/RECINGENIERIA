from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET
import argparse, json
import fitz

parser=argparse.ArgumentParser()
parser.add_argument('docx')
parser.add_argument('--paginas',type=int,required=True)
args=parser.parse_args()
docx=Path(args.docx).resolve()
pdf=docx.with_suffix('.pdf')
with ZipFile(docx) as z:
    core=ET.fromstring(z.read('docProps/core.xml'))
    ns={'dc':'http://purl.org/dc/elements/1.1/','cp':'http://schemas.openxmlformats.org/package/2006/metadata/core-properties'}
    assert core.find('dc:creator',ns).text=='REC Ingeniería'
    assert core.find('cp:lastModifiedBy',ns).text=='REC Ingeniería'
    title=core.find('dc:title',ns).text
    for name in z.namelist():
        if name.endswith('.xml'): ET.fromstring(z.read(name))
with fitz.open(pdf) as d:
    assert len(d)==args.paginas, f'Páginas reales: {len(d)}'
    meta=d.metadata
    meta.update(author='REC Ingeniería',title=title,subject='Propuesta comercial para revisión',keywords='REC Ingeniería; estrategia comercial; Comunidad Valenciana')
    d.set_metadata(meta)
    d.saveIncr()
with fitz.open(pdf) as d:
    output=pdf.parent/'revision_visual'
    output.mkdir(exist_ok=True)
    for i,page in enumerate(d):
        assert len(page.get_text().strip())>150, f'Página vacía: {i+1}'
        page.get_pixmap(matrix=fitz.Matrix(1.3,1.3)).save(output/f'pagina-{i+1:02d}.png')
    result={'paginas':len(d),'autor_docx_pdf':'REC Ingeniería','xml_docx_bien_formado':True,'enlaces_pdf':sum(len(p.get_links()) for p in d),'revision_visual':str(output)}
    assert result['enlaces_pdf']>=12
print(json.dumps(result,ensure_ascii=False))
