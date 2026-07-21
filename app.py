from flask import Flask, render_template_string, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'super_secret_key'

# Твои 20 фильмов с реальными ссылками на Кинопоиск и рейтингами
MY_MOVIES = [
    {"id": 1, "title": "Аватар", "rating": 7.9, "kp_url": "https://www.kinopoisk.ru/film/251733/", "poster": "https://kinogo.my/uploads/posts/2017-04/1493391756-1159271017-avatar.jpg"},
    {"id": 2, "title": "Властелин колец", "rating": 8.6, "kp_url": "https://www.kinopoisk.ru/film/328/", "poster": "https://kinogo.my/uploads/posts/2019-07/1563720942-490328414-vlastelin-kolec-bratstvo-kolca.jpg"},
    {"id": 3, "title": "Интерстеллар", "rating": 8.6, "kp_url": "https://www.kinopoisk.ru/film/258687/", "poster": "https://kinogo.my/uploads/posts/2017-04/1491114790-991695033-interstellar.jpg"},
    {"id": 4, "title": "Начало", "rating": 8.7, "kp_url": "https://www.kinopoisk.ru/film/447301/", "poster": "https://kinogo.my/uploads/posts/2017-04/1491114986-2049908774-nachalo.jpg"},
    {"id": 5, "title": "Темный рыцарь", "rating": 8.5, "kp_url": "https://www.kinopoisk.ru/film/111543/", "poster": "https://kinogo.my/uploads/posts/2020-04/1585997266-939135485-temnyy-rycar.jpg"},
    {"id": 6, "title": "Матрица", "rating": 8.5, "kp_url": "https://www.kinopoisk.ru/film/301/", "poster": "https://kinogo.my/uploads/posts/2020-01/1578316075-753251593-matrica.jpg"},
    {"id": 7, "title": "Гладиатор", "rating": 8.6, "kp_url": "https://www.kinopoisk.ru/film/474/", "poster": "https://kinogo.my/uploads/posts/2017-04/1493391510-611397561-gladiator.jpg"},
    {"id": 8, "title": "Маска", "rating": 8.0, "kp_url": "https://www.kinopoisk.ru/film/2324/", "poster": "https://kinogo.my/uploads/posts/2023-11/1699995824-1618804087-maska.jpg"},
    {"id": 9, "title": "Сияние", "rating": 8.4, "kp_url": "https://www.kinopoisk.ru/film/356/", "poster": "https://kinogo.my/uploads/posts/2024-01/1704798751-1904935975-siyanie.jpg"},
    {"id": 10, "title": "Гарри Поттер", "rating": 8.2, "kp_url": "https://www.kinopoisk.ru/film/689/", "poster": "https://kinogo.my/uploads/posts/2019-07/1563015062-1572996915-garri-potter-i-filosofskiy-kamen.jpg"},
    {"id": 11, "title": "Бойцовский клуб", "rating": 8.7, "kp_url": "https://www.kinopoisk.ru/film/361/", "poster": "https://kinogo.my/uploads/posts/2017-04/1491114704-1886867375-boycovskiy-klub.jpg"},
    {"id": 12, "title": "Криминальное чтиво", "rating": 8.6, "kp_url": "https://www.kinopoisk.ru/film/342/", "poster": "https://kinogo.my/uploads/posts/2023-11/1700692804-555184796-kriminalnoe-chtivo.jpg"},
    {"id": 13, "title": "Леон", "rating": 8.7, "kp_url": "https://www.kinopoisk.ru/film/389/", "poster": "https://kinogo.my/uploads/posts/2019-07/1564070804-298906622-leon.jpg"},
    {"id": 14, "title": "Зеленая миля", "rating": 9.1, "kp_url": "https://www.kinopoisk.ru/film/435/", "poster": "https://kinogo.my/uploads/posts/2017-10/1509302130-598249484-zelenaya-milya.jpg"},
    {"id": 15, "title": "Форрест Гамп", "rating": 8.9, "kp_url": "https://www.kinopoisk.ru/film/448/", "poster": "https://kinogo.my/uploads/posts/2020-02/1581515741-1303433223-forrest-gamp.jpg"},
    {"id": 16, "title": "Титаник", "rating": 8.3, "kp_url": "https://www.kinopoisk.ru/film/2213/", "poster": "https://kinogo.my/uploads/posts/2017-04/1493541637-176580560-titanik.jpg"},
    {"id": 17, "title": "Побег из Шоушенка", "rating": 9.1, "kp_url": "https://www.kinopoisk.ru/film/326/", "poster": "https://kinogo.my/uploads/posts/2017-04/1493224416-1754132569-pobeg-iz-shoushenka.jpg"},
    {"id": 18, "title": "Терминатор 2", "rating": 8.7, "kp_url": "https://www.kinopoisk.ru/film/447/", "poster": "https://kinogo.my/uploads/posts/2020-03/1584109913-1352932125-terminator-2-sudnyy-den.jpg"},
    {"id": 19, "title": "Крестный отец", "rating": 8.7, "kp_url": "https://www.kinopoisk.ru/film/325/", "poster": "https://kinogo.my/uploads/posts/2019-11/1572705738-814634704-krestnyy-otec.jpg"},
    {"id": 20, "title": "Назад в будущее", "rating": 8.6, "kp_url": "https://www.kinopoisk.ru/film/494/", "poster": "https://kinogo.my/uploads/posts/2020-06/1591629086-1280450088-nazad-v-buduschee.jpg"}
]

MOVIES = MY_MOVIES + [{"id": i, "title": f"Фильм #{i}", "rating": 7.0, "kp_url": "https://www.kinopoisk.ru", "poster": "https://via.placeholder.com/200x300"} for i in range(21, 101)]
for m in MOVIES: 
    if 'reviews' not in m: m['reviews'] = []

def get_html(content):
    count = len(session.get('favorites', []))
    return f"""
    <!DOCTYPE html><html><head><title>Films_Iliaz</title>
    <script src="https://quge5.com/88/tag.min.js" data-zone="261051" async></script>
    <style>
        body{{background:#0f0f12; color:white; font-family:sans-serif; margin:0;}} 
        nav{{background:#1a1a24; padding:15px; display:flex; gap:15px; flex-wrap:wrap; align-items:center;}}
        nav a{{color:white; text-decoration:none; font-weight:bold;}}
        .grid{{display:grid; grid-template-columns:repeat(auto-fill, minmax(150px, 1fr)); gap:15px; padding:20px;}}
        .card{{background:#1a1a24; padding:10px; border-radius:10px; color:white; text-decoration:none; text-align:center;}}
        .btn{{display:inline-block; background:#ff4a5a; padding:10px; color:white; text-decoration:none; border-radius:5px; margin:5px;}}
        .search-box{{margin-left:auto; display:flex; gap:5px;}}
        .search-box input{{padding:6px; border-radius:5px; border:none;}}
        .search-box button{{padding:6px 12px; background:#ff4a5a; color:white; border:none; border-radius:5px; cursor:pointer;}}
    </style></head>
    <body>
        <nav>
            <a href="/">Главная</a> 
            <a href="/top10">Топ-10</a> 
            <a href="/top5">Топ-5</a> 
            <a href="/top1">Топ-1</a> 
            <a href="/random" style="background:#ff4a5a; padding:6px 12px; border-radius:5px;">🎲 Случайный фильм</a>
            <a href="/favorites">Избранное ({count})</a>
            <form action="/search" method="GET" class="search-box">
                <input type="text" name="q" placeholder="Поиск фильма..." required>
                <button type="submit">Найти</button>
            </form>
        </nav>
        {content}
    </body></html>"""

@app.route('/')
def index():
    grid = "".join([f'<a href="/movie/{m["id"]}" class="card"><img src="{m["poster"]}" width="100%"><h3>{m["title"]}</h3></a>' for m in MOVIES])
    return render_template_string(get_html(f'<div class="grid">{grid}</div>'))

@app.route('/movie/<int:mid>', methods=['GET','POST'])
def movie_page(mid):
    m = next((item for item in MOVIES if item["id"] == mid), None)
    if request.method == 'POST': m['reviews'].append(request.form['text'])
    reviews = "".join([f'<p style="background:#222; padding:5px; border-radius:5px;">{r}</p>' for r in m['reviews']])
    return render_template_string(get_html(f'''
        <div style="padding:20px;">
            <h1>{m["title"]}</h1>
            <img src="{m["poster"]}" width="300" style="border-radius:10px;">
            <p>Рейтинг: {m.get("rating", "N/A")}</p>
            <br><a href="{m["kp_url"]}" target="_blank" class="btn">Смотреть на Кинопоиске</a>
            <a href="/add_fav/{mid}" class="btn">В Избранное</a>
            <h3>Отзывы:</h3>
            <form method="POST"><input name="text" required style="padding:5px;"><button style="padding:5px;">Добавить</button></form>
            {reviews}
        </div>'''))

@app.route('/add_fav/<int:mid>')
def add_fav(mid):
    if 'favorites' not in session: session['favorites'] = []
    if mid not in session['favorites']: session['favorites'].append(mid)
    return redirect(url_for('index'))

@app.route('/favorites')
def favorites():
    favs = [m for m in MOVIES if m['id'] in session.get('favorites', [])]
    grid = "".join([f'<a href="/movie/{m["id"]}" class="card"><img src="{m["poster"]}" width="100%"><h3>{m["title"]}</h3></a>' for m in favs])
    return render_template_string(get_html(f'<h1>Избранное:</h1><div class="grid">{grid}</div>'))

@app.route('/top10')
def top10():
    top_list = sorted(MOVIES, key=lambda x: x.get('rating', 0), reverse=True)[:10]
    grid = "".join([f'<a href="/movie/{m["id"]}" class="card"><img src="{m["poster"]}" width="100%"><h3>{m["title"]} ({m.get("rating")})</h3></a>' for m in top_list])
    return render_template_string(get_html(f'<h1>Топ-10 фильмов</h1><div class="grid">{grid}</div>'))

@app.route('/top5')
def top5():
    top_list = sorted(MOVIES, key=lambda x: x.get('rating', 0), reverse=True)[:5]
    grid = "".join([f'<a href="/movie/{m["id"]}" class="card"><img src="{m["poster"]}" width="100%"><h3>{m["title"]} ({m.get("rating")})</h3></a>' for m in top_list])
    return render_template_string(get_html(f'<h1>Топ-5 фильмов</h1><div class="grid">{grid}</div>'))

@app.route('/top1')
def top1():
    top_list = sorted(MOVIES, key=lambda x: x.get('rating', 0), reverse=True)[:1]
    grid = "".join([f'<a href="/movie/{m["id"]}" class="card"><img src="{m["poster"]}" width="100%"><h3>{m["title"]} ({m.get("rating")})</h3></a>' for m in top_list])
    return render_template_string(get_html(f'<h1>Топ-1 фильм</h1><div class="grid">{grid}</div>'))

@app.route('/random')
def random_movie():
    random_m = random.choice(MOVIES)
    return redirect(url_for('movie_page', mid=random_m['id']))

# Новая фича: Поиск по фильмам
@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    found_movies = [m for m in MOVIES if query in m['title'].lower()]
    grid = "".join([f'<a href="/movie/{m["id"]}" class="card"><img src="{m["poster"]}" width="100%"><h3>{m["title"]}</h3></a>' for m in found_movies]) if found_movies else "<p style='padding:20px;'>Ничего не найдено по вашему запросу.</p>"
    return render_template_string(get_html(f'<h1>Результаты поиска: "{query}"</h1><div class="grid">{grid}</div>'))

if __name__ == '__main__': app.run(debug=True)
