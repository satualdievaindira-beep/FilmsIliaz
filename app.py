from flask import Flask, render_template_string, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'super_secret_key'

# Твои 20 фильмов с описаниями, реальными ссылками на Кинопоиск и рейтингами
MY_MOVIES = [
    {
        "id": 1, "title": "Аватар", "year": 2009, "rating": 7.9, 
        "kp_url": "https://www.kinopoisk.ru/film/251733/", 
        "poster": "https://kinogo.my/uploads/posts/2017-04/1493391756-1159271017-avatar.jpg",
        "desc": "Бывший морпех Джейк Салли прикован к инвалидному креслу. Получив задание, он отправляется на базу корпорации на Пандоре, где люди добывают редкий минерал. Джейк вынужден вселиться в аватара — тело, созданное путем генной инженерии с использованием ДНК местных жителей на'ви."
    },
    {
        "id": 2, "title": "Властелин колец", "year": 2001, "rating": 8.6, 
        "kp_url": "https://www.kinopoisk.ru/film/328/", 
        "poster": "https://kinogo.my/uploads/posts/2019-07/1563720942-490328414-vlastelin-kolec-bratstvo-kolca.jpg",
        "desc": "Сказания о Средиземье — это хроника Войны Кольца, войны, длившейся не одну тысячу лет. То, что началось как безобидное кольцо, обернулось битвой за судьбу мира. Хоббит Фродо Бэггинс получает жребий уничтожить Кольцо Всевластия."
    },
    {
        "id": 3, "title": "Интерстеллар", "year": 2014, "rating": 8.6, 
        "kp_url": "https://www.kinopoisk.ru/film/258687/", 
        "poster": "https://kinogo.my/uploads/posts/2017-04/1491114790-991695033-interstellar.jpg",
        "desc": "Когда засуха, пыльные бури и вымирание растений приводят человечество к продовольственному кризису, коллектив ученых и исследователей отправляется сквозь червоточину в путешествие, чтобы превзойти прежние ограничения для космических путешествий человека."
    },
    {
        "id": 4, "title": "Начало", "year": 2010, "rating": 8.7, 
        "kp_url": "https://www.kinopoisk.ru/film/447301/", 
        "poster": "https://kinogo.my/uploads/posts/2017-04/1491114986-2049908774-nachalo.jpg",
        "desc": "Кобб — талантливый вор, лучший в опасном искусстве извлечения: он крадет ценные секреты из глубин подсознания во время сна, когда человеческий разум наиболее уязвим. Редкие способности Кобба сделали его ценным игроком в мире промышленного шпионажа."
    },
    {
        "id": 5, "title": "Темный рыцарь", "year": 2008, "rating": 8.5, 
        "kp_url": "https://www.kinopoisk.ru/film/111543/", 
        "poster": "https://kinogo.my/uploads/posts/2020-04/1585997266-939135485-temnyy-rycar.jpg",
        "desc": "Бэтмен поднимает ставки в войне с криминалом. С помощью лейтенанта Джима Гордона и прокурора Харви Дента он намеревается очистить улицы Готэма от преступности раз и навсегда. Но ситуация выходит из-под контроля, когда в городе появляется криминальный гений по имени Джокер."
    },
    {
        "id": 6, "title": "Матрица", "year": 1999, "rating": 8.5, 
        "kp_url": "https://www.kinopoisk.ru/film/301/", 
        "poster": "https://kinogo.my/uploads/posts/2020-01/1578316075-753251593-matrica.jpg",
        "desc": "Жизнь Томаса Андерсона разделена на две части: днем он самый обычный программист, а ночью становится хакером по имени Нео. Однажды его жизнь круто меняется, когда он узнает страшную правду о том, что весь мир вокруг — это иллюзия, созданная машинами."
    },
    {
        "id": 7, "title": "Гладиатор", "year": 2000, "rating": 8.6, 
        "kp_url": "https://www.kinopoisk.ru/film/474/", 
        "poster": "https://kinogo.my/uploads/posts/2017-04/1493391510-611397561-gladiator.jpg",
        "desc": "В Римской империи нет равного полководца генералу Максиму. Непобедимые легионы, ведомые им, боготворили своего предводителя. Но император Марк Аврелий решает передать власть Максиму, что вызывает зависть и ненависть у его родного сына Коммода."
    },
    {
        "id": 8, "title": "Маска", "year": 1994, "rating": 8.0, 
        "kp_url": "https://www.kinopoisk.ru/film/2324/", 
        "poster": "https://kinogo.my/uploads/posts/2023-11/1699995824-1618804087-maska.jpg",
        "desc": "Застенчивый, робкий и вечно попадающий в нелепые ситуации служащий банка Стэнли Ипкисс находит древний таинственный артефакт — деревянную маску. Надев ее, Стэнли превращается в неуязвимого мультяшного супергероя, способного творить любые безумства."
    },
    {
        "id": 9, "title": "Сияние", "year": 1980, "rating": 8.4, 
        "kp_url": "https://www.kinopoisk.ru/film/356/", 
        "poster": "https://kinogo.my/uploads/posts/2024-01/1704798751-1904935975-siyanie.jpg",
        "desc": "Джек Торренс приехал в роскошный уединенный отель на зиму вместе с женой и сыном, чтобы работать смотрителем. Торренс здесь раньше никогда не был. Или это не так? Ответ где-то в зловещей атмосфере этого места."
    },
    {
        "id": 10, "title": "Гарри Поттер", "year": 2001, "rating": 8.2, 
        "kp_url": "https://www.kinopoisk.ru/film/689/", 
        "poster": "https://kinogo.my/uploads/posts/2019-07/1563015062-1572996915-garri-potter-i-filosofskiy-kamen.jpg",
        "desc": "Осиротевший мальчик Гарри Поттер живет в доме своих тети и дяди и даже не подозревает, что он — настоящий волшебник. В день своего одиннадцатилетия он получает письмо с приглашением в Хогвартс — школу чародейства и волшебства."
    },
    {
        "id": 11, "title": "Бойцовский клуб", "year": 1999, "rating": 8.7, 
        "kp_url": "https://www.kinopoisk.ru/film/361/", 
        "poster": "https://kinogo.my/uploads/posts/2017-04/1491114704-1886867375-boycovskiy-klub.jpg",
        "desc": "Сотрудник страховой компании страдает хронической бессонницей и отчаянно пытается вырваться из мучительной скуки своей жизни. Вскоре он встречает Тайлера Дердена — харизматичного торговца мылом с извращенной философией."
    },
    {
        "id": 12, "title": "Криминальное чтиво", "year": 1994, "rating": 8.6, 
        "kp_url": "https://www.kinopoisk.ru/film/342/", 
        "poster": "https://kinogo.my/uploads/posts/2023-11/1700692804-555184796-kriminalnoe-chtivo.jpg",
        "desc": "Двое бандитов Винсент Вега и Джулс Винфилд ведут философские беседы между разборками и решениями проблем с должниками криминального босса Марселласа Уоллеса. В центре сюжета переплетаются несколько историй о преступности Лос-Анджелеса."
    },
    {
        "id": 13, "title": "Леон", "year": 1994, "rating": 8.7, 
        "kp_url": "https://www.kinopoisk.ru/film/389/", 
        "poster": "https://kinogo.my/uploads/posts/2019-07/1564070804-298906622-leon.jpg",
        "desc": "В Нью-Йорке профессиональный киллер Леон знакомится со своей соседкой, девочкой Матильдой. Когда ее семью расстреливают коррумпированные агенты ФБР во главе с Норсфилдом, Леон берет девочку под свою защиту и обучает ремеслу наемника."
    },
    {
        "id": 14, "title": "Зеленая миля", "year": 1999, "rating": 9.1, 
        "kp_url": "https://www.kinopoisk.ru/film/435/", 
        "poster": "https://kinogo.my/uploads/posts/2017-10/1509302130-598249484-zelenaya-milya.jpg",
        "desc": "Джон Коффи, гигантский человек, обвиненный в страшном преступлении, попадает в блок смертников тюрьмы «Холодная гора». Обладая невероятным даром исцеления, этот кроткий человек меняет жизни всех надзирателей и заключенных вокруг."
    },
    {
        "id": 15, "title": "Форрест Гамп", "year": 1994, "rating": 8.9, 
        "kp_url": "https://www.kinopoisk.ru/film/448/", 
        "poster": "https://kinogo.my/uploads/posts/2020-02/1581515741-1303433223-forrest-gamp.jpg",
        "desc": "Сидя на скамейке в ожидании автобуса, добродушный и простодушный Форрест Гамп рассказывает случайным попутчикам историю своей необыкновенной жизни. Благодаря чистоте сердца он невольно становится участником ключевых событий истории США."
    },
    {
        "id": 16, "title": "Титаник", "year": 1997, "rating": 8.3, 
        "kp_url": "https://www.kinopoisk.ru/film/2213/", 
        "poster": "https://kinogo.my/uploads/posts/2017-04/1493541637-176580560-titanik.jpg",
        "desc": "Молодые влюбленные Джек и Роза находят друг друга в первом и последнем плавании «непотопляемого» лайнера. Они из разных социальных слоев, но их любовь сильнее любых преград перед лицом катастрофы века."
    },
    {
        "id": 17, "title": "Побег из Шоушенка", "year": 1994, "rating": 9.1, 
        "kp_url": "https://www.kinopoisk.ru/film/326/", 
        "poster": "https://kinogo.my/uploads/posts/2017-04/1493224416-1754132569-pobeg-iz-shoushenka.jpg",
        "desc": "Успешный банкир Энди Дюфрейн обвинен в убийстве жены и ее любовника. Оказавшись в суровой тюрьме Шоушенк, он не теряет надежды и интеллекта, завоевывая авторитет среди заключенных и начальника тюрьмы."
    },
    {
        "id": 18, "title": "Терминатор 2", "year": 1991, "rating": 8.7, 
        "kp_url": "https://www.kinopoisk.ru/film/447/", 
        "poster": "https://kinogo.my/uploads/posts/2020-03/1584109913-1352932125-terminator-2-sudnyy-den.jpg",
        "desc": "Прошло более десяти лет с тех пор, как киборг-убийца пытался уничтожить Сара Конор. Теперь ее подросший сын Джон становится целью нового, усовершенствованного и жидкого робота из будущего. Но на защиту встает перепрограммированный старый терминатор."
    },
    {
        "id": 19, "title": "Крестный отец", "year": 1972, "rating": 8.7, 
        "kp_url": "https://www.kinopoisk.ru/film/325/", 
        "poster": "https://kinogo.my/uploads/posts/2019-11/1572705738-814634704-krestnyy-otec.jpg",
        "desc": "Эпическая сага о влиятельной сицилийской мафиозной семье Корлеоне под руководством Дона Вито. История о власти, традициях, семейных узах и предательстве, навсегда изменившая мир кинематографа."
    },
    {
        "id": 20, "title": "Назад в будущее", "year": 1985, "rating": 8.6, 
        "kp_url": "https://www.kinopoisk.ru/film/494/", 
        "poster": "https://kinogo.my/uploads/posts/2020-06/1591629086-1280450088-nazad-v-buduschee.jpg",
        "desc": "Подросток Марти МакФлай с помощью машины времени, созданной его другом-ученым доком Брауном, случайно отправляется из 1985 года в 1955-й. Там он встречает своих молодых родителей и должен сделать так, чтобы они влюбились друг в друга."
    }
]

MOVIES = MY_MOVIES + [{"id": i, "title": f"Фильм #{i}", "year": 2020, "rating": 7.0, "kp_url": "https://www.kinopoisk.ru", "poster": "https://via.placeholder.com/200x300", "desc": "Увлекательный художественный фильм, заслуживающий внимания зрителей своей атмосферой и сюжетом."} for i in range(21, 101)]
for m in MOVIES: 
    if 'reviews' not in m: m['reviews'] = []
    if 'year' not in m: m['year'] = 2020
    if 'desc' not in m: m['desc'] = "Увлекательный художественный фильм, заслуживающий внимания зрителей."

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
        .btn{{display:inline-block; background:#ff4a5a; padding:10px; color:white; text-decoration:none; border-radius:5px; margin:5px 5px 5px 0;}}
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
            <a href="/years">📅 По годам</a>
            <a href="/random" style="background:#ff4a5a; padding:6px 12px; border-radius:5px;">🎲 Случайный фильм</a>
            <a href="/favorites">Избранное ({count})</a>
            <a href="/stats">📊 Статистика</a>
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
    reviews = "".join([f'<p style="background:#1a1a24; padding:10px; border-radius:5px; margin-top:5px;">{r}</p>' for r in m['reviews']])
    return render_template_string(get_html(f'''
        <div style="padding:20px;">
            <h1>{m["title"]} ({m.get("year", "N/A")})</h1>
            <div style="display:flex; gap:30px; flex-wrap:wrap; align-items:flex-start; margin-top:15px;">
                <div>
                    <img src="{m["poster"]}" width="280" style="border-radius:10px; display:block;">
                    <p style="font-size:18px; margin-top:10px;"><b>Рейтинг:</b> {m.get("rating", "N/A")}</p>
                    <div style="margin-top:10px;">
                        <a href="{m["kp_url"]}" target="_blank" class="btn">Смотреть на Кинопоиске</a>
                        <a href="/add_fav/{mid}" class="btn" style="background:#333;">В Избранное</a>
                    </div>
                </div>
                <div style="flex:1; min-width:280px; background:#1a1a24; padding:20px; border-radius:10px;">
                    <h3 style="margin-top:0; color:#ff4a5a;">Описание фильма</h3>
                    <p style="font-size:16px; line-height:1.6; color:#ccc;">{m.get("desc", "")}</p>
                </div>
            </div>
            <div style="margin-top:30px; max-width:800px;">
                <h3>Отзывы:</h3>
                <form method="POST" style="display:flex; gap:10px; margin-bottom:15px;">
                    <input name="text" required placeholder="Написать отзыв..." style="flex:1; padding:10px; border-radius:5px; border:none; background:#222; color:white;">
                    <button style="padding:10px 20px; background:#ff4a5a; color:white; border:none; border-radius:5px; cursor:pointer; font-weight:bold;">Добавить</button>
                </form>
                {reviews if reviews else '<p style="color:#777;">Пока нет отзывов. Будьте первыми!</p>'}
            </div>
        </div>'''))

@app.route('/add_fav/<int:mid>')
def add_fav(mid):
    if 'favorites' not in session: session['favorites'] = []
    if mid not in session['favorites']: session['favorites'].append(mid)
    return redirect(url_for('movie_page', mid=mid))

@app.route('/favorites')
def favorites():
    favs = [m for m in MOVIES if m['id'] in session.get('favorites', [])]
    grid = "".join([f'<a href="/movie/{m["id"]}" class="card"><img src="{m["poster"]}" width="100%"><h3>{m["title"]}</h3></a>' for m in favs]) if favs else "<p style='padding:20px;'>Ваше избранное пока пусто.</p>"
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

@app.route('/years')
def years():
    sorted_movies = sorted(MOVIES, key=lambda x: x.get('year', 2020), reverse=True)
    grid = "".join([f'<a href="/movie/{m["id"]}" class="card"><img src="{m["poster"]}" width="100%"><h3>{m["title"]} ({m.get("year")})</h3></a>' for m in sorted_movies])
    return render_template_string(get_html(f'<h1>Фильмы по годам</h1><div class="grid">{grid}</div>'))

@app.route('/random')
def random_movie():
    random_m = random.choice(MOVIES)
    return redirect(url_for('movie_page', mid=random_m['id']))

@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    found_movies = [m for m in MOVIES if query in m['title'].lower()]
    grid = "".join([f'<a href="/movie/{m["id"]}" class="card"><img src="{m["poster"]}" width="100%"><h3>{m["title"]}</h3></a>' for m in found_movies]) if found_movies else "<p style='padding:20px;'>Ничего не найдено по вашему запросу.</p>"
    return render_template_string(get_html(f'<h1>Результаты поиска: "{query}"</h1><div class="grid">{grid}</div>'))

@app.route('/stats')
def stats():
    total_movies = len(MOVIES)
    fav_count = len(session.get('favorites', []))
    avg_rating = round(sum([m.get('rating', 0) for m in MOVIES]) / total_movies, 2)
    return render_template_string(get_html(f'''
        <div style="padding:20px; max-width:600px;">
            <h1>📊 Статистика сайта Films_Iliaz</h1>
            <ul style="line-height:2; font-size:18px;">
                <li>Всего фильмов в базе: <b>{total_movies}</b></li>
                <li>Фильмов добавлено в твоё избранное: <b>{fav_count}</b></li>
                <li>Средний рейтинг кинотеки: <b>{avg_rating} / 10</b></li>
            </ul>
        </div>
    '''))

if __name__ == '__main__': app.run(debug=True)
