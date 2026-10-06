# Tarjeta REC Ingeniería: Materia precisa

Revisión del 6 de octubre de 2026. Dos caras: frente azul profundo con una estructura conceptual que pasa de materia a dibujo; reverso claro con el nombre completo, apoyo técnico a estudios y empresas, WhatsApp de España, correo y contacto digital. El WhatsApp de Chile se ha retirado de las tarjetas física y digital.

## Archivos

- `REC-tarjeta-91x61-con-sangrado.pdf`: original de impresión. Texto vectorial, fuentes incrustadas, ilustración conceptual de alta resolución y enlaces digitales activos. Dos páginas, frente y reverso.
- `tarjeta-frente.svg` y `tarjeta-reverso.svg`: arte vectorial con letras en contornos e imagen incrustada. Medidas físicas 91 × 61 mm. No requieren instalar fuentes para conservar el aspecto.
- `tarjeta-frente.png` y `tarjeta-reverso.png`: 2150 × 1441 px, 600 ppp, con sangrado.
- `REC-tarjeta-91x61-con-sangrado.pptx`: dos diapositivas con el SVG de cada cara y respaldo PNG. El arte se mueve y escala como objeto; el texto se cambia desde el generador, no como cajas de texto independientes.
- `REC-tarjeta-vista.png`: vista de las dos caras al corte, para revisión del diseño.
- `direccion-tarjeta.md`: dirección artística y criterio de composición.

## Medidas y lectura

Corte final: **85 × 55 mm**. Archivo: **91 × 61 mm**, con **3 mm de sangrado** por lado. El PDF incorpora TrimBox de 85 × 55 mm y BleedBox de 91 × 61 mm. El texto esencial conserva al menos 3,5 mm desde el corte hasta sus glifos, medidos en el PDF final.

Nombre en Outfit; contactos en Instrument Sans; indicación de países en DM Mono. Teléfonos a 11,2 puntos, correo a 7,7 puntos y servicios a 7,5 puntos. Los datos necesarios para contactar tienen un mínimo de 6,5 puntos. El pequeño rótulo de la ilustración y el título auxiliar del QR no forman parte de esos datos esenciales.

El QR mide 22 mm, con cuatro módulos blancos de margen. Destino estable: https://recingenieria.com/. La lectura digital se verifica desde el PNG final y el PDF. El sitio y el contacto descargable utilizan solo el número de España.

## Regenerar

Instalar las dependencias Node con `npm ci` y las bibliotecas Python `reportlab`, `pymupdf`, `zxing-cpp` y `Pillow`. En el PC canónico, ejecutar `npm run tarjetas` con Python 3.12. El generador independiente evita reconstruir la presentación o el informe de estrategia.

La fuente editable es `herramientas/generar-tarjeta.py`, con la imagen de `imagenes/estructura-editorial.png` y las fuentes de `fuentes/`. Se incluyen las licencias SIL Open Font License completas; se permite su uso e incrustación en estos materiales. `npm run materiales` también utiliza esta tarjeta actual.

## Antes del lote

El archivo utiliza color RGB. Confirmar con la imprenta el perfil de conversión CMYK, el acabado y las marcas de corte que necesite. Imprimir una unidad a tamaño real y escanearla antes del lote. La comprobación digital no equivale a una prueba física. El nombre comercial continúa siendo REC Ingeniería; no se modifica la razón social ni se anuncian atribuciones profesionales pendientes de verificar.
