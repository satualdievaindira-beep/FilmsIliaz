import os

from flask import Flask, render_template

app = Flask(__name__)

# --- БАЗА ДАННЫХ ФИЛЬМОВ (ОБНОВЛЕННАЯ С EMBED-КОДАМИ ДЛЯ ПЛЕЕРА) ---
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
                'trailer_id': 'hEJnMQG96dQ'
            },
            {
                'id': 'john_wick',
                'title': 'Джон Уик',
                'year': '2014',
                'desc': 'История бывшего наемного убийцы, который возвращается в криминальный мир, чтобы жестоко отомстить за самое дорогое.',
                'image': 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?q=80&w=500&auto=format&fit=crop',
                'trailer_id': '2AUmvWm5epQ'
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
                'trailer_id': 'jEDaVIXyiGg'
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
                'trailer_id': 'VyHV0BRfm1s'
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

# Продвинутые стили CSS с плавной анимацией и размытием (записываем отдельно, без f-строк)
SHARED_CSS = """
body { 
    font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; 
    background-color: #08080a; 
    color: #ffffff; 
    margin: 0; 
    padding: 0; 
    overflow-x: hidden;
}
nav { 
    background-color: rgba(4, 4, 6, 0.85); 
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    padding: 20px 0; 
    box-shadow: 0 4px 30px rgba(0,0,0,0.8); 
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
    transition: all 0.3s ease; 
}
nav a:hover { 
    color: #ff2e3b; 
    text-shadow: 0 0 15px rgba(255, 46, 59, 0.5);
}
.logo { 
    color: #ff2e3b !important; 
    font-size: 1.6rem; 
    text-transform: uppercase; 
    letter-spacing: 3px; 
    font-weight: 900;
}
.container { 
    padding: 40px 20px; 
    max-width: 1200px; 
    margin: 0 auto; 
}
.accent { 
    color: #ff2e3b; 
    text-shadow: 0 0 15px rgba(255, 46, 59, 0.3);
}
h1 { 
    font-size: 3rem; 
    font-weight: 800;
    margin-bottom: 20px; 
}
"""

# 1. Создаем index.html (запись обычным текстом без f-строк во избежание багов)
index_html_content = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Главная | Films_Iliaz</title>
    <meta name="monetag" content="8a4bbe65dee28e911fefcd608f183f21">
    <style>
""" + SHARED_CSS + """
        .hero { 
            padding: 160px 20px; 
            text-align: center; 
            background: radial-gradient(circle at center, #1b1216 0%, #08080a 100%); 
            min-height: 55vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        .hero p { 
            font-size: 1.35rem; 
            color: #9ca3af; 
            max-width: 650px; 
            line-height: 1.7;
            margin-top: 15px;
        }
        .browse-btn {
            margin-top: 35px;
            background-color: #ff2e3b;
            color: white;
            padding: 15px 32px;
            text-decoration: none;
            font-weight: bold;
            border-radius: 50px;
            font-size: 1.15rem;
            box-shadow: 0 5px 20px rgba(255, 46, 59, 0.45);
            transition: 0.3s;
        }
        .browse-btn:hover {
            background-color: #e01b28;
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(255, 46, 59, 0.7);
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
        <h1>Добро пожаловать в <span class="accent">Films_Iliaz Premium</span></h1>
        <p>Интерактивная медиа-лаборатория Ильяза. Читайте и оставляйте настоящие отзывы, смотрите трейлеры прямо в плеере и сохраняйте любимое кино!</p>
        <a href="/genre/action" class="browse-btn">Войти в кинотеатр</a>
    </div>
</body>
</html>"""

with open(os.path.join(TEMPLATES_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(index_html_content)

# 2. Создаем genre.html (Без использования f-строк, чтобы {} в JS не вызывали ошибок компиляции Python)
genre_html_content = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ genre_title }} | Films_Iliaz</title>
    <style>
""" + SHARED_CSS + """
        h1 { text-align: center; margin-bottom: 10px; }

        /* Поиск */
        .search-container {
            display: flex;
            justify-content: center;
            margin: 30px 0 10px;
        }
        .search-input {
            width: 100%;
            max-width: 500px;
            padding: 14px 24px;
            border-radius: 30px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            background-color: #121215;
            color: white;
            font-size: 1rem;
            outline: none;
            transition: all 0.3s ease;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }
        .search-input:focus {
            border-color: #ff2e3b;
            box-shadow: 0 0 15px rgba(255, 46, 59, 0.3);
            background-color: #18181f;
        }

        /* Сетка фильмов */
        .films-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); 
            gap: 40px; 
            margin-top: 40px; 
        }
        .film-card { 
            background-color: #111114; 
            border-radius: 20px; 
            overflow: hidden; 
            box-shadow: 0 10px 25px rgba(0,0,0,0.5); 
            transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1); 
            display: flex; 
            flex-direction: column; 
            position: relative;
            border: 1px solid rgba(255, 255, 255, 0.03);
        }
        .film-card:hover { 
            transform: translateY(-6px); 
            box-shadow: 0 15px 35px rgba(255, 46, 59, 0.2); 
            border-color: rgba(255, 46, 59, 0.15);
        }
        .film-poster-wrapper {
            position: relative;
            width: 100%;
            height: 420px;
            overflow: hidden;
        }
        .film-poster { 
            width: 100%; 
            height: 100%; 
            object-fit: cover; 
            transition: transform 0.5s ease;
        }
        .film-card:hover .film-poster {
            transform: scale(1.04);
        }

        /* Лайки */
        .like-btn {
            position: absolute;
            top: 15px;
            right: 15px;
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(5px);
            border: none;
            width: 44px;
            height: 44px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s ease;
            color: #ffffff;
            font-size: 1.3rem;
            z-index: 10;
        }
        .like-btn:hover { transform: scale(1.15); }
        .like-btn.liked { color: #ff2e3b; text-shadow: 0 0 8px rgba(255, 46, 59, 0.6); }

        .film-info { 
            padding: 25px; 
            display: flex; 
            flex-direction: column; 
            flex-grow: 1; 
        }
        .film-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 8px;
        }
        .film-title { 
            margin: 0; 
            font-size: 1.5rem; 
            font-weight: 700;
            line-height: 1.2; 
        }
        .film-meta {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 15px;
        }
        .film-year { 
            font-size: 0.85rem; 
            color: #ff2e3b; 
            font-weight: 800; 
            background: rgba(255, 46, 59, 0.1);
            padding: 3px 10px;
            border-radius: 20px;
        }
        .film-rating {
            font-size: 0.9rem;
            color: #ffb800;
            font-weight: bold;
        }
        .film-desc { 
            font-size: 0.95rem; 
            color: #9ca3af; 
            line-height: 1.6; 
            margin-bottom: 22px; 
            flex-grow: 1; 
        }

        .button-group {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-bottom: 15px;
        }
        .watch-btn { 
            background-color: #ff2e3b; 
            color: white; 
            text-align: center; 
            text-decoration: none; 
            padding: 12px; 
            border-radius: 8px; 
            font-weight: 700; 
            transition: all 0.2s ease; 
            cursor: pointer;
            border: none;
        }
        .watch-btn:hover { background-color: #e01b28; }

        .reviews-toggle-btn {
            background-color: #24242b;
            color: #e5e7eb;
            border: none;
            padding: 12px;
            border-radius: 8px;
            font-weight: 700;
            cursor: pointer;
            transition: 0.2s;
        }
        .reviews-toggle-btn:hover { background-color: #2f2f38; }

        /* СЕКЦИЯ ОТЗЫВОВ */
        .reviews-panel {
            display: none; 
            border-top: 1px solid rgba(255,255,255,0.06);
            padding-top: 20px;
            margin-top: 15px;
        }
        .reviews-list {
            max-height: 200px;
            overflow-y: auto;
            margin-bottom: 15px;
            padding-right: 5px;
        }
        .reviews-list::-webkit-scrollbar {
            width: 4px;
        }
        .reviews-list::-webkit-scrollbar-thumb {
            background: #2f2f38;
            border-radius: 4px;
        }
        .review-item {
            background: rgba(255, 255, 255, 0.02);
            padding: 10px 14px;
            border-radius: 10px;
            margin-bottom: 10px;
            font-size: 0.88rem;
        }
        .review-header {
            display: flex;
            justify-content: space-between;
            color: #9ca3af;
            margin-bottom: 4px;
            font-weight: 600;
        }
        .review-stars { color: #ffb800; }
        .review-text { color: #d1d5db; line-height: 1.4; }

        /* Форма написания отзыва */
        .review-form {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .review-form input, .review-form textarea {
            background: #18181f;
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 6px;
            padding: 8px 12px;
            color: white;
            font-size: 0.85rem;
            outline: none;
        }
        .review-form input:focus, .review-form textarea:focus {
            border-color: #ff2e3b;
        }
        .review-form-row {
            display: flex;
            gap: 10px;
            align-items: center;
        }
        .star-rating-select {
            display: flex;
            gap: 3px;
            cursor: pointer;
            font-size: 1.2rem;
            color: #374151;
        }
        .star-rating-select span:hover,
        .star-rating-select span.active {
            color: #ffb800;
        }
        .submit-review-btn {
            background-color: rgba(255, 46, 59, 0.15);
            color: #ff2e3b;
            border: 1px solid rgba(255, 46, 59, 0.3);
            padding: 8px;
            border-radius: 6px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.2s;
        }
        .submit-review-btn:hover {
            background-color: #ff2e3b;
            color: white;
        }

        /* КИНОТЕАТР: Встроенный модальный плеер */
        .modal {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background-color: rgba(0,0,0,0.92);
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
            width: 85%;
            max-width: 850px;
            aspect-ratio: 16/9;
            background: black;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 0 50px rgba(255, 46, 59, 0.3);
        }
        .modal-content iframe {
            width: 100%; height: 100%; border: none;
        }
        .close-modal {
            position: absolute;
            top: -45px; right: 0;
            color: white;
            font-size: 2rem;
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

        <div class="search-container">
            <input type="text" id="searchInput" class="search-input" placeholder="🔍 Начните вводить название фильма для поиска...">
        </div>

        <div class="films-grid" id="filmsGrid">
            {% for film in films %}
            <div class="film-card" data-id="{{ film.id }}" data-title="{{ film.title | lower }}">
                <div class="film-poster-wrapper">
                    <button class="like-btn" onclick="toggleLike(this, '{{ film.title }}')">❤</button>
                    <img src="{{ film.image }}" alt="{{ film.title }}" class="film-poster">
                </div>
                <div class="film-info">
                    <div class="film-header">
                        <h3 class="film-title">{{ film.title }}</h3>
                    </div>
                    <div class="film-meta">
                        <span class="film-year">{{ film.year }} год</span>
                        <span class="film-rating" id="rating-{{ film.id }}">⭐ -- (0 отзывов)</span>
                    </div>
                    <p class="film-desc">{{ film.desc }}</p>

                    <div class="button-group">
                        <button class="watch-btn" onclick="openTrailer('{{ film.trailer_id }}')">▶ Трейлер</button>
                        <button class="reviews-toggle-btn" onclick="toggleReviews('{{ film.id }}')">💬 Отзывы</button>
                    </div>

                    <!-- Интерактивная вкладка отзывов -->
                    <div class="reviews-panel" id="reviews-panel-{{ film.id }}">
                        <div class="reviews-list" id="reviews-list-{{ film.id }}"></div>

                        <!-- Форма написания нового отзыва -->
                        <div class="review-form">
                            <div class="review-form-row">
                                <input type="text" id="author-{{ film.id }}" placeholder="Ваше имя" required style="flex-grow: 1;">
                                <div class="star-rating-select" id="star-select-{{ film.id }}">
                                    <span onclick="setFormStars('{{ film.id }}', 1)">★</span>
                                    <span onclick="setFormStars('{{ film.id }}', 2)">★</span>
                                    <span onclick="setFormStars('{{ film.id }}', 3)">★</span>
                                    <span onclick="setFormStars('{{ film.id }}', 4)">★</span>
                                    <span onclick="setFormStars('{{ film.id }}', 5)">★</span>
                                </div>
                            </div>
                            <textarea id="comment-{{ film.id }}" placeholder="Напишите свое мнение о фильме..." rows="2" required></textarea>
                            <button class="submit-review-btn" onclick="submitReview('{{ film.id }}')">Отправить отзыв</button>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
            <div class="no-results" id="noResults">Ничего не найдено. Попробуйте изменить поисковый запрос!</div>
        </div>
    </div>

    <!-- Встроенный модальный видеоплеер -->
    <div class="modal" id="videoModal" onclick="closeTrailer()">
        <div class="modal-content" onclick="event.stopPropagation()">
            <span class="close-modal" onclick="closeTrailer()">&times;</span>
            <iframe id="trailerFrame" allow="autoplay; encrypted-media" allowfullscreen></iframe>
        </div>
    </div>

    <script>
        // --- 1. ЖИВОЙ ПОИСК ---
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

        // --- 2. ИЗБРАННОЕ (ЛАЙКИ) ---
        function toggleLike(btn, filmTitle) {
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

        // --- 3. СИСТЕМА ИНТЕРАКТИВНЫХ ОТЗЫВОВ И ЗВЕЗД ---
        const activeStarsData = {}; 

        function toggleReviews(filmId) {
            const panel = document.getElementById(`reviews-panel-${filmId}`);
            panel.style.display = panel.style.display === 'block' ? 'none' : 'block';
        }

        function setFormStars(filmId, rating) {
            activeStarsData[filmId] = rating;
            const starsContainer = document.getElementById(`star-select-${filmId}`);
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
                const listContainer = document.getElementById(`reviews-list-${filmId}`);
                const reviews = dbReviews[filmId] || [];

                listContainer.innerHTML = '';
                if (reviews.length === 0) {
                    listContainer.innerHTML = '<div style="color: #6b7280; text-align: center; padding: 10px 0;">Отзывов пока нет. Будьте первыми!</div>';
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

                const ratingBadge = document.getElementById(`rating-${filmId}`);
                if (reviews.length > 0) {
                    const sum = reviews.reduce((acc, curr) => acc + curr.rating, 0);
                    const avg = (sum / reviews.length).toFixed(1);
                    ratingBadge.innerHTML = `⭐ ${avg}/5 (${reviews.length} отз.)`;
                } else {
                    ratingBadge.innerHTML = `⭐ -- (0 отзывов)`;
                }
            });
        }

        function submitReview(filmId) {
            const authorInput = document.getElementById(`author-${filmId}`);
            const commentInput = document.getElementById(`comment-${filmId}`);
            const rating = activeStarsData[filmId] || 0;

            if (!authorInput.value.trim() || !commentInput.value.trim()) {
                alert('Пожалуйста, заполните имя и напишите текст отзыва.');
                return;
            }
            if (rating === 0) {
                alert('Пожалуйста, выберите оценку фильма звездками.');
                return;
            }

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
            setFormStars(filmId, 0);

            loadReviewsAndRating();
        }

        // --- 4. ОРИГИНАЛЬНЫЙ МОДАЛЬНЫЙ ТРЕЙЛЕР ПЛЕЕР ---
        function openTrailer(youtubeId) {
            const modal = document.getElementById('videoModal');
            const iframe = document.getElementById('trailerFrame');
            iframe.src = `https://www.youtube.com/embed/${youtubeId}?autoplay=1`;
            modal.classList.add('active');
        }

        function closeTrailer() {
            const modal = document.getElementById('videoModal');
            const iframe = document.getElementById('trailerFrame');
            iframe.src = '';
            modal.classList.remove('active');
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
</html>"""

with open(os.path.join(TEMPLATES_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(index_html_content)

# 2. Создаем genre.html (Без использования f-строк, чтобы {} в JS не вызывали ошибок компиляции Python)
genre_html_content = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ genre_title }} | Films_Iliaz</title>
    <style>
""" + SHARED_CSS + """
        h1 { text-align: center; margin-bottom: 10px; }

        /* Поиск */
        .search-container {
            display: flex;
            justify-content: center;
            margin: 30px 0 10px;
        }
        .search-input {
            width: 100%;
            max-width: 500px;
            padding: 14px 24px;
            border-radius: 30px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            background-color: #121215;
            color: white;
            font-size: 1rem;
            outline: none;
            transition: all 0.3s ease;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }
        .search-input:focus {
            border-color: #ff2e3b;
            box-shadow: 0 0 15px rgba(255, 46, 59, 0.3);
            background-color: #18181f;
        }

        /* Сетка фильмов */
        .films-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); 
            gap: 40px; 
            margin-top: 40px; 
        }
        .film-card { 
            background-color: #111114; 
            border-radius: 20px; 
            overflow: hidden; 
            box-shadow: 0 10px 25px rgba(0,0,0,0.5); 
            transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1); 
            display: flex; 
            flex-direction: column; 
            position: relative;
            border: 1px solid rgba(255, 255, 255, 0.03);
        }
        .film-card:hover { 
            transform: translateY(-6px); 
            box-shadow: 0 15px 35px rgba(255, 46, 59, 0.2); 
            border-color: rgba(255, 46, 59, 0.15);
        }
        .film-poster-wrapper {
            position: relative;
            width: 100%;
            height: 420px;
            overflow: hidden;
        }
        .film-poster { 
            width: 100%; 
            height: 100%; 
            object-fit: cover; 
            transition: transform 0.5s ease;
        }
        .film-card:hover .film-poster {
            transform: scale(1.04);
        }

        /* Лайки */
        .like-btn {
            position: absolute;
            top: 15px;
            right: 15px;
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(5px);
            border: none;
            width: 44px;
            height: 44px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s ease;
            color: #ffffff;
            font-size: 1.3rem;
            z-index: 10;
        }
        .like-btn:hover { transform: scale(1.15); }
        .like-btn.liked { color: #ff2e3b; text-shadow: 0 0 8px rgba(255, 46, 59, 0.6); }

        .film-info { 
            padding: 25px; 
            display: flex; 
            flex-direction: column; 
            flex-grow: 1; 
        }
        .film-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 8px;
        }
        .film-title { 
            margin: 0; 
            font-size: 1.5rem; 
            font-weight: 700;
            line-height: 1.2; 
        }
        .film-meta {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 15px;
        }
        .film-year { 
            font-size: 0.85rem; 
            color: #ff2e3b; 
            font-weight: 800; 
            background: rgba(255, 46, 59, 0.1);
            padding: 3px 10px;
            border-radius: 20px;
        }
        .film-rating {
            font-size: 0.9rem;
            color: #ffb800;
            font-weight: bold;
        }
        .film-desc { 
            font-size: 0.95rem; 
            color: #9ca3af; 
            line-height: 1.6; 
            margin-bottom: 22px; 
            flex-grow: 1; 
        }

        .button-group {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-bottom: 15px;
        }
        .watch-btn { 
            background-color: #ff2e3b; 
            color: white; 
            text-align: center; 
            text-decoration: none; 
            padding: 12px; 
            border-radius: 8px; 
            font-weight: 700; 
            transition: all 0.2s ease; 
            cursor: pointer;
            border: none;
        }
        .watch-btn:hover { background-color: #e01b28; }

        .reviews-toggle-btn {
            background-color: #24242b;
            color: #e5e7eb;
            border: none;
            padding: 12px;
            border-radius: 8px;
            font-weight: 700;
            cursor: pointer;
            transition: 0.2s;
        }
        .reviews-toggle-btn:hover { background-color: #2f2f38; }

        /* СЕКЦИЯ ОТЗЫВОВ */
        .reviews-panel {
            display: none; 
            border-top: 1px solid rgba(255,255,255,0.06);
            padding-top: 20px;
            margin-top: 15px;
        }
        .reviews-list {
            max-height: 200px;
            overflow-y: auto;
            margin-bottom: 15px;
            padding-right: 5px;
        }
        .reviews-list::-webkit-scrollbar {
            width: 4px;
        }
        .reviews-list::-webkit-scrollbar-thumb {
            background: #2f2f38;
            border-radius: 4px;
        }
        .review-item {
            background: rgba(255, 255, 255, 0.02);
            padding: 10px 14px;
            border-radius: 10px;
            margin-bottom: 10px;
            font-size: 0.88rem;
        }
        .review-header {
            display: flex;
            justify-content: space-between;
            color: #9ca3af;
            margin-bottom: 4px;
            font-weight: 600;
        }
        .review-stars { color: #ffb800; }
        .review-text { color: #d1d5db; line-height: 1.4; }

        /* Форма написания отзыва */
        .review-form {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .review-form input, .review-form textarea {
            background: #18181f;
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 6px;
            padding: 8px 12px;
            color: white;
            font-size: 0.85rem;
            outline: none;
        }
        .review-form input:focus, .review-form textarea:focus {
            border-color: #ff2e3b;
        }
        .review-form-row {
            display: flex;
            gap: 10px;
            align-items: center;
        }
        .star-rating-select {
            display: flex;
            gap: 3px;
            cursor: pointer;
            font-size: 1.2rem;
            color: #374151;
        }
        .star-rating-select span:hover,
        .star-rating-select span.active {
            color: #ffb800;
        }
        .submit-review-btn {
            background-color: rgba(255, 46, 59, 0.15);
            color: #ff2e3b;
            border: 1px solid rgba(255, 46, 59, 0.3);
            padding: 8px;
            border-radius: 6px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.2s;
        }
        .submit-review-btn:hover {
            background-color: #ff2e3b;
            color: white;
        }

        /* КИНОТЕАТР: Встроенный модальный плеер */
        .modal {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background-color: rgba(0,0,0,0.92);
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
            width: 85%;
            max-width: 850px;
            aspect-ratio: 16/9;
            background: black;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 0 50px rgba(255, 46, 59, 0.3);
        }
        .modal-content iframe {
            width: 100%; height: 100%; border: none;
        }
        .close-modal {
            position: absolute;
            top: -45px; right: 0;
            color: white;
            font-size: 2rem;
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

        <div class="search-container">
            <input type="text" id="searchInput" class="search-input" placeholder="🔍 Начните вводить название фильма для поиска...">
        </div>

        <div class="films-grid" id="filmsGrid">
            {% for film in films %}
            <div class="film-card" data-id="{{ film.id }}" data-title="{{ film.title | lower }}">
                <div class="film-poster-wrapper">
                    <button class="like-btn" onclick="toggleLike(this, '{{ film.title }}')">❤</button>
                    <img src="{{ film.image }}" alt="{{ film.title }}" class="film-poster">
                </div>
                <div class="film-info">
                    <div class="film-header">
                        <h3 class="film-title">{{ film.title }}</h3>
                    </div>
                    <div class="film-meta">
                        <span class="film-year">{{ film.year }} год</span>
                        <span class="film-rating" id="rating-{{ film.id }}">⭐ -- (0 отзывов)</span>
                    </div>
                    <p class="film-desc">{{ film.desc }}</p>

                    <div class="button-group">
                        <button class="watch-btn" onclick="openTrailer('{{ film.trailer_id }}')">▶ Трейлер</button>
                        <button class="reviews-toggle-btn" onclick="toggleReviews('{{ film.id }}')">💬 Отзывы</button>
                    </div>

                    <!-- Интерактивная вкладка отзывов -->
                    <div class="reviews-panel" id="reviews-panel-{{ film.id }}">
                        <div class="reviews-list" id="reviews-list-{{ film.id }}"></div>

                        <!-- Форма написания нового отзыва -->
                        <div class="review-form">
                            <div class="review-form-row">
                                <input type="text" id="author-{{ film.id }}" placeholder="Ваше имя" required style="flex-grow: 1;">
                                <div class="star-rating-select" id="star-select-{{ film.id }}">
                                    <span onclick="setFormStars('{{ film.id }}', 1)">★</span>
                                    <span onclick="setFormStars('{{ film.id }}', 2)">★</span>
                                    <span onclick="setFormStars('{{ film.id }}', 3)">★</span>
                                    <span onclick="setFormStars('{{ film.id }}', 4)">★</span>
                                    <span onclick="setFormStars('{{ film.id }}', 5)">★</span>
                                </div>
                            </div>
                            <textarea id="comment-{{ film.id }}" placeholder="Напишите свое мнение о фильме..." rows="2" required></textarea>
                            <button class="submit-review-btn" onclick="submitReview('{{ film.id }}')">Отправить отзыв</button>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
            <div class="no-results" id="noResults">Ничего не найдено. Попробуйте изменить поисковый запрос!</div>
        </div>
    </div>

    <!-- Встроенный модальный видеоплеер -->
    <div class="modal" id="videoModal" onclick="closeTrailer()">
        <div class="modal-content" onclick="event.stopPropagation()">
            <span class="close-modal" onclick="closeTrailer()">&times;</span>
            <iframe id="trailerFrame" allow="autoplay; encrypted-media" allowfullscreen></iframe>
        </div>
    </div>

    <script>
        // --- 1. ЖИВОЙ ПОИСК ---
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

        // --- 2. ИЗБРАННОЕ (ЛАЙКИ) ---
        function toggleLike(btn, filmTitle) {
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

        // --- 3. СИСТЕМА ИНТЕРАКТИВНЫХ ОТЗЫВОВ И ЗВЕЗД ---
        const activeStarsData = {}; 

        function toggleReviews(filmId) {
            const panel = document.getElementById(`reviews-panel-${filmId}`);
            panel.style.display = panel.style.display === 'block' ? 'none' : 'block';
        }

        function setFormStars(filmId, rating) {
            activeStarsData[filmId] = rating;
            const starsContainer = document.getElementById(`star-select-${filmId}`);
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
                const listContainer = document.getElementById(`reviews-list-${filmId}`);
                const reviews = dbReviews[filmId] || [];

                listContainer.innerHTML = '';
                if (reviews.length === 0) {
                    listContainer.innerHTML = '<div style="color: #6b7280; text-align: center; padding: 10px 0;">Отзывов пока нет. Будьте первыми!</div>';
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

                const ratingBadge = document.getElementById(`rating-${filmId}`);
                if (reviews.length > 0) {
                    const sum = reviews.reduce((acc, curr) => acc + curr.rating, 0);
                    const avg = (sum / reviews.length).toFixed(1);
                    ratingBadge.innerHTML = `⭐ ${avg}/5 (${reviews.length} отз.)`;
                } else {
                    ratingBadge.innerHTML = `⭐ -- (0 отзывов)`;
                }
            });
        }

        function submitReview(filmId) {
            const authorInput = document.getElementById(`author-${filmId}`);
            const commentInput = document.getElementById(`comment-${filmId}`);
            const rating = activeStarsData[filmId] || 0;

            if (!authorInput.value.trim() || !commentInput.value.trim()) {
                alert('Пожалуйста, заполните имя и напишите текст отзыва.');
                return;
            }
            if (rating === 0) {
                alert('Пожалуйста, выберите оценку фильма звездками.');
                return;
            }

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
            setFormStars(filmId, 0);

            loadReviewsAndRating();
        }

        // --- 4. ОРИГИНАЛЬНЫЙ МОДАЛЬНЫЙ ТРЕЙЛЕР ПЛЕЕР ---
        function openTrailer(youtubeId) {
            const modal = document.getElementById('videoModal');
            const iframe = document.getElementById('trailerFrame');
            iframe.src = `https://www.youtube.com/embed/${youtubeId}?autoplay=1`;
            modal.classList.add('active');
        }

        function closeTrailer() {
            const modal = document.getElementById('videoModal');
            const iframe = document.getElementById('trailerFrame');
            iframe.src = '';
            modal.classList.remove('active');
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
</html>"""

with open(os.path.join(TEMPLATES_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(index_html_content)

# 3. Создаем about.html (Обычным безопасным текстом)
about_html_content = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>О проекте | Films_Iliaz</title>
    <style>
""" + SHARED_CSS + """
        .about-box { 
            text-align: center; 
            padding: 65px 35px; 
            max-width: 750px; 
            margin: 50px auto 0; 
            background: #111114; 
            border-radius: 24px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.6); 
            border: 1px solid rgba(255, 255, 255, 0.05);
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
            background: rgba(255, 46, 59, 0.1);
            color: #ff2e3b;
            padding: 8px 18px;
            border-radius: 30px;
            font-weight: bold;
            font-size: 0.95rem;
            border: 1px solid rgba(255, 46, 59, 0.2);
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
            <h1>Киноплатформа <span class="accent">Films_Iliaz Premium</span></h1>
            <p>Это технологичный, полностью интерактивный развлекательный веб-сервис. Проект построен на Flask (Python) для гибкой маршрутизации и чистого HTML5/CSS3/JS с применением асинхронного сохранения состояния на клиенте (Local Storage).</p>
            <div class="tech-list">
                <span class="tech-tag">Python & Flask</span>
                <span class="tech-tag">Modal Theatre Player</span>
                <span class="tech-tag">Dynamic Star Rating System</span>
                <span class="tech-tag">Client State Engines</span>
            </div>
        </div>
    </div>
</body>
</html>"""

with open(os.path.join(TEMPLATES_DIR, 'about.html'), 'w', encoding='utf-8') as f:
    f.write(about_html_content)

print("[УСПЕХ]: Ошибка f-строки исправлена! Новые HTML-шаблоны без проблем записаны.")


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
