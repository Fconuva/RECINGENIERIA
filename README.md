# REC Ingeniería

Repositorio público de la web y los materiales comerciales de Richard Castro Núñez y REC Ingeniería. Raíz editable local: `C:/dev/rec-ingenieria`. Remoto: `https://github.com/Fconuva/RECINGENIERIA`.

## Empezar

1. Leer `AGENTS.md` y `.github/skills/rec-comercial/SKILL.md`.
2. Sitio: `00_SITIO_WEB_REC/`. Dominio que se conserva: **recingenieria.com**.
3. Investigación, presentación, tarjeta y guiones: `materiales_comerciales/`.
4. Skills: `.github/skills/`; agente: `.github/agents/RICHARDIA.agent.md`.
5. Solo en el PC: expediente S003, bitácora e inventario privado con SHA-256 bajo `06_SERVICIOS_REC/` y `documentacion/migracion/`.

## Materiales comerciales

La investigación pública, el posicionamiento y los guiones están en `materiales_comerciales/`. El expediente interno S003 se conserva únicamente en el PC. Las propuestas de presentación, tarjeta y QR se generan con `npm ci` y `npm run materiales`. Son propuestas para revisión; no prueban demanda comercial ni atribuciones profesionales en España.

- [Cinco especialidades: evidencia y oferta](materiales_comerciales/analisis-cinco-especialidades.md).
- [Identidad visual y fundamento de percepción y diseño](materiales_comerciales/identidad-visual.md).
- [Presentación comercial en PDF](materiales_comerciales/REC-presentacion-comercial.pdf).
- [Tarjeta física con sangrado en PDF](materiales_comerciales/REC-tarjeta-91x61-con-sangrado.pdf).
- [Nueva tarjeta: vista de ambas caras](materiales_comerciales/REC-tarjeta-vista.png) y [especificaciones de impresión](materiales_comerciales/LEEME-TARJETA.md).
- [Alternativas A, B y C: comparador para compartir](materiales_comerciales/tarjetas-ABC/REC-opciones-A-B-C.pdf) y [fuentes, formatos y guía de uso](materiales_comerciales/tarjetas-ABC/LEAME.md). Estas propuestas conservan las cinco especialidades y los títulos declarados en las tarjetas originales, con el contacto español único.

Identidad común: azul de REC y un símbolo estructural simplificado, con nombre comercial REC Ingeniería. La selección de estilo se explica como decisión de diseño; la investigación académica no se presenta como garantía de confianza o ventas.

## Archivo y privacidad

Los originales locales no se borran ni se modifican. `90_ARCHIVO_HISTORICO/` conserva copias verificadas de fuentes pequeñas organizadas por procedencia, con sus instrucciones históricas. Los binarios grandes permanecen en sus carpetas originales, identificados en el inventario local. El archivo histórico completo no está en GitHub.

Por decisión del usuario, el repositorio se mantiene público: los informes de clientes, correos, skills con antecedentes internos y binarios históricos quedan locales e ignorados. No se suben paquetes privados a este remoto. Credenciales, entornos Python, dependencias y cachés quedan fuera de Git. El sitio público se despliega desde su carpeta, nunca desde la raíz de este repositorio.

## Generación y despliegue

`npm ci` y `npm run materiales` generan las propuestas desde las imágenes incluidas. `npm run tarjetas` reconstruye solo las dos caras, su PDF vectorial y PowerPoint; requiere Python 3.12 con reportlab, pymupdf, zxing-cpp y Pillow. En Windows, `herramientas/exportar-office.ps1` exporta el PDF de la presentación con Microsoft PowerPoint y conserva el PDF vectorial de la tarjeta; `py -3.12 herramientas/verificar-materiales.py` verifica QR, contactos y formato de corte.

Las alternativas A/B/C tienen un generador separado: `py -3.12 -X utf8 herramientas/generar-tarjetas-abc.py`. Reconstruye sus PDF y PNG y comprueba el texto, los contactos y el QR; conserva los demás materiales.

La web se puede previsualizar con un servidor estático. El despliegue de producción requiere la copia local de los informes y sus visores heredados, excluidos del clon público, para conservar enlaces ya entregados. Desde `00_SITIO_WEB_REC/`, usar Vercel CLI para vista previa y, tras revisión independiente, producción en el proyecto existente.

Los informes nuevos usan la [receta documental REC](documentacion/formato-informes-rec.md): portada, control de revisiones, índice real y cuerpo continuo. La fuente y los informes de cliente permanecen privados. Las tarjetas vigentes concentran el contacto en España, con un único WhatsApp en el arte físico, la web y la vCard.
