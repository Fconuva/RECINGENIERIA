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

## Archivo y privacidad

Los originales locales no se borran ni se modifican. `90_ARCHIVO_HISTORICO/` conserva copias verificadas de fuentes pequeñas organizadas por procedencia, con sus instrucciones históricas. Los binarios grandes permanecen en sus carpetas originales, identificados en el inventario local. El archivo histórico completo no está en GitHub.

Por decisión del usuario, el repositorio se mantiene público: los informes de clientes, correos, skills con antecedentes internos y binarios históricos quedan locales e ignorados. No se suben paquetes privados a este remoto. Credenciales, entornos Python, dependencias y cachés quedan fuera de Git. El sitio público se despliega desde su carpeta, nunca desde la raíz de este repositorio.

## Generación y despliegue

`npm ci` y `npm run materiales` generan las propuestas desde las imágenes incluidas. En Windows, `herramientas/exportar-office.ps1` exporta PDF con Microsoft PowerPoint; `py -3.12 herramientas/verificar-materiales.py` verifica QR, contactos y formato de corte.

La web se puede previsualizar con un servidor estático. El despliegue de producción requiere la copia local de los informes y sus visores heredados, excluidos del clon público, para conservar enlaces ya entregados. Desde `00_SITIO_WEB_REC/`, usar Vercel CLI para vista previa y, tras revisión independiente, producción en el proyecto existente.
