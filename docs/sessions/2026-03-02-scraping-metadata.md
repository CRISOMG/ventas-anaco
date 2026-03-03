# Sesión: Agregar metadatos al script de scraping

**Fecha:** 2026-03-02

## Objetivo

Agregar generación de `catalog.json` al script `scraping/download.py` para capturar metadatos de cada post (caption, shortcode, fecha, URL permanente) necesarios para construir el catálogo de productos en Nuxt 4.

## Estado actual

- **✅ catalog.json generado** con 40 posts via browser scraping
- **✅ Sesión de Instaloader importada** (usuario `_crisomg`)
- **⏳ Descarga de imágenes** — esperando a que pase el rate limit 429

## Cronología de problemas y soluciones

### 1. `interactive_login()` → Error `"fail" status`

Instagram bloquea logins programáticos desde IPs no reconocidas.
Problema conocido de Instaloader (Issues #92, #615, #1150, #1217).

### 2. Importar cookies de Chrome desde WSL → Valores encriptados

Chrome encripta las cookies con DPAPI de Windows. Desde WSL los valores se leen vacíos.
`browser_cookie3` tampoco funciona en WSL porque busca Chrome en paths de Linux.

### 3. Solución: Extraer sessionid desde el browser sandbox

Se usó el browser sandbox de Antigravity para:

1. Iniciar sesión manualmente en Instagram
2. Interceptar el `sessionid` de las cabeceras HTTP de red
3. Importarlo a Instaloader con `import_session.py --sessionid`

```bash
# Comando que funcionó:
.venv/bin/python import_session.py --sessionid "1517554455%3A..."
# Output: ✅ Sesión importada para '_crisomg'
```

### 4. Rate limit 429 al ejecutar `download.py`

Después del browser scraping intensivo (40+ páginas visitadas), Instagram aplica rate limit.
Instaloader maneja esto automáticamente con retry después de 30 minutos.

## Nota: username correcto

El username de Instagram es `_crisomg` (con guión bajo al inicio), no `crisomg`.
Esto se descubrió al importar la sesión via sessionid.

## Archivos

| Archivo                                      | Descripción                                              |
| -------------------------------------------- | -------------------------------------------------------- |
| `scraping/import_session.py`                 | Importar cookies a Instaloader (soporta --sessionid)     |
| `scraping/login.py`                          | Login interactivo (no funciona desde WSL)                |
| `scraping/download.py`                       | Descargar posts + generar catálogo (USERNAME=`_crisomg`) |
| `scraping/download_images.py`                | Descarga imágenes por URL CDN (no funciona, 403)         |
| `scraping/photos/ventasanacoca/catalog.json` | ✅ 40 posts con metadatos                                |

## Cómo reproducir

```bash
cd scraping

# 1. Importar sesión (si se necesita renovar)
.venv/bin/python import_session.py --sessionid "TU_SESSION_ID"

# 2. Descargar posts e imágenes
.venv/bin/python download.py
```

## Lecciones aprendidas

- `instaloader.interactive_login()` no funciona desde WSL/IPs desconocidas
- Chrome encripta cookies con DPAPI → inaccesible desde WSL
- `browser_cookie3` no funciona en WSL (busca Chrome en paths Linux)
- La solución más confiable: extraer sessionid manualmente o via browser DevTools
- El sessionid cookie es `HttpOnly`, no accesible via `document.cookie`; se extrae de headers HTTP
- URLs CDN de Instagram (`scontent-*.cdninstagram.com`) requieren tokens de auth y expiran rápidamente
- Instaloader maneja 429 rate limits automáticamente con reintentos
