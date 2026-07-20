from flask import Flask, render_template_string, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'super_secret_key'

# Твои 20 фильмов с данными
MY_MOVIES = [
    {"id": 1, "title": "Аватар", "year": 2009, "author": "Джеймс Кэмерон", "desc": "История о планете Пандора.", "poster": "https://kinogo.my/uploads/posts/2017-04/1493391756-1159271017-avatar.jpg", "kp_url": "https://www.kinopoisk.ru/film/251733/"},
    {"id": 2, "title": "Властелин колец", "year": 2001, "author": "Питер Джексон", "desc": "Путешествие Фродо.", "poster": "https://kinogo.my/uploads/posts/2019-07/1563720942-490328414-vlastelin-kolec-bratstvo-kolca.jpg", "kp_url": "https://www.kinopoisk.ru/film/328/"},
    {"id": 3, "title": "Интерстеллар", "year": 2014, "author": "Кристофер Нолан", "desc": "Поиск дома в космосе.", "poster": "https://kinogo.my/uploads/posts/2017-04/1491114790-991695033-interstellar.jpg", "kp_url": "https://www.kinopoisk.ru/film/258687/"},
    {"id": 4, "title": "Начало", "year": 2010, "author": "Кристофер Нолан", "desc": "Кража через сны.", "poster": "https://kinogo.my/uploads/posts/2017-04/1491114986-2049908774-nachalo.jpg", "kp_url": "https://www.kinopoisk.ru/film/447301/"},
    {"id": 5, "title": "Темный рыцарь", "year": 2008, "author": "Кристофер Нолан", "desc": "Бэтмен против Джокера.", "poster": "https://kinogo.my/uploads/posts/2020-04/1585997266-939135485-temnyy-rycar.jpg", "kp_url": "https://www.kinopoisk.ru/film/111543/"},
    {"id": 6, "title": "Матрица", "year": 1999, "author": "Вачовски", "desc": "Мир как симуляция.", "poster": "https://kinogo.my/uploads/posts/2020-01/1578316075-753251593-matrica.jpg", "kp_url": "https://www.kinopoisk.ru/film/301/"},
    {"id": 7, "title": "Гладиатор", "year": 2000, "author": "Ридли Скотт", "desc": "История генерала.", "poster": "https://kinogo.my/uploads/posts/2017-04/1493391510-611397561-gladiator.jpg", "kp_url": "https://www.kinopoisk.ru/film/474/"},
    {"id": 8, "title": "Маска", "year": 1994, "author": "Чак Рассел", "desc": "Волшебная маска.", "poster": "https://kinogo.my/uploads/posts/2023-11/1699995824-1618804087-maska.jpg", "kp_url": "https://www.kinopoisk.ru/film/2324/"},
    {"id": 9, "title": "Сияние", "year": 1980, "author": "Стэнли Кубрик", "desc": "Ужасы в отеле.", "poster": "https://kinogo.my/uploads/posts/2024-01/1704798751-1904935975-siyanie.jpg", "kp_url": "https://www.kinopoisk.ru/film/356/"},
    {"id": 10, "title": "Гарри Поттер", "year": 2001, "author": "Крис Коламбус", "desc": "Мальчик волшебник.", "poster": "https://kinogo.my/uploads/posts/2019-07/1563015062-1572996915-garri-potter-i-filosofskiy-kamen.jpg", "kp_url": "https://www.kinopoisk.ru/film/689/"},
    {"id": 11, "title": "Бойцовский клуб", "year": 1999, "author": "Дэвид Финчер", "desc": "Тайный клуб.", "poster": "https://kinogo.my/uploads/posts/2017-04/1491114704-1886867375-boycovskiy-klub.jpg", "kp_url": "https://www.kinopoisk.ru/film/361/"},
    {"id": 12, "title": "Криминальное чтиво", "year": 1994, "author": "Квентин Тарантино", "desc": "Криминал.", "poster": "https://kinogo.my/uploads/posts/2023-11/1700692804-555184796-kriminalnoe-chtivo.jpg", "kp_url": "https://www.kinopoisk.ru/film/342/"},
    {"id": 13, "title": "Леон", "year": 1994, "author": "Люк Бессон", "desc": "История убийцы.", "poster": "https://kinogo.my/uploads/posts/2019-07/1564070804-298906622-leon.jpg", "kp_url": "https://www.kinopoisk.ru/film/389/"},
    {"id": 14, "title": "Зеленая миля", "year": 1999, "author": "Фрэнк Дарабонт", "desc": "Мистика.", "poster": "https://kinogo.my/uploads/posts/2017-10/1509302130-598249484-zelenaya-milya.jpg", "kp_url": "https://www.kinopoisk.ru/film/435/"},
    {"id": 15, "title": "Форрест Гамп", "year": 1994, "author": "Роберт Земекис", "desc": "Жизнь парня.", "poster": "https://kinogo.my/uploads/posts/2020-02/1581515741-1303433223-forrest-gamp.jpg", "kp_url": "https://www.kinopoisk.ru/film/448/"},
    {"id": 16, "title": "Титаник", "year": 1997, "author": "Джеймс Кэмерон", "desc": "Любовь на лайнере.", "poster": "https://kinogo.my/uploads/posts/2017-04/1493541637-176580560-titanik.jpg", "kp_url": "https://www.kinopoisk.ru/film/2213/"},
    {"id": 17, "title": "Побег из Шоушенка", "year": 1994, "author": "Фрэнк Дарабонт", "desc": "Побег из тюрьмы.", "poster": "https://kinogo.my/uploads/posts/2017-04/1493224416-1754132569-pobeg-iz-shoushenka.jpg", "kp_url": "https://www.kinopoisk.ru/film/326/"},
    {"id": 18, "title": "Терминатор 2", "year": 1991, "author": "Джеймс Кэмерон", "desc": "Восстание машин.", "poster": "https://kinogo.my/uploads/posts/2020-03/1584109913-1352932125-terminator-2-sudnyy-den.jpg", "kp_url": "https://www.kinopoisk.ru/film/447/"},
    {"id": 19, "title": "Крестный отец", "year": 1972, "author": "Ф. Коппола", "desc": "Мафия.", "poster": "https://kinogo.my/uploads/posts/2019-11/1572705738-814634704-krestnyy-otec.jpg", "kp_url": "https://www.kinopoisk.ru/film/325/"},
    {"id": 20, "title": "Назад в будущее", "year": 1985, "author": "Роберт Земекис", "desc": "Путешествия.", "poster": "https://kinogo.my/uploads/posts/2020-06/1591629086-1280450088-nazad-v-buduschee.jpg", "kp_url": "https://www.kinopoisk.ru/film/494/"}
]

# Создаем список из 100 фильмов
MOVIES = MY_MOVIES + [{"id": i, "title": f"Кинофильм #{i}", "year": 2024, "author": "Режиссер", "desc": "Описание.", "poster": "https://via.placeholder.com/200x300", "kp_url": "https://www.kinopoisk.ru", "reviews": []} for i in range(21, 101)]
for m in MOVIES: 
    if 'reviews' not in m: m['reviews'] = []

def get_html(content):
    count = len(session.get('favorites', []))
    return f"""
    <!DOCTYPE html><html><head><title>Films_Iliaz</title>
    <script src="https://quge5.com/88/tag.min.js" data-zone="261051" async></script>
    <style>body{{background:#0f0f12; color:white; font-family:sans-serif;}} 
    .grid{{display:grid; grid-template-columns:repeat(auto-fill, minmax(150px, 1fr)); gap:15px; padding:20px;}}
    .card{{background:#1a1a24; padding:10px; border-radius:10px; color:white; text-decoration:none;}}
    </style></head><body><nav><a href="/">Главная</a> | <a href="/favorites">Избранное ({count})</a></nav>{content}</body></html>"""

@app.route('/')
def index():
    grid = "".join([f'<a href="/movie/{m["id"]}" class="card"><img src="{m["poster"]}" width="100%"><h3>{m["title"]}</h3></a>' for m in MOVIES])
    return render_template_string(get_html(f'<div class="grid">{grid}</div>'))

@app.route('/movie/<int:mid>', methods=['GET','POST'])
def movie_page(mid):
    m = next((item for item in MOVIES if item["id"] == mid), None)
    if request.method == 'POST': m['reviews'].append(request.form['text'])
    reviews = "".join([f'<p>{r}</p>' for r in m['reviews']])
    return render_template_string(get_html(f'<h1>{m["title"]}</h1><img src="{m["poster"]}" width="300"><form method="POST"><input name="text"><button>Отзыв</button></form><a href="/add_fav/{mid}">В Избранное</a>{reviews}'))

@app.route('/add_fav/<int:mid>')
def add_fav(mid):
    if 'favorites' not in session: session['favorites'] = []
    if mid not in session['favorites']: session['favorites'].append(mid)
    return redirect(url_for('index'))

@app.route('/favorites')
def favorites():
    favs = [m for m in MOVIES if m['id'] in session.get('favorites', [])]
    grid = "".join([f'<a href="/movie/{m["id"]}" class="card"><h3>{m["title"]}</h3></a>' for m in favs])
    return render_template_string(get_html(f'<h1>Избранное:</h1><div class="grid">{grid}</div>'))

if __name__ == '__main__': app.run(debug=True)
