import os
from flask import Flask, render_template_string, request

app = Flask(__name__)

# База данных фильмов с твоими картинками
MOVIES = [
    {"id": 1, "title": "Аватар", "poster": "https://kinogo.my/uploads/posts/2017-04/1493391756-1159271017-avatar.jpg", "rating": 7.9, "kp_url": "https://www.kinopoisk.ru/film/251733/"},
    {"id": 2, "title": "Властелин колец", "poster": "https://kinogo.my/uploads/posts/2019-07/1563720942-490328414-vlastelin-kolec-bratstvo-kolca.jpg", "rating": 8.6, "kp_url": "https://www.kinopoisk.ru/film/328/"},
    {"id": 3, "title": "Интерстеллар", "poster": "https://kinogo.my/uploads/posts/2017-04/1491114790-991695033-interstellar.jpg", "rating": 8.6, "kp_url": "https://www.kinopoisk.ru/film/258687/"},
    {"id": 4, "title": "Начало", "poster": "https://kinogo.my/uploads/posts/2017-04/1491114986-2049908774-nachalo.jpg", "rating": 8.7, "kp_url": "https://www.kinopoisk.ru/film/447301/"},
    {"id": 5, "title": "Темный рыцарь", "poster": "https://kinogo.my/uploads/posts/2020-03/1585250490_the-dark-knight-2008.jpg", "rating": 8.5, "kp_url": "https://www.kinopoisk.ru/film/111543/"},
    {"id": 6, "title": "Матрица", "poster": "https://kinogo.my/uploads/posts/2020-01/1578316075-753251593-matrica.jpg", "rating": 8.5, "kp_url": "https://www.kinopoisk.ru/film/301/"},
    {"id": 7, "title": "Гладиатор", "poster": "https://kinogo.my/uploads/posts/2019-11/1574343110_gladiator-2000.jpg", "rating": 8.6, "kp_url": "https://www.kinopoisk.ru/film/474/"},
    {"id": 8, "title": "Маска", "poster": "https://kinogo.my/uploads/posts/2023-11/1699995824-1618804087-maska.jpg", "rating": 8.0, "kp_url": "https://www.kinopoisk.ru/film/2324/"},
    {"id": 9, "title": "Сияние", "poster": "https://kinogo.my/uploads/posts/2024-01/1704798751-1904935975-siyanie.jpg", "rating": 8.4, "kp_url": "https://www.kinopoisk.ru/film/356/"},
    {"id": 10, "title": "Гарри Поттер", "poster": "https://kinogo.my/uploads/posts/2019-07/1563015062-1572996915-garri-potter-i-filosofskiy-kamen.jpg", "rating": 8.2, "kp_url": "https://www.kinopoisk.ru/film/689/"},
    {"id": 11, "title": "Бойцовский клуб", "poster": "https://kinogo.my/uploads/posts/2017-04/1491114704-1886867375-boycovskiy-klub.jpg", "rating": 8.7, "kp_url": "https://www.kinopoisk.ru/film/361/"},
    {"id": 12, "title": "Криминальное чтиво", "poster": "https://kinogo.my/uploads/posts/2017-04/1491114844-1736636780-kriminalnoe-chtivo.jpg", "rating": 8.6, "kp_url": "https://www.kinopoisk.ru/film/342/"},
    {"id": 13, "title": "Леон", "poster": "https://kinogo.my/uploads/posts/2017-04/1493391484-904874384-leon.jpg", "rating": 8.7, "kp_url": "https://www.kinopoisk.ru/film/389/"},
    {"id": 14, "title": "Зеленая миля", "poster": "https://kinogo.my/uploads/posts/2017-04/1491114878-1440786967-zelenaya-milya.jpg", "rating": 9.1, "kp_url": "https://www.kinopoisk.ru/film/435/"},
    {"id": 15, "title": "Форрест Гамп", "poster": "https://kinogo.my/uploads/posts/2017-04/1491114949-1981507786-forrest-gamp.jpg", "rating": 8.9, "kp_url": "https://www.kinopoisk.ru/film/448/"}
]

# Общий шаблон с рекламой
def get_html(content):
    return f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <title>Films_Iliaz Pro</title>
        <script src="https://quge5.com/88/tag.min.js" data-zone="261051" async></script>
        <style>
            body {{ background: #0f0f12; color: white; font-family: sans-serif; margin: 0; }}
            nav {{ background: #1a1a24; padding: 15px; display: flex; gap: 20px; }}
            nav a {{ color: white; text-decoration: none; font-weight: bold; }}
            .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 20px; padding: 20px; }}
            .card {{ background: #1a1a24; padding: 10px; border-radius: 10px; text-decoration: none; color: white; display: block; text-align: center; transition: 0.3s; }}
            .card:hover {{ background: #2a2a35; }}
            .card img {{ width: 100%; border-radius: 8px; }}
            .movie-page {{ text-align: center; padding: 40px 20px; }}
            .btn {{ display: inline-block; background: #ff4a5a; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold; margin-top: 20px; font-size: 16px; }}
        </style>
    </head>
    <body>
        <nav>
            <a href="/">Главная</a>
            <a href="/top10">Топ-10</a>
        </nav>
        {content}
    </body>
    </html>
    """

@app.route('/')
def index():
    grid = "".join([f'<a href="/movie/{m["id"]}" class="card"><img src="{m["poster"]}"><h3>{m["title"]}</h3></a>' for m in MOVIES])
    return render_template_string(get_html(f'<div class="grid">{grid}</div>'))

@app.route('/movie/<int:mid>')
def movie_page(mid):
    m = next((item for item in MOVIES if item["id"] == mid), None)
    if not m: return "Фильм не найден", 404
    return render_template_string(get_html(f'''
        <div class="movie-page">
            <h1>{m["title"]}</h1>
            <img src="{m["poster"]}" width="300" style="border-radius: 10px;">
            <p>Рейтинг: {m["rating"]}</p>
            <a href="{m["kp_url"]}" target="_blank" class="btn">Смотреть фильм на Кинопоиске</a>
        </div>
    '''))

@app.route('/top10')
def top10():
    top = sorted(MOVIES, key=lambda x: x['rating'], reverse=True)[:10]
    grid = "".join([f'<a href="/movie/{m["id"]}" class="card"><h3>{m["title"]}</h3><p>Рейтинг: {m["rating"]}</p></a>' for m in top])
    return render_template_string(get_html(f'<h1 style="padding-left:20px;">Лучшие фильмы</h1><div class="grid">{grid}</div>'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
