# Reporte Ejecutivo: Extracción de Catálogo Instagram @ventasanacoca

**Fecha:** 2026-03-03  
**Estado:** Finalizado (Extracción de Datos) / Pendiente (Descarga de Multimedia en Windows)  
**Autor:** Antigravity AI

---

## 1. Resumen Ejecutivo

Se completó con éxito la extracción de metadatos para **40 publicaciones** del perfil comercial `@ventasanacoca`. El proceso enfrentó desafíos técnicos significativos debido a las políticas de seguridad de Instagram y las limitaciones de encriptación entre los entornos WSL (Linux) y Windows.

## 2. Hitos Alcanzados

- **Extracción de Datos:** Generación de `catalog.json` con 40 entradas completas (Shortcode, URL, Caption, Fecha).
- **Consolidación de Identidad:** Verificación del usuario de autenticación (`_crisomg`).
- **Desarrollo de Herramientas:** Creación de scripts especializados para importación de sesiones (`import_session.py`) y descarga resiliente (`download.py`).

## 3. Desafíos Técnicos y Soluciones

| Desafío                     | Detalle                                                               | Solución                                                             |
| :-------------------------- | :-------------------------------------------------------------------- | :------------------------------------------------------------------- |
| **Bloqueo IP/WSL**          | Instagram rechaza el login directo desde entornos virtualizados.      | Pivote a **Browser Scraping** para captura inicial de metadatos.     |
| **Encriptación de Cookies** | Chrome encripta cookies con DPAPI de Windows, inaccesibles desde WSL. | Extracción manual/sandbox del `sessionid` para bypass de seguridad.  |
| **Rate Limiting (429)**     | Instagram limita peticiones tras actividad intensa.                   | Implementación de gestión de reintentos automática en `download.py`. |

## 4. Estado de los Componentes

- [x] **Metadatos (`catalog.json`):** 100% (40/40 posts).
- [x] **Script de Descarga:** Operativo con manejo de sesiones.
- [ ] **Archivos Multimedia (Fotos):** Pendiente descarga final masiva.

## 5. Próximos Pasos (Recomendación Estratégica)

Para finalizar la descarga de las imágenes sin bloqueos, se recomienda mover la ejecución al entorno nativo de **Windows (PowerShell)**:

1. **Entorno:** Usar Python nativo en Windows para permitir que `browser_cookie3` desencripte las cookies de Chrome automáticamente.
2. **Comando Final:**
   ```powershell
   # En PowerShell (Windows)
   pip install instaloader browser_cookie3
   instaloader --load-cookies chrome ventasanacoca
   ```
3. **Integración:** Una vez descargadas las fotos, el catálogo está listo para ser consumido por el frontend de Nuxt 4.

---

_Este documento sirve como registro oficial de la arquitectura de extracción y el estado del proyecto._
