"""
Script para crear y guardar sesión de Instagram con Instaloader.
Maneja 2FA, challenges, y errores de login con diagnóstico claro.

Uso:
  .venv/bin/python login.py
  .venv/bin/python login.py --username otro_usuario
"""

import argparse
import getpass
import sys

import instaloader
from instaloader.exceptions import (
    BadCredentialsException,
    ConnectionException,
    LoginException,
    TwoFactorAuthRequiredException,
)


def create_session(username: str) -> None:
    L = instaloader.Instaloader()

    password = getpass.getpass(f"Contraseña de Instagram para {username}: ")

    try:
        L.login(username, password)
    except TwoFactorAuthRequiredException:
        print("\n🔐 Se requiere verificación 2FA.")
        while True:
            code = input("Código 2FA (de tu app de autenticación): ").strip()
            if not code:
                continue
            try:
                L.two_factor_login(code)
                break
            except BadCredentialsException:
                print("❌ Código inválido, intenta de nuevo.")
    except BadCredentialsException:
        print("❌ Contraseña incorrecta.")
        sys.exit(1)
    except LoginException as e:
        error_msg = str(e)
        print(f"\n❌ Error de login: {error_msg}")
        if "Checkpoint required" in error_msg:
            print("\n📋 Instagram requiere verificación manual:")
            print("   1. Abre Instagram en tu navegador o celular")
            print("   2. Completa la verificación de seguridad")
            print("   3. Vuelve a ejecutar este script")
        elif '"fail"' in error_msg:
            print("\n📋 Instagram rechazó el login. Posibles causas:")
            print("   • La contraseña es incorrecta")
            print("   • Instagram bloqueó logins desde esta IP/dispositivo")
            print("   • Tu cuenta tiene restricciones temporales")
            print("\n   Soluciones:")
            print("   1. Verifica tu contraseña en instagram.com")
            print("   2. Revisa los correos de seguridad de Instagram")
            print("   3. Intenta de nuevo después de unos minutos")
            print("   4. Si tienes 2FA, asegúrate de que esté correctamente configurada")
        else:
            print("\n   Intenta de nuevo más tarde.")
        sys.exit(1)
    except ConnectionException as e:
        print(f"❌ Error de conexión: {e}")
        print("   Verifica tu conexión a internet e intenta de nuevo.")
        sys.exit(1)

    # Guardar sesión
    L.save_session_to_file()
    print(f"\n✅ Sesión guardada exitosamente para '{username}'")
    print(f"   Ubicación: ~/.config/instaloader/session-{username}")

    # Verificar que funciona
    try:
        test_user = L.test_login()
        if test_user:
            print(f"   Verificación: logueado como '{test_user}'")
        else:
            print("   ⚠️  No se pudo verificar la sesión, pero fue guardada.")
    except Exception:
        print("   ⚠️  No se pudo verificar la sesión, pero fue guardada.")


def main():
    parser = argparse.ArgumentParser(description="Login de Instagram con Instaloader")
    parser.add_argument("--username", "-u", default="crisomg", help="Usuario de Instagram (default: crisomg)")
    args = parser.parse_args()

    print(f"🔑 Iniciando sesión como '{args.username}'...\n")
    create_session(args.username)


if __name__ == "__main__":
    main()
