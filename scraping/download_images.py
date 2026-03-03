"""
Descarga las imágenes de los posts listados en catalog.json.
Usa las URLs de imagen capturadas durante el scraping por browser.

Uso:
  .venv/bin/python download_images.py
"""

import json
import os
import time
import urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PHOTOS_DIR = os.path.join(SCRIPT_DIR, "photos", "ventasanacoca")
CATALOG_PATH = os.path.join(PHOTOS_DIR, "catalog.json")

# Mapa de shortcode -> imageUrl (extraídas del browser scraping)
IMAGE_URLS = {
    "DVJwt7_AbEE": "https://scontent-lga3-1.cdninstagram.com/v/t51.82787-15/640416637_18314991985281061_6351441418361381142_n.webp",
    "DVJu6tBgWk_": "https://scontent-lga3-1.cdninstagram.com/v/t51.82787-15/641100506_18314990713281061_3721515555478218047_n.webp",
    "DVGxJqRDbL4": "https://scontent-lga3-2.cdninstagram.com/v/t51.82787-15/641226149_18314853238281061_2689208062379371886_n.webp",
    "DVB9u8Mkc55": "https://scontent-lga3-1.cdninstagram.com/v/t51.82787-15/639863628_18314648368281061_3468625823911735814_n.webp",
    "DVBj8Y4DcaW": "https://scontent-lga3-2.cdninstagram.com/v/t51.82787-15/640930580_18314624929281061_7371164766813211264_n.webp",
    "DU_0m7JgUql": "https://scontent-lga3-2.cdninstagram.com/v/t51.82787-15/632347451_18314548330281061_1522568880039777323_n.webp",
    "DU_ofyxgbLj": "https://scontent-lga3-2.cdninstagram.com/v/t51.82787-15/636205628_18314539939281061_6321775268089843461_n.webp",
    "DUv7kQNEQpw": "https://scontent-lga3-1.cdninstagram.com/v/t51.82787-15/629318423_18313810852281061_6163193178243859763_n.webp",
    "DUoKqM4Ecpk": "https://scontent-lga3-2.cdninstagram.com/v/t51.82787-15/630476742_18313450525281061_7321840211876041085_n.webp",
    "DUoKUzdkV44": "https://scontent-lga3-1.cdninstagram.com/v/t51.82787-15/627572053_18313450225281061_3999982811387886772_n.webp",
    "DUld4WWEeA6": "https://scontent-lga3-1.cdninstagram.com/v/t51.82787-15/627653885_18313340077281061_3086438447639664506_n.jpg",
    "DUdUQ8yEQce": "https://scontent-lga3-1.cdninstagram.com/v/t51.82787-15/627159176_18312992422281061_4278667053664261727_n.webp",
    "DUWM4WVgX0G": "https://scontent-lga3-2.cdninstagram.com/v/t51.82787-15/626221902_18312708811281061_9064850029864525955_n.webp",
    "DUVw-UijZzK": "https://scontent-lga3-1.cdninstagram.com/v/t51.82787-15/628433043_18312685903281061_694482212981604596_n.webp",
    "DUTj84XEYTM": "https://scontent-lga3-1.cdninstagram.com/v/t51.82787-15/626467912_18312606955281061_4620002612820813655_n.webp",
    "DURl2lDDepR": "https://scontent-lga3-1.cdninstagram.com/v/t51.82787-15/627378192_18312522514281061_2331625252268011282_n.webp",
    "DURDjI8gRgb": "https://scontent-lga3-1.cdninstagram.com/v/t51.82787-15/625797586_18312488455281061_3641633831959174582_n.webp",
    "DURCcpeAXnG": "https://scontent-lga3-3.cdninstagram.com/v/t51.82787-15/625458821_18312488008281061_3725257215224316407_n.webp",
    "DUOdCSGkduN": "https://scontent-lga3-2.cdninstagram.com/v/t51.82787-15/624680706_18312324115281061_6322738810496303784_n.jpg",
    "DULN-KNEeTR": "https://scontent-lga3-2.cdninstagram.com/v/t51.82787-15/624565835_18312072292281061_7041920632226967346_n.webp",
    "DUGZK97Ef_d": "https://scontent-lga3-2.cdninstagram.com/v/t51.82787-15/624297028_18311692336281061_7026218144560019476_n.webp",
    "DT-YQu7jvlB": "https://scontent-lga3-2.cdninstagram.com/v/t51.82787-15/621415387_18311144083281061_6484585736153852252_n.webp",
    "DT3IJcfERwm": "https://scontent-lga3-1.cdninstagram.com/v/t51.82787-15/622219339_18310741084281061_3745569077167775509_n.webp",
    "DT0co-nkb15": "https://scontent-lga3-2.cdninstagram.com/v/t51.82787-15/620433211_18310577770281061_5611566731504638575_n.webp",
    "DT0GuMPjW0M": "https://scontent-lga3-1.cdninstagram.com/v/t51.82787-15/620927343_18310557850281061_7863948474960180031_n.webp",
    "DTx2lCqkeLH": "https://scontent-lga3-1.cdninstagram.com/v/t51.82787-15/619506826_18310424887281061_3665903022891884043_n.webp",
    "DTvNuSGjRvu": "https://scontent-lga3-2.cdninstagram.com/v/t51.82787-15/619577898_18310253758281061_5316831280333894799_n.webp",
    "DTikXQFkfHL": "https://scontent-lga3-1.cdninstagram.com/v/t51.82787-15/616315912_18309625357281061_2824481022580697607_n.webp",
    "DTLL5-tEQ6N": "https://scontent-lga3-1.cdninstagram.com/v/t51.82787-15/591555429_18308659825281061_3527183286723688119_n.webp",
    "DTLJ2jsEeNY": "https://scontent-lga3-1.cdninstagram.com/v/t51.82787-15/611648706_18308657896281061_3424700183110963060_n.webp",
    "DSqz6-7jejP": "https://scontent-lga3-3.cdninstagram.com/v/t51.82787-15/605954877_18307170994281061_3877734419285673431_n.webp",
    "DSqzuewDT_p": "https://scontent-lga3-2.cdninstagram.com/v/t51.82787-15/605552423_18307170709281061_7093659469282845728_n.webp",
    "DSnRvIAEU80": "https://scontent-lga3-1.cdninstagram.com/v/t51.82787-15/606379110_18307005361281061_2654984620624312229_n.webp",
    "DSnPZeKETNW": "https://scontent-lga3-1.cdninstagram.com/v/t51.82787-15/605184823_18307003348281061_2048983792914341570_n.webp",
    "DSnFsq8DUnE": "https://scontent-lga3-1.cdninstagram.com/v/t51.82787-15/606074482_18306994558281061_5585394477509107081_n.webp",
    "DSnBYI9jQhh": "https://scontent-lga3-3.cdninstagram.com/v/t51.82787-15/605239680_18306990100281061_9211093532219183892_n.webp",
    "DSIdDq1kX_U": "https://scontent-lga3-2.cdninstagram.com/v/t51.82787-15/598764910_18305667013281061_6539765204819598223_n.webp",
    "DSINbIFjRFa": "https://scontent-lga3-3.cdninstagram.com/v/t51.82787-15/599464022_18305654359281061_8004805905254347131_n.webp",
    "DSGaoRSgUtK": "https://scontent-lga3-1.cdninstagram.com/v/t51.82787-15/589021729_18305575615281061_1208424651233601961_n.webp",
    "DSGWkE3gbux": "https://scontent-lga3-3.cdninstagram.com/v/t51.82787-15/587291054_18305572159281061_7131838628322643793_n.webp",
}


def main():
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    print(f"📸 Descargando {len(catalog)} imágenes a {PHOTOS_DIR}/\n")

    downloaded = 0
    skipped = 0
    errors = []

    for item in catalog:
        shortcode = item["shortcode"]
        filename = item["filename"]
        filepath = os.path.join(PHOTOS_DIR, filename)

        # Saltar si ya existe
        if os.path.exists(filepath):
            skipped += 1
            print(f"  ⏭️  {filename} (ya existe)")
            continue

        url = IMAGE_URLS.get(shortcode)
        if not url:
            print(f"  ⚠️  {shortcode}: sin URL de imagen")
            errors.append(shortcode)
            continue

        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": "https://www.instagram.com/",
            })
            with urllib.request.urlopen(req, timeout=30) as response:
                data = response.read()

            # Detectar extensión real
            content_type = response.headers.get("Content-Type", "")
            if "webp" in content_type or url.endswith(".webp"):
                actual_filename = filename.replace(".jpg", ".webp")
            elif "jpeg" in content_type or "jpg" in content_type:
                actual_filename = filename
            else:
                actual_filename = filename

            actual_path = os.path.join(PHOTOS_DIR, actual_filename)
            with open(actual_path, "wb") as f:
                f.write(data)

            # Actualizar catalog con el nombre real
            item["filename"] = actual_filename

            downloaded += 1
            size_kb = len(data) / 1024
            print(f"  ✅ {actual_filename} ({size_kb:.0f} KB)")

        except Exception as e:
            print(f"  ❌ {shortcode}: {e}")
            errors.append(shortcode)

        time.sleep(0.5)

    # Guardar catálogo actualizado con filenames reales
    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}")
    print(f"📊 Resumen:")
    print(f"   Descargadas: {downloaded}")
    print(f"   Ya existían: {skipped}")
    print(f"   Errores:     {len(errors)}")

    if errors:
        print(f"\n⚠️  Shortcodes con error: {', '.join(errors)}")


if __name__ == "__main__":
    main()
