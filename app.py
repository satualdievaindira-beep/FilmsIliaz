import os
import urllib.request
from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey_films_iliaz_2026_pro'

# Расширенная база данных
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

# Глобальный шаблон с навигацией
BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8"><title>Films_Iliaz Pro</title>
    <script src="https://quge5.com/88/tag.min.js" data-zone="261051" async></script>
    <style>
        :root { --bg: #0f0f12; --primary: #ff4a5a; --text: #fff; }
        body { background: var(--bg); color: var(--text); font-family: sans-serif; margin: 0; }
        nav { background: #1a1a24; padding: 15px; display: flex; gap: 20px; align-items: center; }
        nav a { color: white; text-decoration: none; font-weight: bold; }
        .hero { padding: 40px; text-align: center; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 20px; padding: 20px; }
        .card { background: #1a1a24; padding: 10px; border-radius: 10px; text-align: center; }
        .card img { width: 100%; border-radius: 8px; }
        .fav-btn { background: var(--primary); border: none; color: white; padding: 5px 10px; cursor: pointer; border-radius: 5px; margin-top: 5px; }
    </style>
</head>
<body>
    <nav>
        <a href="/">ГЛАВНАЯ</a>
        <a href="/top10">ТОП-10 ФИЛЬМОВ</a>
        <a href="/favorites">ИЗБРАННОЕ ({{ session.get('favs', [])|length }})</a>
        <form action="/search" method="GET"><input type="text" name="q" placeholder="Поиск..."></form>
    </nav>
    {% block content %}{% endblock %}
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(BASE_TEMPLATE + """
    {% block content %}
    <div class="hero"><h1>Добро пожаловать в Films_Iliaz Pro</h1></div>
    <div class="grid">
        {% for m in movies %}
        <div class="card">
            <img src="{{ m.poster }}">
            <h3>{{ m.title }}</h3>
            <a href="/add_fav/{{ m.id }}" class="fav-btn">В избранное</a>
        </div>
        {% endfor %}
    </div>
    {% endblock %}
    """, movies=MOVIES)

@app.route('/top10')
def top10():
    top = sorted(MOVIES, key=lambda x: x['rating'], reverse=True)
    return render_template_string(BASE_TEMPLATE + """
    {% block content %}
    <h1>Наши лучшие фильмы</h1>
    <div class="grid">
        {% for m in top %}
        <div class="card"><h3>#{{ loop.index }} {{ m.title }}</h3><p>Рейтинг: {{ m.rating }}</p></div>
        {% endfor %}
    </div>
    {% endblock %}
    """, top=top)

@app.route('/add_fav/<int:mid>')
def add_fav(mid):
    favs = session.get('favs', [])
    if mid not in favs: favs.append(mid)
    session['favs'] = favs
    return redirect('/')

@app.route('/favorites')
def favorites():
    fav_movies = [m for m in MOVIES if m['id'] in session.get('favs', [])]
    return render_template_string(BASE_TEMPLATE + """
    {% block content %}
    <h1>Ваше избранное</h1>
    <div class="grid">
        {% for m in fav_movies %}<div class="card"><h3>{{ m.title }}</h3></div>{% endfor %}
    </div>
    {% endblock %}
    """, fav_movies=fav_movies)

@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    results = [m for m in MOVIES if query in m['title'].lower()]
    return render_template_string(BASE_TEMPLATE + """
    {% block content %}
    <h1>Результаты поиска:</h1>
    <div class="grid">{% for m in results %}<div class="card"><h3>{{ m.title }}</h3></div>{% endfor %}</div>
    {% endblock %}
    """, results=results)

if __name__ == '__main__':
    app.run(debug=True)
