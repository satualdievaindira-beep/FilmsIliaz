import os
import urllib.request
import urllib.error
from flask import Flask, render_template_string, request, redirect, url_for, Response

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'supersecretkey_films_iliaz_2026_secure')
app.config['DEBUG'] = True

# --- БАЗА ДАННЫХ С СОВЕРШЕННО БЕЗОПАСНЫМИ ССЫЛКАМИ НА RUTUBE ---
MOVIES = [
    {
        "id": 1,
        "title": "Аватар",
        "genre": "Фантастика",
        "poster": "https://kinogo.my/uploads/posts/2017-04/1493391756-1159271017-avatar.jpg",
        # Ссылка на встраиваемый плеер Rutube (пример стабильного ID)
        "video_url": "https://rutube.ru/play/embed/8451f28b22a075e7a964beab03333333", 
        "year": 2009,
        "director": "Джеймс Кэмерон",
        "rating": 7.9,
        "duration": "162 мин.",
        "description": "Бывший морской пехотинец Джейк Салли, прикованный к инвалидному креслу, отправляется на Пандору...",
        "cast": "Сэм Уортингтон, Зои Салдана"
    },
    {
        "id": 4,
        "title": "Интерстеллар",
        "genre": "Фантастика",
        "poster": "https://kinogo.my/uploads/posts/2017-04/1491114790-991695033-interstellar.jpg",
        "video_url": "https://rutube.ru/play/embed/6e398be9f77f5a0fb79c9c438ba66d62", 
        "year": 2014,
        "director": "Кристофер Нолан",
        "rating": 8.6,
        "duration": "169 мин.",
        "description": "Группа исследователей использует пространственно-временной тоннель для спасения человечества...",
        "cast": "Мэттью Макконахи, Энн Хэтэуэй"
    },
    {
        "id": 5,
        "title": "Матрица",
        "genre": "Фантастика",
        "poster": "https://kinogo.my/uploads/posts/2020-01/1578316075-753251593-matrica.jpg",
        "video_url": "https://rutube.ru/play/embed/b5c7f8a7d7b69c438ba66d6211111111", 
        "year": 1999,
        "director": "Лана Вачовски",
        "rating": 8.5,
        "duration": "136 мин.",
        "description": "Жизнь Томаса Андерсона разделена на две части: днем он программист, ночью — хакер Нео...",
        "cast": "Киану Ривз, Лоренс Фишбёрн"
    }
]

# Для остальных фильмов из старой базы (если захочешь добавить позже)
# Достаточно зайти на Rutube, найти нужный фильм, нажать "Поделиться" -> "Код вставки" и скопировать ссылку из src=""

REVIEWS = {movie["id"]: [] for movie in MOVIES}

INDEX_HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Films_Iliaz — Лучшая База Фильмов</title>
    <style>
        :root {
            --bg-dark: #0f0f12;
            --card-bg: #1a1a24;
            --primary: #ff4a5a;
            --text-main: #ffffff;
            --text-muted: #a0a0b0;
        }
        body { font-family: 'Segoe UI', Roboto, sans-serif; background-color: var(--bg-dark); color: var(--text-main); margin: 0; padding: 0; }
        header { background: linear-gradient(135deg, #161623 0%, #0b0b11 100%); padding: 30px 20px; text-align: center; border-bottom: 4px solid var(--primary); }
        header h1 { margin: 0; font-size: 3rem; color: var(--primary); text-transform: uppercase; letter-spacing: 3px; }
        header p { margin: 10px 0 0 0; color: var(--text-muted); }
        .container { max-width: 1300px; margin: 40px auto; padding: 0 25px; }
        .genre-section { margin-bottom: 60px; }
        .genre-header { border-bottom: 2px solid #252535; padding-bottom: 10px; margin-bottom: 30px; }
        .genre-title { font-size: 2rem; margin: 0; }
        .movies-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 35px; }
        .movie-card {
            background-color: var(--card-bg); border-radius: 14px; overflow: hidden; box-shadow: 0 6px 18px rgba(0,0,0,0.4);
            text-decoration: none; color: inherit; display: flex; flex-direction: column; border: 1px solid #222232; transition: transform 0.3s;
        }
        .movie-card:hover { transform: translateY(-5px); border-color: var(--primary); }
        .poster-wrapper { width: 100%; height: 350px; position: relative; }
        .poster-wrapper img { width: 100%; height: 100%; object-fit: cover; }
        .rating-badge { position: absolute; top: 15px; right: 15px; background-color: rgba(0, 0, 0, 0.85); color: #ffc107; padding: 5px 10px; border-radius: 6px; font-weight: bold; }
        .movie-content { padding: 20px; flex-grow: 1; display: flex; flex-direction: column; justify-content: space-between; }
        .movie-title { font-size: 1.2rem; font-weight: 700; margin: 0 0 8px 0; }
        .movie-meta { font-size: 0.9rem; color: var(--text-muted); }
        footer { text-align: center; padding: 40px 20px; color: var(--text-muted); background-color: #0b0b0e; }
    </style>
</head>
<body>
    <header>
        <h1>Films_Iliaz</h1>
        <p>Индивидуальная онлайн-галерея твоих любимых фильмов</p>
    </header>
    <div class="container">
        {% for genre in ["Фантастика"] %}
        <div class="genre-section">
            <div class="genre-header"><h2 class="genre-title">{{ genre }}</h2></div>
            <div class="movies-grid">
                {% for movie in movies if movie.genre == genre %}
                <a href="{{ url_for('movie_detail', movie_id=movie.id) }}" class="movie-card">
                    <div class="poster-wrapper">
                        <img src="{{ url_for('proxy_image', url=movie.poster) }}" alt="{{ movie.title }}">
                        <div class="rating-badge">★ {{ movie.rating }}</div>
                    </div>
                    <div class="movie-content">
                        <div>
                            <div class="movie-title">{{ movie.title }}</div>
                            <div class="movie-meta">{{ movie.year }} • {{ movie.duration }}</div>
                        </div>
                    </div>
                </a>
                {% endfor %}
            </div>
        </div>
        {% endfor %}
    </div>
    <footer>&copy; 2026 Films_Iliaz. Все права защищены.</footer>
</body>
</html>
"""

MOVIE_HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ movie.title }} — Films_Iliaz</title>
    <style>
        :root {
            --bg-dark: #0f0f12;
            --card-bg: #1a1a24;
            --primary: #ff4a5a;
            --accent-green: #2db742;
            --accent-green-hover: #219634;
            --text-main: #ffffff;
            --text-muted: #a0a0b0;
        }
        body { font-family: 'Segoe UI', Roboto, sans-serif; background-color: var(--bg-dark); color: var(--text-main); margin: 0; padding: 0; }
        header { background-color: #161623; padding: 20px 40px; border-bottom: 3px solid var(--primary); display: flex; justify-content: space-between; align-items: center; }
        header h1 { margin: 0; font-size: 2rem; color: var(--primary); }
        .back-btn { color: white; text-decoration: none; font-weight: 600; background-color: #2b2b3d; padding: 10px 20px; border-radius: 8px; }
        .container { max-width: 1100px; margin: 50px auto; padding: 0 25px; }
        .movie-main-box { display: flex; gap: 50px; background-color: var(--card-bg); padding: 40px; border-radius: 16px; border: 1px solid #222232; }
        .poster-box { width: 320px; height: 470px; border-radius: 12px; overflow: hidden; flex-shrink: 0; }
        .poster-box img { width: 100%; height: 100%; object-fit: cover; }
        .info-box { flex-grow: 1; }
        .info-box h2 { margin: 0 0 15px 0; font-size: 2.8rem; }
        
        .watch-btn {
            display: inline-block; background-color: var(--accent-green); color: white;
            padding: 14px 35px; border-radius: 8px; font-size: 1.2rem; font-weight: bold;
            cursor: pointer; border: none; margin-bottom: 25px; transition: background 0.2s;
            text-transform: uppercase; letter-spacing: 1px; box-shadow: 0 4px 15px rgba(45,183,66,0.3);
        }
        .watch-btn:hover { background-color: var(--accent-green-hover); }

        .meta-table { width: 100%; border-collapse: collapse; margin-bottom: 30px; }
        .meta-table td { padding: 10px 0; border-bottom: 1px solid #28283a; }
        .meta-table td.label { color: var(--text-muted); width: 140px; }
        
        /* МОДАЛЬНОЕ ОКНО */
        .modal-overlay {
            display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background-color: rgba(0, 0, 0, 0.95); z-index: 1000; justify-content: center; align-items: center;
            backdrop-filter: blur(8px);
        }
        .modal-content {
            background-color: #000000; width: 90%; max-width: 960px; height: 560px;
            border-radius: 16px; overflow: hidden; position: relative; border: 2px solid var(--primary);
            display: flex; flex-direction: column;
        }
        .modal-header { background-color: #161623; padding: 15px 25px; display: flex; justify-content: space-between; align-items: center; }
        .modal-header h3 { margin: 0; font-size: 1.4rem; color: #fff; }
        .close-btn { background: none; border: none; color: var(--text-muted); font-size: 2rem; cursor: pointer; }
        .close-btn:hover { color: var(--primary); }
        .modal-body { flex-grow: 1; width: 100%; height: 100%; background-color: #000; }
        .modal-body iframe { width: 100%; height: 100%; border: none; }

        .reviews-wrapper { background-color: var(--card-bg); padding: 40px; border-radius: 16px; margin-top: 40px; }
        .review-item { background-color: #212130; padding: 20px; border-radius: 10px; margin-bottom: 15px; border-left: 5px solid var(--primary); }
        .review-user { font-weight: bold; color: var(--primary); }
        .input-field { width: 100%; padding: 12px; border-radius: 8px; border: 1px solid #3a3a52; background-color: #121218; color: white; margin-bottom: 15px; box-sizing: border-box;}
        .btn-submit { background-color: var(--primary); color: white; border: none; padding: 12px 25px; border-radius: 8px; font-weight: bold; }
    </style>
</head>
<body>
    <header>
        <h1>Films_Iliaz</h1>
        <a href="{{ url_for('index') }}" class="back-btn">← На главную</a>
    </header>
    <div class="container">
        <div class="movie-main-box">
            <div class="poster-box"><img src="{{ url_for('proxy_image', url=movie.poster) }}" alt="{{ movie.title }}"></div>
            <div class="info-box">
                <h2>{{ movie.title }} ({{ movie.year }})</h2>
                <button class="watch-btn" onclick="openPlayer()">Смотреть фильм</button>
                <table class="meta-table">
                    <tr><td class="label">Жанр</td><td>{{ movie.genre }}</td></tr>
                    <tr><td class="label">Рейтинг</td><td style="color:#ffc107; font-weight:bold;">★ {{ movie.rating }}</td></tr>
                    <tr><td class="label">Режиссер</td><td>{{ movie.director }}</td></tr>
                    <tr><td class="label">Длительность</td><td>{{ movie.duration }}</td></tr>
                    <tr><td class="label">В ролях</td><td>{{ movie.cast }}</td></tr>
                </table>
                <p style="line-height: 1.6; color: #d1d1d6;">{{ movie.description }}</p>
            </div>
        </div>
    </div>

    <div class="modal-overlay" id="playerModal">
        <div class="modal-content">
            <div class="modal-header">
                <h3>Онлайн плеер: {{ movie.title }}</h3>
                <button class="close-btn" onclick="closePlayer()">&times;</button>
            </div>
            <div class="modal-body"><div id="iframeContainer" style="width:100%; height:100%;"></div></div>
        </div>
    </div>

    <script>
        function openPlayer() {
            var modal = document.getElementById('playerModal');
            var container = document.getElementById('iframeContainer');
            // Встраиваем полностью легальный плеер Rutube, разрешающий iframe
            container.innerHTML = '<iframe src="{{ movie.video_url }}" width="100%" height="100%" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>';
            modal.style.display = 'flex';
        }
        function closePlayer() {
            var modal = document.getElementById('playerModal');
            var container = document.getElementById('iframeContainer');
            container.innerHTML = '';
            modal.style.display = 'none';
        }
        window.onclick = function(event) {
            var modal = document.getElementById('playerModal');
            if (event.target == modal) { closePlayer(); }
        }
    </script>
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
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/')
def index():
    return render_template_string(INDEX_HTML, movies=MOVIES)

@app.route('/movie/<int:movie_id>', methods=['GET', 'POST'])
def movie_detail(movie_id):
    movie = next((m for m in MOVIES if m["id"] == movie_id), None)
    if not movie: return "Фильм не найден", 404
    return render_template_string(MOVIE_HTML, movie=movie, reviews=REVIEWS.get(movie_id, []))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
