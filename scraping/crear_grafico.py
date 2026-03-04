import json
import os
from datetime import datetime
from collections import defaultdict

# 1. Leer el archivo JSON
json_path = os.path.join(os.path.dirname(__file__), '..', 'marketing_macro_results.json')
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# ==========================================
# PROCESAMIENTO: GRÁFICO DIARIO
# ==========================================
daily_posts = []
for post_id, info in data.get("posts", {}).items():
    if info.get("timestamp"):
        try:
            date_obj = datetime.strptime(info["timestamp"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
            likes = int(info.get("grid_likes", 0))
            comments = int(info.get("grid_comments", 0))
            
            daily_posts.append({
                "shortcode": info.get("shortcode", post_id),
                "date_label": date_obj.strftime("%d/%m/%Y"),
                "timestamp_sort": date_obj.timestamp(),
                "likes": likes,
                "comments": comments,
                "interactions": likes + comments
            })
        except Exception as e:
            print(f"Daily: No se pudo parsear fecha para {post_id}: {e}")

daily_posts.sort(key=lambda x: x["timestamp_sort"])

daily_labels = [p["date_label"] for p in daily_posts]
daily_likes = [p["likes"] for p in daily_posts]
daily_comments = [p["comments"] for p in daily_posts]
daily_interactions = [p["interactions"] for p in daily_posts]
daily_shortcodes = [p["shortcode"] for p in daily_posts]

html_daily = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rendimiento Diario - Ventas Anaco</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; margin: 0; padding: 20px; }}
        .container {{ width: 90%; max-width: 1200px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
        h1 {{ text-align: center; color: #333; }}
        .summary {{ display: flex; justify-content: space-around; margin-bottom: 20px; }}
        .stat-box {{ background: #e0f7fa; padding: 15px; border-radius: 8px; text-align: center; width: 30%; }}
        .stat-box h3 {{ margin: 0; color: #006064; }}
        .stat-box p {{ font-size: 24px; margin: 5px 0 0 0; font-weight: bold; color: #00838f; }}
        .nav-link {{ display: block; text-align: center; margin-bottom: 20px; font-weight: bold; color: #00838f; text-decoration: none; }}
        .nav-link:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Rendimiento de Publicaciones (Time Series - Por Post/Día)</h1>
        <a href="rendimiento_semanal.html" class="nav-link">👉 Ver Gráfico Semanal</a>
        
        <div class="summary">
            <div class="stat-box">
                <h3>Total Posts Analizados</h3>
                <p>{len(daily_posts)}</p>
            </div>
            <div class="stat-box">
                <h3>Total Interacciones</h3>
                <p>{sum(daily_interactions)}</p>
            </div>
        </div>

        <canvas id="dailyChart" height="100"></canvas>
    </div>

    <script>
        const ctxDaily = document.getElementById('dailyChart').getContext('2d');
        new Chart(ctxDaily, {{
            type: 'bar',
            data: {{
                labels: {daily_labels},
                datasets: [
                    {{
                        type: 'line',
                        label: 'Interacciones Totales (Tendencia)',
                        data: {daily_interactions},
                        borderColor: 'rgba(255, 99, 132, 1)',
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderWidth: 2,
                        tension: 0.3,
                        fill: false
                    }},
                    {{
                        type: 'bar',
                        label: 'Likes',
                        data: {daily_likes},
                        backgroundColor: 'rgba(54, 162, 235, 0.6)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }},
                    {{
                        type: 'bar',
                        label: 'Comentarios',
                        data: {daily_comments},
                        backgroundColor: 'rgba(255, 206, 86, 0.6)',
                        borderColor: 'rgba(255, 206, 86, 1)',
                        borderWidth: 1
                    }}
                ]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    tooltip: {{
                        callbacks: {{
                            footer: function(tooltipItems) {{
                                const index = tooltipItems[0].dataIndex;
                                const shortcodes = {daily_shortcodes};
                                return 'Post ID: ' + shortcodes[index];
                            }}
                        }}
                    }},
                    title: {{ display: true, text: 'Evolución de Interacciones (Más antiguo -> Más reciente)' }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""

# ==========================================
# PROCESAMIENTO: GRÁFICO SEMANAL
# ==========================================
weekly_data_map = defaultdict(lambda: {'posts': 0, 'likes': 0, 'start_date': None})

for post_id, info in data.get("posts", {}).items():
    if info.get("timestamp"):
        try:
            date_obj = datetime.strptime(info["timestamp"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
            iso_year, iso_week, _ = date_obj.isocalendar()
            week_label = f"Semana {iso_week} ({iso_year})"
            
            likes = int(info.get("grid_likes", 0))
            
            weekly_data_map[week_label]['posts'] += 1
            weekly_data_map[week_label]['likes'] += likes
            
            if not weekly_data_map[week_label]['start_date']:
                start_of_week = datetime.strptime(f"{iso_year}-W{iso_week}-1", "%G-W%V-%u")
                weekly_data_map[week_label]['start_date'] = start_of_week.timestamp()
                
        except Exception as e:
            print(f"Weekly: No se pudo parsear fecha para {post_id}: {e}")

weekly_posts = []
for label, stats in weekly_data_map.items():
    weekly_posts.append({
        "week_label": label,
        "posts_count": stats['posts'],
        "total_likes": stats['likes'],
        "timestamp_sort": stats['start_date'] or 0
    })

weekly_posts.sort(key=lambda x: x["timestamp_sort"])

weekly_labels = [p["week_label"] for p in weekly_posts]
weekly_likes = [p["total_likes"] for p in weekly_posts]
weekly_posts_count = [p["posts_count"] for p in weekly_posts]

html_weekly = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rendimiento Semanal - Ventas Anaco</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; margin: 0; padding: 20px; }}
        .container {{ width: 90%; max-width: 1200px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
        h1 {{ text-align: center; color: #333; }}
        .summary {{ display: flex; justify-content: space-around; margin-bottom: 20px; }}
        .stat-box {{ background: #e0f7fa; padding: 15px; border-radius: 8px; text-align: center; width: 30%; }}
        .stat-box h3 {{ margin: 0; color: #006064; }}
        .stat-box p {{ font-size: 24px; margin: 5px 0 0 0; font-weight: bold; color: #00838f; }}
        .nav-link {{ display: block; text-align: center; margin-bottom: 20px; font-weight: bold; color: #00838f; text-decoration: none; }}
        .nav-link:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Rendimiento de Publicaciones (Por Semana)</h1>
        <a href="rendimiento_diario.html" class="nav-link">👉 Ver Gráfico Diario</a>
        
        <div class="summary">
            <div class="stat-box">
                <h3>Total Posts</h3>
                <p>{sum(weekly_posts_count)}</p>
            </div>
            <div class="stat-box">
                <h3>Total Likes</h3>
                <p>{sum(weekly_likes)}</p>
            </div>
        </div>

        <canvas id="weeklyChart" height="100"></canvas>
    </div>

    <script>
        const ctxWeekly = document.getElementById('weeklyChart').getContext('2d');
        new Chart(ctxWeekly, {{
            type: 'bar',
            data: {{
                labels: {weekly_labels},
                datasets: [
                    {{
                        type: 'line',
                        label: 'Total Likes',
                        data: {weekly_likes},
                        borderColor: 'rgba(255, 99, 132, 1)',
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderWidth: 2,
                        tension: 0.3, 
                        fill: true,
                        yAxisID: 'y'
                    }},
                    {{
                        type: 'bar',
                        label: 'Cantidad de Posts',
                        data: {weekly_posts_count},
                        backgroundColor: 'rgba(54, 162, 235, 0.6)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1,
                        yAxisID: 'y1'
                    }}
                ]
            }},
            options: {{
                responsive: true,
                interaction: {{ mode: 'index', intersect: false }},
                plugins: {{ title: {{ display: true, text: 'Cantidad de Publicaciones vs Likes Totales por Semana' }} }},
                scales: {{
                    y: {{ type: 'linear', display: true, position: 'left', title: {{ display: true, text: 'Total Likes' }} }},
                    y1: {{
                        type: 'linear', display: true, position: 'right', beginAtZero: true,
                        grid: {{ drawOnChartArea: false }},
                        title: {{ display: true, text: 'Cantidad de Posts' }},
                        ticks: {{ stepSize: 1 }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""

# ==========================================
# GUARDAR ARCHIVOS
# ==========================================
daily_path = os.path.join(os.path.dirname(__file__), '..', 'rendimiento_diario.html')
weekly_path = os.path.join(os.path.dirname(__file__), '..', 'rendimiento_semanal.html')

with open(daily_path, "w", encoding="utf-8") as f:
    f.write(html_daily)

with open(weekly_path, "w", encoding="utf-8") as f:
    f.write(html_weekly)

print(f"✨ ¡Gráficos generados exitosamente!")
print(f"📈 Diario: {daily_path}")
print(f"📉 Semanal: {weekly_path}")
