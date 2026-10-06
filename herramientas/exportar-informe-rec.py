"""Actualizar índice Word, exportar PDF y limpiar metadatos REC."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from io import BytesIO
from xml.etree import ElementTree as ET
import sys,json,fitz,subprocess
docx=Path(sys.argv[1]).resolve()
pdf=docx.with_suffix('.pdf')
assert docx.is_file(),docx
# Office mediante PowerShell: evita alterar la caché makepy global del PC.
if '--solo-metadatos' not in sys.argv:
    result=subprocess.run(['powershell','-NoProfile','-File',
        str(Path(__file__).with_name('exportar-informe-rec-office.ps1')),
        '-Documento',str(docx)],capture_output=True,text=True)
    if result.returncode:
        sys.stderr.write(result.stderr)
        raise SystemExit(result.returncode)
    status=json.loads(result.stdout.strip())
with fitz.open(pdf) as check:
    pages=len(check)
    assert pages>2 and 'ÍNDICE' in check[1].get_text(),'Índice Word no actualizado'

with ZipFile(docx) as source:
    output=BytesIO()
    with ZipFile(output,'w',ZIP_DEFLATED) as target:
        for item in source.infolist():
            raw=source.read(item.filename)
            if item.filename=='docProps/core.xml':
                core=ET.fromstring(raw)
                for tag in ['{http://purl.org/dc/elements/1.1/}creator',
                            '{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}lastModifiedBy']:
                    node=core.find(tag)
                    if node is None:node=ET.SubElement(core,tag)
                    node.text='REC Ingeniería'
                raw=ET.tostring(core,encoding='utf-8',xml_declaration=True)
            target.writestr(item,raw)
docx.write_bytes(output.getvalue())
with fitz.open(pdf) as doc:
    meta=doc.metadata
    meta.update(author='REC Ingeniería',creator='REC Ingeniería',producer='REC Ingeniería',
                subject='Estrategia comercial, emitida para revisión',
                keywords='REC Ingeniería; Comunidad Valenciana; Rev02')
    doc.set_metadata(meta);doc.saveIncr()
print(json.dumps({'docx':str(docx),'pdf':str(pdf),'paginas':pages,'indice_actualizado':True,
                  'autor':'REC Ingeniería'},ensure_ascii=False))
