# Formato de informes REC

Formato comercial adoptado a partir de documentos propios de REC. Antes de un informe nuevo, comprobar la referencia específica del encargo. Los originales históricos y las aprobaciones de otros proyectos se conservan intactos.

- A4, márgenes superior 22 mm, izquierdo 25 mm, inferior y derecho 20 mm.
- Calibri 10,5 puntos e interlineado 1,15 para texto continuo.
- Portada azul `#1F3A5F`, ficha documental, estado de revisión y control de versiones.
- Índice automático de capítulos y subtítulos, actualizado en Word.
- Títulos de 14 y 11,5 puntos; tablas con encabezado repetido, filas completas y anchos explícitos; figuras y tablas numeradas.
- Encabezado REC y ámbito del informe; pie con código, revisión y página actual/total.
- Autor y metadatos: REC Ingeniería. No copiar aprobadores, fotografías, datos ni firmas de otro encargo.

## Generar y revisar

La fuente JSON y el informe de cliente permanecen en el expediente privado. No se incluyen en este repositorio público. Utilizar un nombre nuevo para cada revisión.

```powershell
node herramientas/generar-informe-rec.cjs entrada-privada.json informe-nueva-revision.docx
py -3.12 -X utf8 herramientas/exportar-informe-rec.py informe-nueva-revision.docx
py -3.12 -X utf8 herramientas/verificar-informe.py informe-nueva-revision.docx --paginas NUMERO_REAL
```

La exportación requiere Microsoft Word, actualiza el índice y guarda el DOCX antes de producir el PDF. El número de páginas debe comprobarse en el PDF, no asumirse por la fuente. La verificación lee los artefactos y produce imágenes privadas para revisar todas las páginas; no modifica el informe.

Antes de la entrega: revisión independiente, contraste de fuentes y contenido, inspección de todas las páginas, paginación del índice, nombres y metadatos. Una revisión documental no equivale a aceptación del cliente ni autoriza un envío.
