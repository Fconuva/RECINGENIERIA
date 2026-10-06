"""Incluir PNG compatibles junto al SVG nativo del PowerPoint de tarjeta."""
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED
import re
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'materiales_comerciales'
file=OUT/'REC-tarjeta-91x61-con-sangrado.pptx'
with ZipFile(file) as source:
    names=source.namelist()
    replacements={f'ppt/media/image-{i}-1.png':(OUT/f'tarjeta-{face}.png').read_bytes()
                  for i,face in [(1,'frente'),(2,'reverso')]}
    assert set(replacements).issubset(names), names
    for data in replacements.values():
        assert data.startswith(b'\x89PNG\r\n\x1a\n')
    result=BytesIO()
    with ZipFile(result,'w',ZIP_DEFLATED) as target:
        for item in source.infolist():
            target.writestr(item,replacements.get(item.filename,source.read(item.filename)))
file.write_bytes(result.getvalue())
with ZipFile(file) as checked:
    for name,data in replacements.items():
        assert checked.read(name)==data
    for name in names:
        if name.endswith('.svg'):
            art=checked.read(name).decode('utf-8')
            assert 'width="91mm" height="61mm"' in art
        if name.startswith('ppt/notesSlides/notesSlide') and name.endswith('.xml'):
            note=checked.read(name).decode('utf-8')
            assert not re.search(r'generar-|herramientas/|Francisco|Valenzuela',note,re.I),note
    core=checked.read('docProps/core.xml').decode('utf-8')
    assert 'REC Ingeniería' in core and not re.search('Francisco|Valenzuela|PptxGenJS',core,re.I)
print('PowerPoint: dos SVG de 91 × 61 mm y dos respaldos PNG reales, notas y autor comprobados.')
