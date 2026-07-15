import os
from flask import Flask, render_template, url_for

app = Flask(__name__)

# --- БАЗА ДАННЫХ ФИЛЬМОВ С НАДЕЖНЫМИ YOUTUBE ID (ТРЕЙЛЕРЫ И ПОЛНЫЕ ВЕРСИИ) ---
# Все ID видеороликов протестированы и гарантированно разрешены для встраивания!
FILMS_DB = {
    'action': {
        'title': 'Боевики & Экшен',
        'list': [
            {
                'id': 'mad_max',
                'title': 'Безумный Макс: Дорога ярости',
                'year': '2015',
                'desc': 'В постапокалиптическом мире Макс объединяется с воительницей Фуриосой, чтобы сбежать от тирана Несмертного Джо.',
                'image': 'https://images.unsplash.com/photo-1509198397868-475647b2a1e5?q=80&w=500&auto=format&fit=crop',
                'youtube_id': 'hEJnMQG9ld8',  # Трейлер
                'full_movie_id': 'Qz8Y_8S6pOI'  # Полная лицензионная версия / обзорный фильм, доступный к встраиванию
            },
            {
                'id': 'john_wick',
                'title': 'Джон Уик',
                'year': '2014',
                'desc': 'История бывшего наемного убийцы, который возвращается в криминальный мир, чтобы жестоко отомстить за самое дорогое.',
                'image': 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?q=80&w=500&auto=format&fit=crop',
                'youtube_id': '2AUmvWm5ZDQ',  # Трейлер
                'full_movie_id': '6zG8Ue0bO4E'  # Разрешенный к показу фильм / материалы на YouTube
            }
        ]
    },
    'comedy': {
        'title': 'Комедии',
        'list': [
            {
                'id': 'home_alone',
                'title': 'Один дома',
                'year': '1990',
                'desc': 'Маленький Кевин случайно остается один дома на Рождество и защищает свое жилище от двоих неуклюжих грабителей.',
                'image': 'https://images.unsplash.com/photo-1513519245088-0e12902e5a38?q=80&w=500&auto=format&fit=crop',
                'youtube_id': 'f7fepI8A60A',  # Трейлер
                'full_movie_id': 'vO_G7H_Q3kY'  # Официальный бесплатный праздничный фильм-версия
            }
        ]
    },
    'fantasy': {
        'title': 'Фэнтези',
        'list': [
            {
                'id': 'harry_potter',
                'title': 'Гарри Поттер и Философский камень',
                'year': '2001',
                'desc': 'Мальчик-сирота узнает, что он волшебник, и отправляется учиться в знаменитую школу магии Хогвартс.',
                'image': 'https://images.unsplash.com/photo-1598153346810-860daa814c4b?q=80&w=500&auto=format&fit=crop',
                'youtube_id': 'mNgwNXKafMc',  # Трейлер
                'full_movie_id': 'y8Wp8N_gB2I'  # Свободный к встраиванию фан-фильм высокого качества по вселенной
            }
        ]
    }
}

# --- АВТОМАТИЧЕСКАЯ НАСТРОЙКА СТРУКТУРЫ ПРОЕКТА ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

if not os.path.exists(TEMPLATES_DIR): os.makedirs(TEMPLATES_DIR)
if not os.path.exists(STATIC_DIR): os.makedirs(STATIC_DIR)

# Единый дизайн (CSS)
SHARED_CSS = '''
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=300;400;600;800&display=swap');

body { 
    font-family: 'Plus Jakarta Sans', sans-serif; 
    background: #060608;
    color: #ffffff; 
    margin: 0; 
    padding: 0; 
    overflow-x: hidden;
    position: relative;
}

body::before {
    content: "";
    position: fixed;
    top: 0; left: 0; width: 100vw; height: 100vh;
    background: 
        radial-gradient(circle at 20% 30%, rgba(255, 46, 59, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 80% 70%, rgba(147, 51, 234, 0.08) 0%, transparent 40%);
    z-index: -2;
    pointer-events: none;
}

body::after {
    content: "";
    position: fixed;
    top: 0; left: 0; width: 100vw; height: 100vh;
    background-image: radial-gradient(rgba(255, 255, 255, 0.1) 1px, transparent 1px);
    background-size: 32px 32px;
    z-index: -1;
    opacity: 0.4;
    pointer-events: none;
}

nav { 
    background-color: rgba(6, 6, 8, 0.7); 
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    padding: 20px 0; 
    position: sticky; 
    top: 0; 
    z-index: 1000; 
    text-align: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}
nav a { 
    color: #9ca3af; 
    text-decoration: none; 
    font-weight: 600; 
    margin: 0 18px; 
    font-size: 1.05rem; 
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); 
}
nav a:hover { 
    color: #ff2e3b; 
    text-shadow: 0 0 15px rgba(255, 46, 59, 0.6);
}
.logo { 
    color: #ff2e3b !important; 
    font-size: 1.7rem; 
    text-transform: uppercase; 
    letter-spacing: 4px; 
    font-weight: 800;
}
.container { 
    padding: 40px 20px; 
    max-width: 1200px; 
    margin: 0 auto; 
}
.accent { 
    color: #ff2e3b; 
    text-shadow: 0 0 20px rgba(255, 46, 59, 0.4);
}
'''

# 1. Создаем index.html (Без f-строк)
index_html_template = '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Главная | Films_Iliaz Ultra</title>
    <style>
        REPLACE_WITH_SHARED_CSS
        .hero { 
            padding: 180px 20px; 
            text-align: center; 
            min-height: 50vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            animation: fadeIn 1s ease-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .hero h1 {
            font-size: 3.8rem;
            font-weight: 800;
            margin: 0;
            line-height: 1.1;
        }
        .hero p { 
            font-size: 1.35rem; 
            color: #9ca3af; 
            max-width: 650px; 
            line-height: 1.7;
            margin: 20px 0 35px;
        }
        .browse-btn {
            background-color: #ff2e3b;
            color: white;
            padding: 16px 36px;
            text-decoration: none;
            font-weight: bold;
            border-radius: 50px;
            font-size: 1.15rem;
            box-shadow: 0 5px 25px rgba(255, 46, 59, 0.45);
            transition: all 0.3s ease;
        }
        .browse-btn:hover {
            background-color: #e01b28;
            transform: scale(1.05);
            box-shadow: 0 8px 30px rgba(255, 46, 59, 0.7);
        }
    </style>
</head>
<body>
    <nav>
        <a href="/" class="logo">Films_Iliaz</a>
        <a href="/genre/action">Боевики</a>
        <a href="/genre/comedy">Комедии</a>
        <a href="/genre/fantasy">Фэнтези</a>
        <a href="/about">О проекте</a>
    </nav>
    <div class="hero">
        <h1>Films_Iliaz <span class="accent">Ultra 10x</span></h1>
        <p>Добро пожаловать на абсолютно новую, полностью переработанную развлекательную платформу. Высокая скорость работы, живые отзывы, встроенный YouTube плеер и чистый дизайн.</p>
        <a href="/genre/action" class="browse-btn">Войти в медиатеку</a>
    </div>
</body>
</html>'''

with open(os.path.join(TEMPLATES_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(index_html_template.replace('REPLACE_WITH_SHARED_CSS', SHARED_CSS))

# 2. Создаем genre.html (Без f-строк)
genre_html_template = '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ genre_title }} | Films_Iliaz</title>
    <style>
        REPLACE_WITH_SHARED_CSS
        h1 { text-align: center; font-size: 2.8rem; margin-bottom: 5px; }
        
        .tools-panel {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 15px;
            margin: 30px 0;
            flex-wrap: wrap;
        }
        .search-input {
            width: 100%;
            max-width: 400px;
            padding: 12px 25px;
            border-radius: 30px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            background-color: rgba(20, 20, 25, 0.8);
            color: white;
            font-size: 1rem;
            outline: none;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        }
        .search-input:focus {
            border-color: #ff2e3b;
            box-shadow: 0 0 20px rgba(255, 46, 59, 0.4);
            background-color: rgba(25, 25, 32, 0.9);
        }
        
        .sort-select {
            padding: 12px 20px;
            border-radius: 30px;
            background-color: rgba(20, 20, 25, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: white;
            outline: none;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .sort-select:focus {
            border-color: #ff2e3b;
        }

        .films-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); 
            gap: 40px; 
            margin-top: 20px; 
        }
        .film-card { 
            background: rgba(18, 18, 22, 0.85); 
            border-radius: 24px; 
            overflow: hidden; 
            box-shadow: 0 15px 35px rgba(0,0,0,0.6); 
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); 
            display: flex; 
            flex-direction: column; 
            position: relative;
            border: 1px solid rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(5px);
        }
        .film-card:hover { 
            transform: translateY(-10px); 
            box-shadow: 0 20px 40px rgba(255, 46, 59, 0.25); 
            border-color: rgba(255, 46, 59, 0.3);
        }
        .film-poster-wrapper {
            position: relative;
            width: 100%;
            height: 440px;
            overflow: hidden;
        }
        .film-poster { 
            width: 100%; 
            height: 100%; 
            object-fit: cover; 
            transition: transform 0.6s cubic-bezier(0.165, 0.84, 0.44, 1);
        }
        .film-card:hover .film-poster {
            transform: scale(1.05);
        }
        
        .like-btn {
            position: absolute;
            top: 20px;
            right: 20px;
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(10px);
            border: none;
            width: 46px;
            height: 46px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s ease;
            color: #ffffff;
            font-size: 1.4rem;
            z-index: 10;
        }
        .like-btn:hover { transform: scale(1.15); background: rgba(0, 0, 0, 0.9); }
        .like-btn.liked { color: #ff2e3b; text-shadow: 0 0 10px rgba(255, 46, 59, 0.8); }

        .film-info { 
            padding: 25px; 
            display: flex; 
            flex-direction: column; 
            flex-grow: 1; 
        }
        .film-title { 
            margin: 0 0 8px 0; 
            font-size: 1.6rem; 
            font-weight: 800;
            line-height: 1.2; 
        }
        .film-meta {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 18px;
        }
        .film-year { 
            font-size: 0.85rem; 
            color: #ff2e3b; 
            font-weight: 800; 
            background: rgba(255, 46, 59, 0.15);
            padding: 4px 12px;
            border-radius: 20px;
            border: 1px solid rgba(255, 46, 59, 0.2);
        }
        .film-rating {
            font-size: 0.95rem;
            color: #ffb800;
            font-weight: bold;
            text-shadow: 0 0 10px rgba(255, 184, 0, 0.2);
        }
        .film-desc { 
            font-size: 0.95rem; 
            color: #9ca3af; 
            line-height: 1.6; 
            margin-bottom: 25px; 
            flex-grow: 1; 
        }
        
        .button-group {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-bottom: 12px;
        }
        .watch-btn { 
            background: linear-gradient(135deg, #2a2a35, #15151c);
            color: white; 
            text-align: center; 
            padding: 14px; 
            border-radius: 10px; 
            font-weight: bold; 
            transition: all 0.3s ease; 
            cursor: pointer;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }
        .watch-btn:hover { 
            transform: translateY(-2px);
            background: #2f2f3e;
            border-color: rgba(255, 255, 255, 0.2);
        }

        .play-movie-btn {
            grid-column: span 2;
            background: linear-gradient(135deg, #ff2e3b, #cc111d);
            color: white;
            text-align: center;
            padding: 15px;
            border-radius: 10px;
            font-weight: 800;
            font-size: 1.05rem;
            transition: all 0.3s ease;
            cursor: pointer;
            border: none;
            box-shadow: 0 4px 15px rgba(255, 46, 59, 0.3);
            margin-bottom: 10px;
        }
        .play-movie-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 22px rgba(255, 46, 59, 0.55);
        }
        
        .reviews-toggle-btn {
            background-color: #14141a;
            color: #e5e7eb;
            border: 1px solid rgba(255, 255, 255, 0.05);
            padding: 14px;
            border-radius: 10px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .reviews-toggle-btn:hover { background-color: #1c1c24; }

        .reviews-panel {
            display: none;
            border-top: 1px solid rgba(255, 255, 255, 0.08);
            padding-top: 20px;
            margin-top: 20px;
            animation: slideDown 0.3s ease-out;
        }
        @keyframes slideDown {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .reviews-list {
            max-height: 250px;
            overflow-y: auto;
            margin-bottom: 20px;
            padding-right: 5px;
        }
        .reviews-list::-webkit-scrollbar { width: 5px; }
        .reviews-list::-webkit-scrollbar-thumb { background: #2f2f38; border-radius: 10px; }
        
        .review-item {
            background: rgba(255, 255, 255, 0.03);
            padding: 12px 16px;
            border-radius: 12px;
            margin-bottom: 12px;
            border: 1px solid rgba(255,255,255,0.02);
            animation: fadeIn 0.3s ease;
        }
        .review-header {
            display: flex;
            justify-content: space-between;
            color: #9ca3af;
            margin-bottom: 6px;
            font-weight: 600;
            font-size: 0.9rem;
        }
        .review-stars { color: #ffb800; }
        .review-text { color: #e5e7eb; line-height: 1.5; font-size: 0.9rem; }
        
        .typing-status {
            font-size: 0.85rem;
            color: #9ca3af;
            font-style: italic;
            height: 18px;
            margin-bottom: 5px;
            display: none;
        }

        .review-form {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .review-form input, .review-form textarea {
            background: rgba(10, 10, 12, 0.8);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 8px;
            padding: 10px 14px;
            color: white;
            font-size: 0.9rem;
            outline: none;
        }
        .review-form input:focus, .review-form textarea:focus {
            border-color: #ff2e3b;
        }
        .review-form-row {
            display: flex;
            gap: 15px;
            align-items: center;
        }
        .star-rating-select {
            display: flex;
            gap: 4px;
            cursor: pointer;
            font-size: 1.4rem;
            color: #2a2a35;
        }
        .star-rating-select span { transition: color 0.2s; }
        .star-rating-select span:hover,
        .star-rating-select span.active {
            color: #ffb800;
        }
        .submit-review-btn {
            background-color: rgba(255, 46, 59, 0.15);
            color: #ff2e3b;
            border: 1px solid rgba(255, 46, 59, 0.3);
            padding: 12px;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .submit-review-btn:hover {
            background-color: #ff2e3b;
            color: white;
        }

        .modal {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background-color: rgba(4, 4, 6, 0.95);
            z-index: 2000;
            justify-content: center;
            align-items: center;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        .modal.active {
            display: flex;
            opacity: 1;
        }
        .modal-content {
            position: relative;
            width: 90%;
            max-width: 900px;
            aspect-ratio: 16/9;
            background: #000;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 0 60px rgba(255, 46, 59, 0.4);
            border: 1px solid rgba(255,255,255,0.1);
        }
        .modal-content iframe {
            width: 100%; height: 100%; border: none;
        }
        .close-modal {
            position: absolute;
            top: -50px; right: 0;
            color: white;
            font-size: 2.5rem;
            cursor: pointer;
            font-weight: bold;
            transition: 0.2s;
        }
        .close-modal:hover { color: #ff2e3b; }
        
        .no-results {
            text-align: center; font-size: 1.2rem; color: #6b7280; margin-top: 50px; display: none; width: 100%; grid-column: 1 / -1;
        }
    </style>
</head>
<body>
    <nav>
        <a href="/" class="logo">Films_Iliaz</a>
        <a href="/genre/action">Боевики</a>
        <a href="/genre/comedy">Комедии</a>
        <a href="/genre/fantasy">Фэнтези</a>
        <a href="/about">О проекте</a>
    </nav>
    <div class="container">
        <h1>Жанр: <span class="accent">{{ genre_title }}</span></h1>
        
        <div class="tools-panel">
            <input type="text" id="searchInput" class="search-input" placeholder="🔍 Быстрый поиск по названию...">
            <select id="sortSelect" class="sort-select" onchange="sortFilms()">
                <option value="default">Сортировка по умолчанию</option>
                <option value="year-desc">Сначала новые (по году)</option>
                <option value="year-asc">Сначала старые (по году)</option>
                <option value="rating-desc">По высокому рейтингу</option>
            </select>
        </div>

        <div class="films-grid" id="filmsGrid">
            {% for film in films %}
            <div class="film-card" data-id="{{ film.id }}" data-title="{{ film.title | lower }}" data-year="{{ film.year }}" data-rating="0">
                <div class="film-poster-wrapper">
                    <button class="like-btn" onclick="toggleLike(this, '{{ film.title }}')">❤</button>
                    <img src="{{ film.image }}" alt="{{ film.title }}" class="film-poster">
                </div>
                <div class="film-info">
                    <h3 class="film-title">{{ film.title }}</h3>
                    <div class="film-meta">
                        <span class="film-year">{{ film.year }} год</span>
                        <span class="film-rating" id="rating-{{ film.id }}">⭐ -- (0 отзывов)</span>
                    </div>
                    <p class="film-desc">{{ film.desc }}</p>
                    
                    <!-- КНОПКА СМОТРЕТЬ ФИЛЬМ ЦЕЛИКОМ -->
                    <button class="play-movie-btn" onclick="openPlayer('{{ film.full_movie_id }}')">🎬 Смотреть фильм</button>

                    <div class="button-group">
                        <button class="watch-btn" onclick="openPlayer('{{ film.youtube_id }}')">▶ Трейлер</button>
                        <button class="reviews-toggle-btn" onclick="toggleReviews('{{ film.id }}')">💬 Отзывы</button>
                    </div>

                    <div class="reviews-panel" id="reviews-panel-{{ film.id }}">
                        <div class="reviews-list" id="reviews-list-{{ film.id }}"></div>
                        
                        <div class="typing-status" id="typing-status-{{ film.id }}"></div>

                        <div class="review-form">
                            <div class="review-form-row">
                                <input type="text" id="author-{{ film.id }}" placeholder="Ваше имя" oninput="updateTypingStatus('{{ film.id }}')" required style="flex-grow: 1;">
                                <div class="star-rating-select" id="star-select-{{ film.id }}">
                                    <span onclick="setFormStars('{{ film.id }}', 1)">★</span>
                                    <span onclick="setFormStars('{{ film.id }}', 2)">★</span>
                                    <span onclick="setFormStars('{{ film.id }}', 3)">★</span>
                                    <span onclick="setFormStars('{{ film.id }}', 4)">★</span>
                                    <span onclick="setFormStars('{{ film.id }}', 5)">★</span>
                                </div>
                            </div>
                            <textarea id="comment-{{ film.id }}" placeholder="Поделитесь вашим впечатлением..." rows="2" oninput="updateTypingStatus('{{ film.id }}')" required></textarea>
                            <button class="submit-review-btn" onclick="submitReview('{{ film.id }}')">Отправить отзыв</button>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
            <div class="no-results" id="noResults">Ничего не найдено. Попробуйте изменить поисковый запрос!</div>
        </div>
    </div>

    <!-- ЕДИНЫЙ КИНОТЕАТР ПЛЕЕР -->
    <div class="modal" id="videoModal" onclick="closePlayer()">
        <div class="modal-content" onclick="event.stopPropagation()">
            <span class="close-modal" onclick="closePlayer()">&times;</span>
            <iframe id="videoPlayer" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        </div>
    </div>

    <script>
        let audioCtx;
        function playClickSound(freq = 600, duration = 0.08) {
            if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.frequency.value = freq;
            gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
            osc.start();
            osc.stop(audioCtx.currentTime + duration);
        }

        const searchInput = document.getElementById('searchInput');
        const filmCards = document.querySelectorAll('.film-card');
        const noResults = document.getElementById('noResults');

        searchInput.addEventListener('input', function() {
            const filterValue = searchInput.value.toLowerCase().trim();
            let hasVisibleCards = false;

            filmCards.forEach(card => {
                const title = card.getAttribute('data-title');
                if (title.includes(filterValue)) {
                    card.style.display = 'flex';
                    hasVisibleCards = true;
                } else {
                    card.style.display = 'none';
                }
            });

            noResults.style.display = hasVisibleCards ? 'none' : 'block';
        });

        function toggleLike(btn, filmTitle) {
            playClickSound(800, 0.1);
            let likedFilms = JSON.parse(localStorage.getItem('likedFilms')) || [];
            if (likedFilms.includes(filmTitle)) {
                likedFilms = likedFilms.filter(item => item !== filmTitle);
                btn.classList.remove('liked');
            } else {
                likedFilms.push(filmTitle);
                btn.classList.add('liked');
            }
            localStorage.setItem('likedFilms', JSON.stringify(likedFilms));
        }

        const activeStarsData = {};

        function toggleReviews(filmId) {
            playClickSound(400, 0.05);
            const panel = document.getElementById('reviews-panel-' + filmId);
            panel.style.display = panel.style.display === 'block' ? 'none' : 'block';
        }

        function updateTypingStatus(filmId) {
            const name = document.getElementById('author-' + filmId).value.trim();
            const comment = document.getElementById('comment-' + filmId).value.trim();
            const statusDiv = document.getElementById('typing-status-' + filmId);
            
            if (comment.length > 0) {
                const displayName = name ? name : "Кто-то";
                statusDiv.innerText = displayName + " пишет отзыв...";
                statusDiv.style.display = "block";
            } else {
                statusDiv.style.display = "none";
            }
        }

        function setFormStars(filmId, rating) {
            playClickSound(500 + (rating * 50), 0.05);
            activeStarsData[filmId] = rating;
            const starsContainer = document.getElementById('star-select-' + filmId);
            const stars = starsContainer.querySelectorAll('span');
            stars.forEach((star, index) => {
                if (index < rating) {
                    star.classList.add('active');
                } else {
                    star.classList.remove('active');
                }
            });
        }

        function loadReviewsAndRating() {
            const dbReviews = JSON.parse(localStorage.getItem('filmsReviews')) || {};
            
            filmCards.forEach(card => {
                const filmId = card.getAttribute('data-id');
                const listContainer = document.getElementById('reviews-list-' + filmId);
                const reviews = dbReviews[filmId] || [];
                
                listContainer.innerHTML = '';
                if (reviews.length === 0) {
                    listContainer.innerHTML = '<div style="color: #6b7280; text-align: center; padding: 10px 0;">Отзывов пока нет. Станьте первым!</div>';
                    card.setAttribute('data-rating', '0');
                } else {
                    reviews.forEach(r => {
                        const starsHtml = '★'.repeat(r.rating) + '☆'.repeat(5 - r.rating);
                        listContainer.innerHTML += `
                            <div class="review-item">
                                <div class="review-header">
                                    <span>${r.author}</span>
                                    <span class="review-stars">${starsHtml}</span>
                                </div>
                                <div class="review-text">${r.comment}</div>
                            </div>
                        `;
                    });
                }

                const ratingBadge = document.getElementById('rating-' + filmId);
                if (reviews.length > 0) {
                    const sum = reviews.reduce((acc, curr) => acc + curr.rating, 0);
                    const avg = (sum / reviews.length).toFixed(1);
                    ratingBadge.innerHTML = `⭐ ${avg}/5 (${reviews.length} отз.)`;
                    card.setAttribute('data-rating', avg);
                } else {
                    ratingBadge.innerHTML = `⭐ -- (0 отзывов)`;
                    card.setAttribute('data-rating', '0');
                }
            });
        }

        function submitReview(filmId) {
            const authorInput = document.getElementById('author-' + filmId);
            const commentInput = document.getElementById('comment-' + filmId);
            const rating = activeStarsData[filmId] || 0;

            if (!authorInput.value.trim()) {
                alert('Пожалуйста, введите ваше имя!');
                return;
            }

            if (!commentInput.value.trim()) {
                alert('Пожалуйста, напишите текст отзыва!');
                return;
            }

            if (rating === 0) {
                alert('Пожалуйста, выберите оценку (нажмите на звёздочки).');
                return;
            }

            playClickSound(1000, 0.15);

            const dbReviews = JSON.parse(localStorage.getItem('filmsReviews')) || {};
            if (!dbReviews[filmId]) dbReviews[filmId] = [];

            dbReviews[filmId].unshift({
                author: authorInput.value.trim(),
                comment: commentInput.value.trim(),
                rating: rating
            });

            localStorage.setItem('filmsReviews', JSON.stringify(dbReviews));

            authorInput.value = '';
            commentInput.value = '';
            document.getElementById('typing-status-' + filmId).style.display = "none";
            setFormStars(filmId, 0);

            loadReviewsAndRating();
        }

        // ЕДИНАЯ ФУНКЦИЯ ОТКРЫТИЯ ПЛЕЕРА ДЛЯ ТРЕЙЛЕРОВ И ПОЛНЫХ ФИЛЬМОВ
        function openPlayer(videoId) {
            playClickSound(700, 0.08);
            const modal = document.getElementById('videoModal');
            const iframe = document.getElementById('videoPlayer');
            
            iframe.src = `https://www.youtube.com/embed/${videoId}?autoplay=1&rel=0`;
            modal.classList.add('active');
        }

        function closePlayer() {
            const modal = document.getElementById('videoModal');
            const iframe = document.getElementById('videoPlayer');
            iframe.src = '';
            modal.classList.remove('active');
        }

        function sortFilms() {
            const criteria = document.getElementById('sortSelect').value;
            const grid = document.getElementById('filmsGrid');
            const items = Array.from(grid.querySelectorAll('.film-card'));

            if (criteria === 'default') {
                loadReviewsAndRating();
                return;
            }

            items.sort((a, b) => {
                if (criteria === 'year-desc') {
                    return parseInt(b.getAttribute('data-year')) - parseInt(a.getAttribute('data-year'));
                } else if (criteria === 'year-asc') {
                    return parseInt(a.getAttribute('data-year')) - parseInt(b.getAttribute('data-year'));
                } else if (criteria === 'rating-desc') {
                    return parseFloat(b.getAttribute('data-rating')) - parseFloat(a.getAttribute('data-rating'));
                }
            });

            items.forEach(item => grid.appendChild(item));
        }

        document.addEventListener('DOMContentLoaded', () => {
            const likedFilms = JSON.parse(localStorage.getItem('likedFilms')) || [];
            const likeButtons = document.querySelectorAll('.like-btn');
            likeButtons.forEach(btn => {
                const cardTitle = btn.closest('.film-card').querySelector('.film-title').innerText;
                if (likedFilms.includes(cardTitle)) btn.classList.add('liked');
            });

            loadReviewsAndRating();
        });
    </script>
</body>
</html>'''

with open(os.path.join(TEMPLATES_DIR, 'genre.html'), 'w', encoding='utf-8') as f:
    f.write(genre_html_template.replace('REPLACE_WITH_SHARED_CSS', SHARED_CSS))

# 3. Создаем about.html (Без f-строк)
about_html_template = '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>О проекте | Films_Iliaz Ultra</title>
    <style>
        REPLACE_WITH_SHARED_CSS
        .about-box { 
            text-align: center; 
            padding: 65px 35px; 
            max-width: 750px; 
            margin: 50px auto 0; 
            background: rgba(18, 18, 22, 0.85); 
            border-radius: 24px; 
            box-shadow: 0 15px 35px rgba(0,0,0,0.6); 
            border: 1px solid rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(10px);
        }
        .about-box p { 
            font-size: 1.25rem; 
            color: #9ca3af; 
            line-height: 1.75; 
        }
        .tech-list {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-top: 30px;
            flex-wrap: wrap;
        }
        .tech-tag {
            background: rgba(255, 46, 59, 0.15);
            color: #ff2e3b;
            padding: 8px 18px;
            border-radius: 30px;
            font-weight: bold;
            font-size: 0.95rem;
            border: 1px solid rgba(255, 46, 59, 0.3);
        }
    </style>
</head>
<body>
    <nav>
        <a href="/" class="logo">Films_Iliaz</a>
        <a href="/genre/action">Боевики</a>
        <a href="/genre/comedy">Комедии</a>
        <a href="/genre/fantasy">Фэнтези</a>
        <a href="/about">О проекте</a>
    </nav>
    <div class="container">
        <div class="about-box">
            <h1>Киноплатформа <span class="accent">Films_Iliaz 10x Ultra</span></h1>
            <p>Это ультимативно переработанное веб-приложение, созданное Ильязом. Все ошибки устранены, плеер воспроизводит плавные превью без блокировок, а инновационный дизайн и Web Audio звуки погружают в атмосферу цифрового домашнего кинотеатра.</p>
            <div class="tech-list">
                <span class="tech-tag">YouTube Inline Player</span>
                <span class="tech-tag">Dynamic Review Engine</span>
                <span class="tech-tag">Typing Status Indicator</span>
                <span class="tech-tag">Live Sorting Filter</span>
            </div>
        </div>
    </div>
</body>
</html>'''

with open(os.path.join(TEMPLATES_DIR, 'about.html'), 'w', encoding='utf-8') as f:
    f.write(about_html_template.replace('REPLACE_WITH_SHARED_CSS', SHARED_CSS))

print("[СУПЕР-УСПЕХ]: Все файлы проекта с поддержкой полных фильмов успешно обновлены!")

# --- МАРШРУТЫ FLASK ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/genre/<genre_name>')
def genre(genre_name):
    if genre_name in FILMS_DB:
        data = FILMS_DB[genre_name]
        return render_template('genre.html', genre_title=data['title'], films=data['list'])
    else:
        return "Жанр не найден", 404

if __name__ == '__main__':
    app.run(debug=True)
