"""
Descarga los últimos 40 posts de @ventasanacoca y genera catalog.json.

Requiere sesión autenticada. Si no existe, ejecutar primero:
  .venv/bin/python login.py

Uso:
  .venv/bin/python download.py
"""

import json
import os
import sys
import time

import instaloader
from instaloader.exceptions import (
    ConnectionException,
    LoginException,
    QueryReturnedBadRequestException,
)

PROFILE = "ventasanacoca"
USERNAME = "_crisomg"
MAX_POSTS = 40
DELAY_BETWEEN_POSTS = 3  # segundos entre cada descarga para evitar rate limiting
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
PHOTOS_DIR = os.path.join(OUTPUT_DIR, "photos", PROFILE)


def load_existing_catalog() -> dict[str, dict]:
    """Carga catalog.json existente para reanudación."""
    catalog_path = os.path.join(PHOTOS_DIR, "catalog.json")
    if os.path.exists(catalog_path):
        with open(catalog_path, "r", encoding="utf-8") as f:
            items = json.load(f)
            return {item["shortcode"]: item for item in items}
    return {}


def main():
    # Configurar Instaloader
    L = instaloader.Instaloader(
        dirname_pattern=PHOTOS_DIR,
        filename_pattern="{date_utc:%Y-%m-%d}_{shortcode}",
        download_pictures=True,
        download_videos=False,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,
        post_metadata_txt_pattern="",
        max_connection_attempts=3,
    )

    # Cargar sesión autenticada
    try:
        L.load_session_from_file(USERNAME)
    except FileNotFoundError:
        print(f"❌ No se encontró sesión para '{USERNAME}'.")
        print(f"   Ejecuta primero: .venv/bin/python login.py")
        sys.exit(1)

    # Verificar sesión
    test_user = L.test_login()
    if not test_user:
        print("❌ La sesión expiró o es inválida.")
        print("   Ejecuta: .venv/bin/python login.py")
        sys.exit(1)
    print(f"✅ Sesión válida: logueado como '{test_user}'\n")

    # Obtener perfil
    try:
        profile = instaloader.Profile.from_username(L.context, PROFILE)
    except ConnectionException as e:
        print(f"❌ Error al obtener perfil @{PROFILE}: {e}")
        sys.exit(1)

    print(f"📸 Perfil: @{profile.username}")
    print(f"   Posts totales: {profile.mediacount}")
    print(f"   Descargando a: {PHOTOS_DIR}/\n")

    # Cargar catálogo existente para reanudación
    existing = load_existing_catalog()
    if existing:
        print(f"📋 Catálogo existente con {len(existing)} entradas (se reanudará)\n")

    count = 0
    catalog = dict(existing)  # empezar con lo existente
    errors = []

    for post in profile.get_posts():
        if count >= MAX_POSTS:
            break

        shortcode = post.shortcode

        # Si ya fue descargado, solo contar
        if shortcode in catalog:
            count += 1
            print(f"  ⏭️  [{count}/{MAX_POSTS}] {shortcode} (ya existe)")
            continue

        # Descargar
        try:
            L.download_post(post, target=PHOTOS_DIR)
        except (ConnectionException, QueryReturnedBadRequestException) as e:
            error_msg = str(e)
            print(f"  ❌ [{count + 1}/{MAX_POSTS}] {shortcode}: {error_msg}")
            errors.append({"shortcode": shortcode, "error": error_msg})

            if "429" in error_msg or "rate" in error_msg.lower():
                print("\n⏸️  Rate limit alcanzado. Esperando 60 segundos...")
                time.sleep(60)
            continue
        except Exception as e:
            print(f"  ❌ [{count + 1}/{MAX_POSTS}] {shortcode}: {e}")
            errors.append({"shortcode": shortcode, "error": str(e)})
            continue

        filename = f"{post.date_utc.strftime('%Y-%m-%d')}_{shortcode}.jpg"
        catalog[shortcode] = {
            "shortcode": shortcode,
            "url": f"https://www.instagram.com/p/{shortcode}/",
            "caption": post.caption,
            "date": post.date_utc.isoformat(),
            "filename": filename,
        }
        count += 1
        print(f"  ✅ [{count}/{MAX_POSTS}] {shortcode}")

        # Rate limiting preventivo
        if count < MAX_POSTS:
            time.sleep(DELAY_BETWEEN_POSTS)

    # Guardar catálogo (siempre, incluso con errores parciales)
    os.makedirs(PHOTOS_DIR, exist_ok=True)
    catalog_list = sorted(catalog.values(), key=lambda x: x["date"], reverse=True)
    catalog_path = os.path.join(PHOTOS_DIR, "catalog.json")
    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(catalog_list, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}")
    print(f"📊 Resumen:")
    print(f"   Posts en catálogo: {len(catalog_list)}")
    print(f"   Errores: {len(errors)}")
    print(f"   Catálogo: {catalog_path}")

    if errors:
        print(f"\n⚠️  Posts con error (puedes re-ejecutar el script para reintentar):")
        for err in errors:
            print(f"   • {err['shortcode']}: {err['error'][:80]}")


if __name__ == "__main__":
    main()
