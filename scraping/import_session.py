"""
Importa la sesión de Instagram a Instaloader desde Chrome/Edge de Windows.

El truco en WSL: Chrome bloquea su archivo de cookies mientras está abierto.
Este script soporta 2 modos:

  Modo 1 (automático): Cierra Chrome, ejecuta el script, se leen las cookies directamente.
  Modo 2 (manual):     Exporta tu sessionid cookie manualmente y pásala como argumento.

Uso:
  # Modo 1: Cierra Chrome primero
  .venv/bin/python import_session.py

  # Modo 2: Exportar sessionid manualmente (desde DevTools > Application > Cookies)
  .venv/bin/python import_session.py --sessionid "TU_SESSION_ID_AQUI"

  # Especificar navegador
  .venv/bin/python import_session.py --browser edge
"""

import argparse
import os
import sys
from sqlite3 import OperationalError, connect

import instaloader
from instaloader import ConnectionException

USERNAME = "crisomg"

COOKIE_PATHS = {
    "chrome": "/mnt/c/Users/Administrator/AppData/Local/Google/Chrome/User Data/Default/Network/Cookies",
    "edge": "/mnt/c/Users/Administrator/AppData/Local/Microsoft/Edge/User Data/Default/Network/Cookies",
}


def import_from_sessionid(sessionid: str) -> None:
    """Importa sesión usando solo el sessionid cookie."""
    print("🔑 Usando sessionid proporcionado...")

    L = instaloader.Instaloader(max_connection_attempts=1)
    L.context._session.cookies.set("sessionid", sessionid, domain=".instagram.com")

    test_user = L.test_login()
    if not test_user:
        print("❌ El sessionid no es válido o expiró.")
        sys.exit(1)

    L.context.username = test_user
    L.save_session_to_file()
    print(f"\n✅ Sesión importada para '{test_user}'")
    print(f"   Guardada en: ~/.config/instaloader/session-{test_user}")


def import_from_cookie_file(cookiefile: str) -> None:
    """Importa cookies del archivo SQLite de Chrome/Edge."""
    print(f"📂 Leyendo cookies de: {cookiefile}")

    if not os.path.exists(cookiefile):
        print(f"❌ Archivo no encontrado: {cookiefile}")
        sys.exit(1)

    # Intentar copia temporal (por si Chrome está cerrado pero permisos WSL)
    tmp_copy = "/tmp/browser_cookies_copy.sqlite"
    try:
        import shutil
        shutil.copy2(cookiefile, tmp_copy)
        db_path = tmp_copy
        print("   Copia temporal creada OK")
    except (PermissionError, OSError):
        # Intentar lectura directa
        db_path = cookiefile

    try:
        conn = connect(f"file:{db_path}?immutable=1", uri=True)
    except Exception:
        try:
            conn = connect(db_path)
        except Exception as e:
            print(f"❌ No se pudo abrir la base de datos: {e}")
            print("\n📋 Chrome probablemente está abierto. Tienes 2 opciones:")
            print("   1. Cierra Chrome completamente y ejecuta de nuevo")
            print("   2. Usa --sessionid (ver instrucciones abajo)")
            print_sessionid_instructions()
            sys.exit(1)

    try:
        cookie_data = conn.execute(
            "SELECT name, value FROM cookies WHERE host_key LIKE '%instagram.com'"
        ).fetchall()
        cookies = {name: value for name, value in cookie_data if value}
    except OperationalError as e:
        print(f"❌ Error leyendo cookies: {e}")
        print_sessionid_instructions()
        sys.exit(1)
    finally:
        conn.close()

    if "sessionid" not in cookies or not cookies["sessionid"]:
        print("❌ No hay sesión de Instagram activa en este navegador.")
        print("   Inicia sesión en instagram.com y vuelve a intentar.")
        sys.exit(1)

    print(f"   Encontradas {len(cookies)} cookies de Instagram")

    L = instaloader.Instaloader(max_connection_attempts=1)
    L.context._session.cookies.update(
        {k: v for k, v in cookies.items()}
    )

    test_user = L.test_login()
    if not test_user:
        print("❌ Las cookies no son válidas.")
        sys.exit(1)

    L.context.username = test_user
    L.save_session_to_file()
    print(f"\n✅ Sesión importada para '{test_user}'")
    print(f"   Guardada en: ~/.config/instaloader/session-{test_user}")


def print_sessionid_instructions():
    """Imprime instrucciones para exportar sessionid manualmente."""
    print("\n" + "=" * 60)
    print("📋 CÓMO OBTENER TU SESSIONID MANUALMENTE:")
    print("=" * 60)
    print("   1. Abre Chrome y ve a instagram.com (logueado)")
    print("   2. Presiona F12 (DevTools)")
    print("   3. Ve a Application > Cookies > instagram.com")
    print("   4. Busca la cookie 'sessionid'")
    print("   5. Copia su valor (Value)")
    print("   6. Ejecuta:")
    print('   .venv/bin/python import_session.py --sessionid "TU_VALOR"')
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Importar sesión de Instagram desde Chrome/Edge de Windows"
    )
    parser.add_argument(
        "--browser", "-b", choices=["chrome", "edge"], default="chrome",
        help="Navegador (default: chrome)"
    )
    parser.add_argument(
        "--sessionid", "-s",
        help="sessionid cookie de Instagram (modo manual)"
    )
    parser.add_argument(
        "--cookiefile", "-c",
        help="Ruta personalizada al archivo de cookies"
    )
    args = parser.parse_args()

    print(f"🔑 Importando sesión de Instagram...\n")

    # Modo manual con sessionid
    if args.sessionid:
        import_from_sessionid(args.sessionid)
        return

    # Modo automático con archivo de cookies
    cookiefile = args.cookiefile or COOKIE_PATHS.get(args.browser)
    if cookiefile:
        try:
            import_from_cookie_file(cookiefile)
            return
        except (ConnectionException,) as e:
            print(f"⚠️  Error de conexión: {e}")

    print("❌ No se pudo importar la sesión automáticamente.")
    print_sessionid_instructions()
    sys.exit(1)


if __name__ == "__main__":
    main()
