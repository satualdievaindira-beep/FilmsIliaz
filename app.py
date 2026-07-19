import os
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# База данных
MOVIES = [
    {"id": 1, "title": "Аватар", "genre": "Фантастика", "poster": "https://kinogo.my/uploads/posts/2017-04/1493391756-1159271017-avatar.jpg", "rating": 7.9},
    {"id": 2, "title": "Властелин колец", "genre": "Фантастика", "poster": "https://kinogo.my/uploads/posts/2019-07/1563720942-490328414-vlastelin-kolec-bratstvo-kolca.jpg", "rating": 8.6},
    {"id": 3, "title": "Интерстеллар", "genre": "Фантастика", "poster": "https://kinogo.my/uploads/posts/2017-04/1491114790-991695033-interstellar.jpg", "rating": 8.6},
    {"id": 4, "title": "Начало", "genre": "Фантастика", "poster": "https://kinogo.my/uploads/posts/2017-04/1491114986-2049908774-nachalo.jpg", "rating": 8.7},
    {"id": 5, "title": "Темный рыцарь", "genre": "Боевики", "poster": "https://kinogo.my/uploads/posts/2020-03/1585250490_the-dark-knight-2008.jpg", "rating": 8.5},
    {"id": 6, "title": "Гладиатор", "genre": "Боевики", "poster": "https://kinogo.my/uploads/posts/2019-11/1574343110_gladiator-2000.jpg", "rating": 8.6},
    {"id": 7, "title": "Маска", "genre": "Комедии", "poster": "https://kinogo.my/uploads/posts/2023-11/1699995824-1618804087-maska.jpg", "rating": 8.0},
    {"id": 8, "title": "Сияние", "genre": "Ужасы", "poster": "https://kinogo.my/uploads/posts/2024-01/1704798751-1904935975-siyanie.jpg", "rating": 8.4},
    {"id": 9, "title": "Матрица", "genre": "Фантастика", "poster": "https://kinogo.my/uploads/posts/2020-01/1578316075-753251593-matrica.jpg", "rating": 8.5},
    {"id": 10, "title": "Гарри Поттер", "genre": "Фантастика", "poster": "https://kinogo.my/uploads/posts/2019-07/1563015062-1572996915-garri-potter-i-filosofskiy-kamen.jpg", "rating": 8.2},
]

# Общий HTML с рекламой
def get_html(content):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Films_Iliaz Pro</title>
        <script src="https://quge5.com/88/tag.min.js" data-zone="261051" async></script>
        <style>
            body {{ background: #0f0f12; color: white; font-family: sans-serif; margin: 0; }}
            nav {{ background: #1a1a24; padding: 15px; display: flex; gap: 15px; }}
            nav a {{ color: white; text-decoration: none; font-weight: bold; }}
            .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 20px; padding: 20px; }}
            .card {{ background: #1a1a24; padding: 10px; border-radius: 10px; text-align: center; }}
            .card img {{ width: 100%; border-radius: 8px; }}
        </style>
    </head>
    <body>
        <nav>
            <a href="/">Главная</a>
            <a href="/top10">Топ-10</a>
            <form action="/search" method="GET"><input type="text" name="q" placeholder="Поиск..."></form>
        </nav>
        {content}
    </body>
    </html>
    """

@app.route('/')
def index():
    grid = "".join([f'<div class="card"><img src="{m["poster"]}"><h3>{m["title"]}</h3></div>' for m in MOVIES])
    return render_template_string(get_html(f'<div class="grid">{grid}</div>'))

@app.route('/top10')
def top10():
    top = sorted(MOVIES, key=lambda x: x['rating'], reverse=True)
    grid = "".join([f'<div class="card"><h3>{m["title"]}</h3><p>Рейтинг: {m["rating"]}</p></div>' for m in top])
    return render_template_string(get_html(f'<h1>Лучшие фильмы</h1><div class="grid">{grid}</div>'))

@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    results = [m for m in MOVIES if query in m['title'].lower()]
    grid = "".join([f'<div class="card"><img src="{m["poster"]}"><h3>{m["title"]}</h3></div>' for m in results])
    return render_template_string(get_html(f'<h1>Результаты поиска</h1><div class="grid">{grid}</div>'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
