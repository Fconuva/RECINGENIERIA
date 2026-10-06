# Validación de la propuesta comercial

6 de octubre de 2026. Revisión independiente final: apta para publicación digital, sin hallazgos graves o medios pendientes en el alcance revisado.

- Ocho diapositivas y dos caras de tarjeta inspeccionadas visualmente. Contactos y metadatos cotejados; autor REC Ingeniería.
- QR decodificados en web, presentación y tarjeta: https://recingenieria.com/.
- PDF de tarjeta con TrimBox de 85 × 55 mm y sangrado exterior. PNG de 1075 × 721 px a 300 dpi. vCard con CRLF preservado en Git.
- Web comprobada en 320 × 740, 390 × 844 y 1440 × 900. Contactos visibles en móvil, navegación por secciones, imágenes y pausa de video comprobados. Sin errores o advertencias observados en la consola de la vista previa.
- JavaScript revisado de forma independiente: reproducción, pausa, reanudación y preferencia de movimiento reducido. Dependencias npm sin vulnerabilidades conocidas en la comprobación realizada.
- Revisión de 45 rutas públicas antes de publicar: sin correos, expedientes, archivo histórico ni informes de clientes. Manifiesto de vista previa conserva 96 archivos de informes y visores heredados sin cambios respecto de la producción anterior.

La revisión digital no sustituye una prueba física de imprenta ni confirma categoría BNI, atribuciones personales en España, importación en un teléfono o funcionamiento efectivo de las cuentas de WhatsApp. Las imágenes son conceptuales y los objetivos comerciales son propuestas, no resultados acreditados.

## Publicación comprobada

Web publicada en https://recingenieria.com, despliegue `dpl_F6YqCraXn5TLh7fJH1yJtBEqU3ZG`, READY / production. Página, CSS, JavaScript, video, QR y vCard respondieron HTTP 200 y coinciden por SHA-256 con los archivos locales revisados. Conservados 96 archivos de entregas y visores por comparación del manifiesto; un PDF heredado también se descargó y comparó sin diferencias. La redirección de `/servicios` llega a `/#servicios`. Prueba móvil repetida sobre el dominio definitivo. Evidencia técnica: `publicacion.json`.
