import asyncio
import json
import os
from datetime import datetime
from playwright.async_api import async_playwright

async def run_instagram_macro(max_posts=None, target_date_str=None, start_from_shortcode=None):
    # Parsear la fecha objetivo si se proporcionó
    target_date = None
    if target_date_str:
        target_date = datetime.strptime(target_date_str, "%d-%m-%Y")
        print(f"📅 Límite de fecha activado: Solo posts desde hoy hasta {target_date.strftime('%d/%m/%Y')}")

    if max_posts:
        print(f"🔢 Límite de posts activado: Máximo {max_posts} posts")
        
    if start_from_shortcode:
        print(f"🏁 Límite de inicio activado: Saltando hasta encontrar {start_from_shortcode}")

    found_start_post = False if start_from_shortcode else True

    async with async_playwright() as p:
        try:
            # 1. Conectar a la sesión del usuario (debe existir un Chrome en puerto 9222)
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
            print("🔗 Conectado a Chrome (puerto 9222)")
            
            context = browser.contexts[0]
            pages = context.pages
            
            # Buscar la página del perfil en las pestañas abiertas
            profile_page = None
            for page in pages:
                if "instagram.com" in page.url and "/p/" not in page.url:
                    profile_page = page
                    break
                    
            if not profile_page:
                print("❌ No se encontró una pestaña con el perfil de Instagram (grid view).")
                print("⚠️ Por favor, abre el perfil de Instagram en una pestaña (Ej: instagram.com/ventasanacoca)")
                return

            await profile_page.bring_to_front()
            print(f"📄 Macro iniciada en: {profile_page.url}")
            
            output_file = "marketing_macro_results.json"
            data = {"posts": {}}
            processed_hrefs = set()
            
            # Cargar estado anterior para reanudar si falló o paramos
            if os.path.exists(output_file):
                try:
                    with open(output_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        for _, info in data.get("posts", {}).items():
                            if "url" in info:
                                href_str = info["url"].replace("https://www.instagram.com", "")
                                processed_hrefs.add(href_str)
                    print(f"📦 Cargados {len(processed_hrefs)} posts anteriores para reanudar y omitir repetidos.")
                except Exception as e:
                    print(f"⚠️ Error cargando backup: {e}")

            posts_processed_count = 0
            should_stop = False
            
            while not should_stop:
                # Extraemos primero SOLO los links en texto usando JS, para que Playwright
                # no crashee por "Element is not attached to the DOM" si la página se actualiza sola.
                hrefs_in_view = await profile_page.evaluate('''() => {
                    const anchors = document.querySelectorAll('a[href*="/p/"]');
                    return Array.from(anchors).map(a => a.getAttribute('href'));
                }''')
                
                new_posts_found = False
                
                for href in hrefs_in_view:
                    if not href or href in processed_hrefs:
                        continue
                        
                    new_posts_found = True
                    
                    # Verificación del punto de inicio
                    if not found_start_post:
                        shortcode_in_view = href.split('/p/')[1].split('/')[0]
                        if shortcode_in_view == start_from_shortcode:
                            print(f"\n🎯 Punto de inicio encontrado ({start_from_shortcode}). Comenzando extracción de aquí en adelante...")
                            found_start_post = True
                        else:
                            # Lo marcamos como "procesado" silenciosamente para saltarlo en el grid
                            processed_hrefs.add(href)
                            continue
                    
                    # Comprobar límite de máxima cantidad
                    if max_posts is not None and posts_processed_count >= max_posts:
                        print("\n🛑 Límite de cantidad de posts alcanzado.")
                        should_stop = True
                        break
                    
                    print(f"\n⏳ [{posts_processed_count+1}] Procesando: {href}")
                    
                    # --- A. HOVER: Obtener Likes y Comentarios del Grid ---
                    # Generamos el locator al momento, para no tener elementos huérfanos
                    post_loc = profile_page.locator(f'a[href="{href}"]').first
                    await post_loc.scroll_into_view_if_needed()
                    await profile_page.wait_for_timeout(500) # Pausa humanizada
                    await post_loc.hover()
                    await profile_page.wait_for_timeout(1000) # Esperar animación de overlay
                    
                    grid_stats = await post_loc.evaluate('''(el) => {
                        let likes = "0", comments = "0";
                        const listItems = el.querySelectorAll('li');
                        if(listItems.length >= 2) {
                            likes = listItems[0].innerText || "0";
                            comments = listItems[1].innerText || "0";
                        } else {
                            const spans = el.querySelectorAll('span');
                            let values = [];
                            spans.forEach(s => { 
                                if(s.innerText.trim().length > 0 && !isNaN(parseInt(s.innerText))) {
                                    values.push(s.innerText);
                                }
                            });
                            if(values.length >= 2) {
                                likes = values[0];
                                comments = values[1];
                            }
                        }
                        return { likes, comments };
                    }''')
                    
                    print(f"   Hover -> Likes: {grid_stats['likes']}, Comments: {grid_stats['comments']}")
                    
                    # --- B. CLICK: Abrir Modal de Detalles ---
                    await post_loc.click()
                    
                    try:
                        await profile_page.wait_for_selector('[role="dialog"]', timeout=5000)
                        await profile_page.wait_for_timeout(1500) # Tiempo de carga de comentarios
                    except Exception:
                        print("   ⚠️ Modal no cargó o tardó demasiado.")
                        await profile_page.keyboard.press('Escape')
                        # Lo marcamos procesado de todas formas para no entrar en loop infinito
                        processed_hrefs.add(href)
                        continue
                    
                    # --- C. EXTRACCIÓN MODAL Y TIMESTAMP ---
                    modal_stats = await profile_page.evaluate('''() => {
                        let caption = "";
                        let rootCommentsCount = 0;
                        let timestamp = null;
                        
                        const dialog = document.querySelector('[role="dialog"]');
                        if (!dialog) return { caption, rootCommentsCount, timestamp };

                        // Timestamp
                        const timeEl = document.querySelector('time');
                        if (timeEl) timestamp = timeEl.getAttribute('datetime');

                        // Caption
                        const h1 = dialog.querySelector("h1");
                        if (h1) caption = h1.innerText;

                        // Root comments
                        const uls = dialog.querySelectorAll("ul");
                        for (let ul of uls) {
                            const lis = Array.from(ul.children).filter(child => child.tagName === "LI");
                            if (lis.length > 0) {
                                rootCommentsCount = Math.max(0, lis.length - 1); 
                                break; 
                            }
                        }
                        
                        return { caption, rootCommentsCount, timestamp };
                    }''')
                    
                    # --- D. CERRAR MODAL ---
                    await profile_page.keyboard.press('Escape')
                    await profile_page.wait_for_timeout(1000)
                    
                    # Validar el límite de fecha ANTES de agregarlo a nuestra data
                    if target_date and modal_stats['timestamp']:
                        # Parseamos la fecha del post tomando la parte de YYYY-MM-DDTHH:MM:SS
                        # Ej instgram: "2024-02-14T18:47:26.000Z"
                        time_str_clean = modal_stats['timestamp'].split('.')[0]
                        post_date = datetime.strptime(time_str_clean, "%Y-%m-%dT%H:%M:%S")
                        
                        if post_date < target_date:
                            print(f"\n🛑 Fecha límite alcanzada. El post {href} es del {post_date.strftime('%d/%m/%Y')} (Anterior al límite).")
                            should_stop = True
                            break # No guardamos este post, terminamos la macro

                    # Extraer el shortcode limpio del href (Ej: /p/ABCDEFG/ -> ABCDEFG)
                    shortcode = href.split('/p/')[1].split('/')[0]

                    # Guardar al diccionario usando el shortcode como Keyword Map
                    data["posts"][shortcode] = {
                        "url": f"https://www.instagram.com{href}",
                        "grid_likes": grid_stats['likes'],
                        "grid_comments": grid_stats['comments'],
                        "caption": modal_stats['caption'],
                        "root_comments_count": modal_stats['rootCommentsCount'],
                        "timestamp": modal_stats['timestamp'],
                        "shortcode": shortcode
                    }
                    
                    print(f"   Modal -> Comentarios Padre: {modal_stats['rootCommentsCount']}")
                    cleaned_caption = modal_stats['caption'].replace('\\n', ' ')[:40]
                    print(f"   Date  -> {modal_stats['timestamp']}")
                    
                    # GUARDADO EN TIEMPO REAL: Por cada iteración salvamos. 
                    # Así, si la macro falla, no perdemos nada!
                    with open(output_file, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                        
                    processed_hrefs.add(href)
                    posts_processed_count += 1
                
                # Si terminamos el for break normal pero no hay que parar la macro... hacemos un scroll
                if not should_stop:
                    if not new_posts_found:
                        print("\n🏁 No hay más posts para scrollear. Fin del grid.")
                        should_stop = True
                    else:
                        print("\n⏬ Scrolleando para cargar más posts...")
                        await profile_page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                        await profile_page.wait_for_timeout(3000) # Dar tiempo a que cargue IG los nuevos posts

            print(f"\n✨ Macro completada. ({posts_processed_count} posts NUEVOS procesados)")

        except Exception as e:
            print(f"❌ Error crítico en la macro: {e}")

if __name__ == "__main__":
    
    # ==========================================
    # ⚙️ CONFIGURACIONES DE LA MACRO
    # ==========================================
    
    # 1. Cantidad máxima de posts a evaluar. Coloca None para ignorar.
    # Ejemplo: MAX_POSTS = 5 (Solo procesa los primeros 5)
    MAX_POSTS = None
    
    # 2. Extraer todos hasta una fecha en específico. Coloca None para ignorar.
    # Formato: "DD-MM-YYYY". Ejemplo: "20-09-2025" 
    TARGET_DATE = "20-09-2025" 
    
    # 3. Empezar a escanear a partir de un post en específico (shortcode). Coloca None para ignorar.
    START_FROM_SHORTCODE = "DSqz6-7jejP"

    asyncio.run(run_instagram_macro(
        max_posts=MAX_POSTS, 
        target_date_str=TARGET_DATE, 
        start_from_shortcode=START_FROM_SHORTCODE
    ))
