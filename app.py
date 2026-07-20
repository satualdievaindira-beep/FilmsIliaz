import os
from flask import Flask, render_template_string, request

app = Flask(__name__)

MOVIES = [
    {"id": 1, "title": "Аватар", "year": 2009, "author": "Джеймс Кэмерон", "desc": "История о далекой планете Пандора.", "poster": "https://kinogo.my/uploads/posts/2017-04/1493391756-1159271017-avatar.jpg", "rating": 7.9, "kp_url": "https://www.kinopoisk.ru/film/251733/"},
    {"id": 2, "title": "Властелин колец", "year": 2001, "author": "Питер Джексон", "desc": "Путешествие хоббита Фродо к Роковой горе.", "poster": "https://kinogo.my/uploads/posts/2019-07/1563720942-490328414-vlastelin-kolec-bratstvo-kolca.jpg", "rating": 8.6, "kp_url": "https://www.kinopoisk.ru/film/328/"},
    {"id": 3, "title": "Интерстеллар", "year": 2014, "author": "Кристофер Нолан", "desc": "Поиск нового дома для человечества в космосе.", "poster": "https://kinogo.my/uploads/posts/2017-04/1491114790-991695033-interstellar.jpg", "rating": 8.6, "kp_url": "https://www.kinopoisk.ru/film/258687/"},
    {"id": 4, "title": "Начало", "year": 2010, "author": "Кристофер Нолан", "desc": "Кража секретов через сны.", "poster": "https://kinogo.my/uploads/posts/2017-04/1491114986-2049908774-nachalo.jpg", "rating": 8.7, "kp_url": "https://www.kinopoisk.ru/film/447301/"},
    {"id": 5, "title": "Темный рыцарь", "year": 2008, "author": "Кристофер Нолан", "desc": "Бэтмен против Джокера.", "poster": "https://kinogo.my/uploads/posts/2020-04/1585997266-939135485-temnyy-rycar.jpg", "rating": 8.5, "kp_url": "https://www.kinopoisk.ru/film/111543/"},
    {"id": 6, "title": "Матрица", "year": 1999, "author": "Вачовски", "desc": "Мир — это компьютерная симуляция.", "poster": "https://kinogo.my/uploads/posts/2020-01/1578316075-753251593-matrica.jpg", "rating": 8.5, "kp_url": "https://www.kinopoisk.ru/film/301/"},
    {"id": 7, "title": "Гладиатор", "year": 2000, "author": "Ридли Скотт", "desc": "История римского генерала.", "poster": "https://kinogo.my/uploads/posts/2017-04/1493391510-611397561-gladiator.jpg", "rating": 8.6, "kp_url": "https://www.kinopoisk.ru/film/474/"},
    {"id": 8, "title": "Маска", "year": 1994, "author": "Чак Рассел", "desc": "Обычный клерк находит волшебную маску.", "poster": "https://kinogo.my/uploads/posts/2023-11/1699995824-1618804087-maska.jpg", "rating": 8.0, "kp_url": "https://www.kinopoisk.ru/film/2324/"},
    {"id": 9, "title": "Сияние", "year": 1980, "author": "Стэнли Кубрик", "desc": "Ужасы в уединенном отеле.", "poster": "https://kinogo.my/uploads/posts/2024-01/1704798751-1904935975-siyanie.jpg", "rating": 8.4, "kp_url": "https://www.kinopoisk.ru/film/356/"},
    {"id": 10, "title": "Гарри Поттер", "year": 2001, "author": "Крис Коламбус", "desc": "Мальчик узнает, что он волшебник.", "poster": "https://kinogo.my/uploads/posts/2019-07/1563015062-1572996915-garri-potter-i-filosofskiy-kamen.jpg", "rating": 8.2, "kp_url": "https://www.kinopoisk.ru/film/689/"},
    {"id": 11, "title": "Бойцовский клуб", "year": 1999, "author": "Дэвид Финчер", "desc": "Тайная организация бойцов.", "poster": "https://kinogo.my/uploads/posts/2017-04/1491114704-1886867375-boycovskiy-klub.jpg", "rating": 8.7, "kp_url": "https://www.kinopoisk.ru/film/361/"},
    {"id": 12, "title": "Криминальное чтиво", "year": 1994, "author": "Квентин Тарантино", "desc": "Переплетение криминальных историй.", "poster": "https://kinogo.my/uploads/posts/2023-11/1700692804-555184796-kriminalnoe-chtivo.jpg", "rating": 8.6, "kp_url": "https://www.kinopoisk.ru/film/342/"},
    {"id": 13, "title": "Леон", "year": 1994, "author": "Люк Бессон", "desc": "История профессионального убийцы.", "poster": "https://kinogo.my/uploads/posts/2019-07/1564070804-298906622-leon.jpg", "rating": 8.7, "kp_url": "https://www.kinopoisk.ru/film/389/"},
    {"id": 14, "title": "Зеленая миля", "year": 1999, "author": "Фрэнк Дарабонт", "desc": "Мистические события в тюрьме.", "poster": "https://kinogo.my/uploads/posts/2017-10/1509302130-598249484-zelenaya-milya.jpg", "rating": 9.1, "kp_url": "https://www.kinopoisk.ru/film/435/"},
    {"id": 15, "title": "Форрест Гамп", "year": 1994, "author": "Роберт Земекис", "desc": "Невероятная жизнь простого парня.", "poster": "https://kinogo.my/uploads/posts/2020-02/1581515741-1303433223-forrest-gamp.jpg", "rating": 8.9, "kp_url": "https://www.kinopoisk.ru/film/448/"},
    {"id": 16, "title": "Титаник", "year": 1997, "author": "Джеймс Кэмерон", "desc": "Трагическая история любви на лайнере.", "poster": "https://kinogo.my/uploads/posts/2017-04/1493541637-176580560-titanik.jpg", "rating": 8.3, "kp_url": "https://www.kinopoisk.ru/film/2213/"},
    {"id": 17, "title": "Побег из Шоушенка", "year": 1994, "author": "Фрэнк Дарабонт", "desc": "История о надежде и побеге из тюрьмы.", "poster": "https://kinogo.my/uploads/posts/2017-04/1493224416-1754132569-pobeg-iz-shoushenka.jpg", "rating": 9.1, "kp_url": "https://www.kinopoisk.ru/film/326/"},
    {"id": 18, "title": "Терминатор 2", "year": 1991, "author": "Джеймс Кэмерон", "desc": "Борьба за спасение будущего.", "poster": "https://kinogo.my/uploads/posts/2020-03/1584109913-1352932125-terminator-2-sudnyy-den.jpg", "rating": 8.7, "kp_url": "https://www.kinopoisk.ru/film/447/"},
    {"id": 19, "title": "Крестный отец", "year": 1972, "author": "Фрэнсис Форд Коппола", "desc": "Сага о жизни мафиозного клана.", "poster": "https://kinogo.my/uploads/posts/2019-11/1572705738-814634704-krestnyy-otec.jpg", "rating": 8.7, "kp_url": "https://www.kinopoisk.ru/film/325/"},
    {"id": 20, "title": "Назад в будущее", "year": 1985, "author": "Роберт Земекис", "desc": "Путешествия во времени на машине.", "poster": "https://kinogo.my/uploads/posts/2020-06/1591629086-1280450088-nazad-v-buduschee.jpg", "rating": 8.6, "kp_url": "https://www.kinopoisk.ru/film/494/"}
]

# Добавляем остальные фильмы для полноты базы
for i in range(21, 101):
    MOVIES.append({"id": i, "title": f"Фильм {i}", "year": 2025, "author": "Режиссер", "desc": "Скоро добавим описание.", "poster": "https://via.placeholder.com/200x300", "rating": 7.0, "kp_url": "https://www.kinopoisk.ru"})

def get_html(content):
    return f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <title>Films_Iliaz Pro</title>
        <script src="https://quge5.com/88/tag.min.js" data-zone="261051" async></script>
        <style>
            body {{ background: #0f0f12; color: white; font-family: sans-serif; margin: 0; min-height: 100vh; display: flex; flex-direction: column; }}
            nav {{ background: #1a1a24; padding: 15px; display: flex; gap: 20px; }}
            nav a {{ color: white; text-decoration: none; font-weight: bold; }}
            .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 20px; padding: 20px; }}
            .card {{ background: #1a1a24; padding: 10px; border-radius: 10px; text-decoration: none; color: white; text-align: center; }}
            .movie-page {{ text-align: center; padding: 40px; max-width: 600px; margin: auto; }}
            .btn {{ display: inline-block; background: #ff4a5a; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold; margin-top: 20px; }}
            footer {{ margin-top: auto; background: #1a1a24; padding: 20px; text-align: center; color: #888; }}
        </style>
    </head>
    <body>
        <nav><a href="/">Главная</a><a href="/top10">Топ-10</a></nav>
        {content}
        <footer><a href="/about">О нас</a> | <a href="/contacts">Контакты</a> | <a href="/cookies">Cookie</a></footer>
    </body>
    </html>
    """

@app.route('/')
def index():
    grid = "".join([f'<a href="/movie/{m["id"]}" class="card"><img src="{m["poster"]}" width="100%"><h3>{m["title"]}</h3></a>' for m in MOVIES])
    return render_template_string(get_html(f'<div class="grid">{grid}</div>'))

@app.route('/movie/<int:mid>')
def movie_page(mid):
    m = next((item for item in MOVIES if item["id"] == mid), None)
    return render_template_string(get_html(f'''
        <div class="movie-page">
            <h1>{m["title"]} ({m["year"]})</h1>
            <img src="{m["poster"]}" width="300" style="border-radius:10px;">
            <p><strong>Автор:</strong> {m["author"]}</p>
            <p>{m["desc"]}</p>
            <a href="{m["kp_url"]}" target="_blank" class="btn">Смотреть на Кинопоиске</a>
        </div>
    '''))

@app.route('/top10')
def top10():
    top = sorted(MOVIES, key=lambda x: x['rating'], reverse=True)[:10]
    grid = "".join([f'<a href="/movie/{m["id"]}" class="card"><h3>{m["title"]}</h3></a>' for m in top])
    return render_template_string(get_html(f'<div class="grid">{grid}</div>'))

@app.route('/about')
def about(): return render_template_string(get_html("<h1>О нас</h1>"))
@app.route('/contacts')
def contacts(): return render_template_string(get_html("<h1>Контакты</h1>"))
@app.route('/cookies')
def cookies(): return render_template_string(get_html("<h1>Cookie</h1>"))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
