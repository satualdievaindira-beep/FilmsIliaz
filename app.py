import os
import urllib.request
import urllib.error
from flask import Flask, render_template_string, request, redirect, url_for, Response

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'supersecretkey_films_iliaz_2026_secure')
app.config['DEBUG'] = True

# --- БАЗА ДАННЫХ ---
MOVIES = [
    {"id": 1, "title": "Аватар", "genre": "Фантастика", "poster": "https://kinogo.my/uploads/posts/2017-04/1493391756-1159271017-avatar.jpg", "video_url": "https://www.kinopoisk.ru/film/251733/", "year": 2009, "director": "Джеймс Кэмерон", "rating": 7.9, "duration": "162 мин.", "description": "Бывший морской пехотинец Джейк Салли...", "cast": "Сэм Уортингтон, Зои Салдана"},
    {"id": 2, "title": "Властелин колец: Братство Кольца", "genre": "Фантастика", "poster": "https://kinogo.my/uploads/posts/2019-07/1563720942-490328414-vlastelin-kolec-bratstvo-kolca.jpg", "video_url": "https://www.kinopoisk.ru/film/348/", "year": 2001, "director": "Питер Джексон", "rating": 8.6, "duration": "178 мин.", "description": "Молодой хоббит Фродо Бэггинс...", "cast": "Элайджа Вуд, Иэн Маккеллен"},
    {"id": 3, "title": "Гарри Поттер и Философский камень", "genre": "Фантастика", "poster": "https://kinogo.my/uploads/posts/2019-07/1563015062-1572996915-garri-potter-i-filosofskiy-kamen.jpg", "video_url": "https://www.kinopoisk.ru/film/689/", "year": 2001, "director": "Крис Коламбус", "rating": 8.2, "duration": "152 мин.", "description": "Гарри Поттер — обычный сирота...", "cast": "Дэниэл Рэдклифф, Эмма Уотсон"},
    {"id": 4, "title": "Интерстеллар", "genre": "Фантастика", "poster": "https://kinogo.my/uploads/posts/2017-04/1491114790-991695033-interstellar.jpg", "video_url": "https://www.kinopoisk.ru/film/258687/", "year": 2014, "director": "Кристофер Нолан", "rating": 8.6, "duration": "169 мин.", "description": "Группа исследователей использует...", "cast": "Мэттью Макконахи, Энн Хэтэуэй"},
    {"id": 5, "title": "Матрица", "genre": "Фантастика", "poster": "https://kinogo.my/uploads/posts/2020-01/1578316075-753251593-matrica.jpg", "video_url": "https://www.kinopoisk.ru/film/301/", "year": 1999, "director": "Лана Вачовски", "rating": 8.5, "duration": "136 мин.", "description": "Жизнь Томаса Андерсона...", "cast": "Киану Ривз, Лоренс Фишбёрн"},
    {"id": 6, "title": "Начало", "genre": "Фантастика", "poster": "https://kinogo.my/uploads/posts/2017-04/1491114986-2049908774-nachalo.jpg", "video_url": "https://www.kinopoisk.ru/film/447301/", "year": 2010, "director": "Кристофер Нолан", "rating": 8.7, "duration": "148 мин.", "description": "Кобб — мастер кражи секретов...", "cast": "Леонардо Ди Каприо, Том Харди"},
    {"id": 7, "title": "Темный рыцарь", "genre": "Боевики", "poster": "https://kinogo.my/uploads/posts/2020-03/1585250490_the-dark-knight-2008.jpg", "video_url": "https://www.kinopoisk.ru/film/111543/", "year": 2008, "director": "Кристофер Нолан", "rating": 8.5, "duration": "152 мин.", "description": "Бэтмен поднимает ставки...", "cast": "Кристиан Бейл, Хит Леджер"},
    {"id": 8, "title": "Гладиатор", "genre": "Боевики", "poster": "https://kinogo.my/uploads/posts/2019-11/1574343110_gladiator-2000.jpg", "video_url": "https://www.kinopoisk.ru/film/474/", "year": 2000, "director": "Ридли Скотт", "rating": 8.6, "duration": "155 мин.", "description": "Преданный генерал Максимус...", "cast": "Рассел Кроу, Хоакин Феникс"},
    {"id": 9, "title": "Мальчишник в Вегасе", "genre": "Комедии", "poster": "https://kinogo.my/uploads/posts/2017-04/1491158875-2116979171-malchishnik-v-vegase.jpg", "video_url": "https://www.kinopoisk.ru/film/408410/", "year": 2009, "director": "Тодд Филлипс", "rating": 7.9, "duration": "100 мин.", "description": "Трое друзей просыпаются...", "cast": "Брэдли Купер, Зак Галифианакис"},
    {"id": 10, "title": "Маска", "genre": "Комедии", "poster": "https://kinogo.my/uploads/posts/2023-11/1699995824-1618804087-maska.jpg", "video_url": "https://www.kinopoisk.ru/film/6039/", "year": 1994, "director": "Чак Рассел", "rating": 8.0, "duration": "101 мин.", "description": "Скромный работник банка...", "cast": "Джим Керри, Кэмерон Диас"},
    {"id": 11, "title": "Главный герой", "genre": "Комедии", "poster": "https://kinogo.my/uploads/posts/2021-09/1632400100_free-guy-2021.jpg", "video_url": "https://www.kinopoisk.ru/film/1199159/", "year": 2021, "director": "Шон Леви", "rating": 7.2, "duration": "115 мин.", "description": "Банковский клерк узнает...", "cast": "Райан Рейнольдс, Джоди Комер"},
    {"id": 12, "title": "Заклятие", "genre": "Ужасы", "poster": "https://kinogo.my/uploads/posts/2020-03/1583751212-1153530858-zaklyatie.jpg", "video_url": "https://www.kinopoisk.ru/film/462682/", "year": 2013, "director": "Джеймс Ван", "rating": 7.4, "duration": "112 мин.", "description": "Исследователи паранормального...", "cast": "Вера Фармига, Патрик Уилсон"},
    {"id": 13, "title": "Оно", "genre": "Ужасы", "poster": "https://kinogo.my/uploads/posts/2019-10/1570100719-126843975-ono.jpg", "video_url": "https://www.kinopoisk.ru/film/452973/", "year": 2017, "director": "Энди Мускетти", "rating": 7.3, "duration": "135 мин.", "description": "Школьники объединяются...", "cast": "Билл Скарсгард, Финн Вулфхард"},
    {"id": 14, "title": "Сияние", "genre": "Ужасы", "poster": "https://kinogo.my/uploads/posts/2024-01/1704798751-1904935975-siyanie.jpg", "video_url": "https://www.kinopoisk.ru/film/409/", "year": 1980, "director": "Стэнли Кубрик", "rating": 8.4, "duration": "144 мин.", "description": "Писатель Джек Торренс...", "cast": "Джек Николсон, Шелли Дювалл"},
    {"id": 15, "title": "Тихое место", "genre": "Ужасы", "poster": "https://kinogo.my/uploads/posts/2019-10/1570971117-511240173-tihoe-mesto.jpg", "video_url": "https://www.kinopoisk.ru/film/1043743/", "year": 2018, "director": "Джон Красински", "rating": 7.1, "duration": "90 мин.", "description": "Семья выживает в мире...", "cast": "Эмили Блант, Джон Красински"},
    {"id": 16, "title": "Астрал", "genre": "Ужасы", "poster": "https://kinogo.my/uploads/posts/2020-02/1582196735-58106119-astral.jpg", "video_url": "https://www.kinopoisk.ru/film/495892/", "year": 2010, "director": "Джеймс Ван", "rating": 6.8, "duration": "103 мин.", "description": "Мальчик впадает в кому...", "cast": "Патрик Уилсон, Роуз Бирн"}
]

REVIEWS = {movie["id"]: [] for movie in MOVIES}

AD_CODE = """
    <meta name="monetag" content="8a4bbe65dee28e911fefcd608f183f21">
    <script src="https://quge5.com/88/tag.min.js" data-zone="261051" async data-cfasync="false"></script>
"""

MODAL_STYLES = """
    .footer-links { margin-top: 15px; display: flex; justify-content: center; gap: 25px; }
    .footer-links a { color: var(--text-muted); text-decoration: none; font-size: 0.95rem; cursor: pointer; transition: color 0.2s; }
    .footer-links a:hover { color: var(--primary); }
    .modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0, 0, 0, 0.85); display: flex; align-items: center; justify-content: center; z-index: 2000; opacity: 0; pointer-events: none; transition: opacity 0.3s ease; }
    .modal-overlay.active { opacity: 1; pointer-events: auto; }
    .modal-box { background-color: var(--card-bg); width: 90%; max-width: 550px; padding: 35px; border-radius: 16px; border: 1px solid #333344; box-shadow: 0 10px 30px rgba(0,0,0,0.6); position: relative; transform: translateY(-20px); transition: transform 0.3s ease; }
    .modal-overlay.active .modal-box { transform: translateY(0); }
    .modal-close { position: absolute; top: 15px; right: 20px; background: none; border: none; color: var(--text-muted); font-size: 2rem; cursor: pointer; transition: color 0.2s; }
    .modal-close:hover { color: var(--primary); }
    .modal-box h3 { margin-top: 0; color: var(--primary); font-size: 1.6rem; border-bottom: 1px solid #28283a; padding-bottom: 10px; }
    .modal-box p { line-height: 1.6; color: #d1d1d6; font-size: 0.95rem; }
    .admin-contact-item { background: #13131c; padding: 12px 18px; border-radius: 8px; margin-top: 10px; border-left: 3px solid var(--primary); font-weight: 600; }
"""

MODAL_SCRIPT = """
<script>
    function openModal(id) { document.getElementById(id).classList.add('active'); document.body.style.overflow = 'hidden'; }
    function closeModal(id) { document.getElementById(id).classList.remove('active'); document.body.style.overflow = 'auto'; }
    window.onclick = function(event) { if (event.target.classList.contains('modal-overlay')) { event.target.classList.remove('active'); document.body.style.overflow = 'auto'; } }
</script>
"""

INDEX_HTML = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Films_Iliaz — Лучшая База Фильмов</title>
    {AD_CODE}
    <style>
        :root {{ --bg-dark: #0f0f12; --card-bg: #1a1a24; --primary: #ff4a5a; --text-main: #ffffff; --text-muted: #a0a0b0; }}
        body {{ font-family: 'Segoe UI', Roboto, sans-serif; background-color: var(--bg-dark); color: var(--text-main); margin: 0; padding: 0; }}
        header {{ background: linear-gradient(135deg, #161623 0%, #0b0b11 100%); padding: 30px 20px; text-align: center; border-bottom: 4px solid var(--primary); }}
        header h1 {{ margin: 0; font-size: 3rem; color: var(--primary); text-transform: uppercase; letter-spacing: 3px; }}
        header p {{ margin: 10px 0 0 0; color: var(--text-muted); }}
        .container {{ max-width: 1300px; margin: 40px auto; padding: 0 25px; }}
        .genre-section {{ margin-bottom: 60px; }}
        .genre-header {{ border-bottom: 2px solid #252535; padding-bottom: 10px; margin-bottom: 30px; }}
        .genre-title {{ font-size: 2rem; margin: 0; }}
        .movies-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 35px; }}
        .movie-card {{ background-color: var(--card-bg); border-radius: 14px; overflow: hidden; box-shadow: 0 6px 18px rgba(0,0,0,0.4); text-decoration: none; color: inherit; display: flex; flex-direction: column; border: 1px solid #222232; transition: transform 0.3s; }}
        .movie-card:hover {{ transform: translateY(-5px); border-color: var(--primary); }}
        .poster-wrapper {{ width: 100%; height: 350px; position: relative; }}
        .poster-wrapper img {{ width: 100%; height: 100%; object-fit: cover; }}
        .rating-badge {{ position: absolute; top: 15px; right: 15px; background-color: rgba(0, 0, 0, 0.85); color: #ffc107; padding: 5px 10px; border-radius: 6px; font-weight: bold; }}
        .movie-content {{ padding: 20px; flex-grow: 1; }}
        .movie-title {{ font-size: 1.2rem; font-weight: 700; margin: 0 0 8px 0; }}
        .movie-meta {{ font-size: 0.9rem; color: var(--text-muted); }}
        footer {{ text-align: center; padding: 40px 20px; color: var(--text-muted); background-color: #0b0b0e; border-top: 1px solid #1c1c28; }}
        {MODAL_STYLES}
    </style>
</head>
<body>
    <header><h1>Films_Iliaz</h1><p>Индивидуальная онлайн-галерея твоих любимых фильмов</p></header>
    <div class="container">
        {{% for genre in ["Фантастика", "Боевики", "Комедии", "Ужасы"] %}}
        <div class="genre-section">
            <div class="genre-header"><h2 class="genre-title">{{{{ genre }}}}</h2></div>
            <div class="movies-grid">
                {{% for movie in movies if movie.genre == genre %}}
                <a href="{{{{ url_for('movie_detail', movie_id=movie.id) }}}}" class="movie-card">
                    <div class="poster-wrapper">
                        <img src="{{{{ url_for('proxy_image', url=movie.poster) }}}}" alt="{{{{ movie.title }}}}">
                        <div class="rating-badge">★ {{{{ movie.rating }}}}</div>
                    </div>
                    <div class="movie-content">
                        <div class="movie-title">{{{{ movie.title }}}}</div>
                        <div class="movie-meta">{{{{ movie.year }}}} • {{{{ movie.duration }}}}</div>
                    </div>
                </a>
                {{% endfor %}}
            </div>
        </div>
        {{% endfor %}}
    </div>
    <footer>
        <div>&copy; 2026 Films_Iliaz. Все права защищены.</div>
        <div class="footer-links">
            <a onclick="openModal('aboutModal')">О сайте</a>
            <a onclick="openModal('adminModal')">Связаться с админом</a>
            <a onclick="openModal('cookieModal')">Файлы cookie</a>
        </div>
    </footer>
    <div id="aboutModal" class="modal-overlay"><div class="modal-box"><button class="modal-close" onclick="closeModal('aboutModal')">&times;</button><h3>О проекте</h3><p>Films_Iliaz — это современный кинотеатр на Flask.</p></div></div>
    <div id="adminModal" class="modal-overlay"><div class="modal-box"><button class="modal-close" onclick="closeModal('adminModal')">&times;</button><h3>Контакты</h3><div class="admin-contact-item">Email: admin@films-iliaz.ru</div><div class="admin-contact-item">Telegram: @iliaz_media</div></div></div>
    <div id="cookieModal" class="modal-overlay"><div class="modal-box"><button class="modal-close" onclick="closeModal('cookieModal')">&times;</button><h3>Файлы Cookie</h3><p>Мы используем их для удобства работы.</p></div></div>
    {MODAL_SCRIPT}
</body>
</html>
"""

MOVIE_HTML = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{{{ movie.title }}}} — Films_Iliaz</title>
    {AD_CODE}
    <style>
        :root {{ --bg-dark: #0f0f12; --card-bg: #1a1a24; --primary: #ff4a5a; --accent-green: #00c853; --text-main: #ffffff; --text-muted: #a0a0b0; }}
        body {{ font-family: 'Segoe UI', Roboto, sans-serif; background-color: var(--bg-dark); color: var(--text-main); margin: 0; padding: 0; }}
        header {{ background-color: #161623; padding: 20px 40px; border-bottom: 3px solid var(--primary); display: flex; justify-content: space-between; align-items: center; }}
        .back-btn {{ color: white; text-decoration: none; background-color: #2b2b3d; padding: 10px 20px; border-radius: 8px; }}
        .container {{ max-width: 1100px; margin: 50px auto; padding: 0 25px; }}
        .movie-main-box {{ display: flex; gap: 50px; background-color: var(--card-bg); padding: 40px; border-radius: 16px; border: 1px solid #222232; }}
        .poster-box {{ width: 320px; height: 470px; border-radius: 12px; overflow: hidden; }}
        .poster-box img {{ width: 100%; height: 100%; object-fit: cover; }}
        .watch-link {{ display: inline-block; background-color: var(--accent-green); color: black; padding: 14px 35px; border-radius: 8px; font-weight: bold; text-decoration: none; margin-bottom: 25px; }}
        .reviews-wrapper {{ background-color: var(--card-bg); padding: 40px; border-radius: 16px; margin-top: 40px; }}
        .input-field {{ width: 100%; padding: 12px; border-radius: 8px; border: 1px solid #3a3a52; background-color: #121218; color: white; margin-bottom: 15px; }}
        .btn-submit {{ background-color: var(--primary); color: white; border: none; padding: 12px 25px; border-radius: 8px; cursor: pointer;}}
        {MODAL_STYLES}
    </style>
</head>
<body>
    <header><h1>Films_Iliaz</h1><a href="{{{{ url_for('index') }}}}" class="back-btn">← На главную</a></header>
    <div class="container">
        <div class="movie-main-box">
            <div class="poster-box"><img src="{{{{ url_for('proxy_image', url=movie.poster) }}}}" alt="{{{{ movie.title }}}}"></div>
            <div class="info-box">
                <h2>{{{{ movie.title }}}} ({{{{ movie.year }}}})</h2>
                <a href="{{{{ movie.video_url }}}}" target="_blank" class="watch-link">Смотреть на Кинопоиске</a>
                <p>{{{{ movie.description }}}}</p>
            </div>
        </div>
        <div class="reviews-wrapper">
            <h3>Отзывы</h3>
            {{% for r in reviews %}}<p><strong>{{{{ r.name }}}}:</strong> {{{{ r.text }}}}</p>{{% endfor %}}
            <form action="{{{{ url_for('movie_detail', movie_id=movie.id) }}}}" method="POST">
                <input type="text" name="name" class="input-field" placeholder="Ваше имя" required>
                <textarea name="review_text" class="input-field" placeholder="Ваш отзыв" required></textarea>
                <button type="submit" class="btn-submit">Отправить</button>
            </form>
        </div>
    </div>
    {MODAL_SCRIPT}
</body>
</html>
"""

@app.route('/proxy-image')
def proxy_image():
    image_url = request.args.get('url')
    if not image_url: return "Missing url", 400
    try:
        req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://kinogo.my/'})
        with urllib.request.urlopen(req, timeout=12) as response:
            return Response(response.read(), content_type=response.headers.get('Content-Type', 'image/jpeg'))
    except Exception as e: return f"Error: {str(e)}", 500

@app.route('/')
def index():
    return render_template_string(INDEX_HTML, movies=MOVIES)

@app.route('/movie/<int:movie_id>', methods=['GET', 'POST'])
def movie_detail(movie_id):
    movie = next((m for m in MOVIES if m["id"] == movie_id), None)
    if not movie: return "Фильм не найден", 404
    if request.method == 'POST':
        name = request.form.get('name', 'Аноним').strip()
        text = request.form.get('review_text', '').strip()
        if text: REVIEWS[movie_id].append({"name": name, "text": text})
        return redirect(url_for('movie_detail', movie_id=movie_id))
    return render_template_string(MOVIE_HTML, movie=movie, reviews=REVIEWS.get(movie_id, []))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
