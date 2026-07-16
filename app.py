import os
from flask import Flask, render_template

app = Flask(__name__)

# --- РАСШИРЕННАЯ БАЗА ДАННЫХ ФИЛЬМОВ С БАННЕРАМИ С КИНОГО ---
FILMS_DB = {
    'action': {
        'title': 'Боевики & Экшен',
        'list': [
            {
                'id': 'mad_max',
                'title': 'Безумный Макс: Дорога ярости',
                'year': '2015',
                'desc': 'В постапокалиптическом мире Макс объединяется с воительницей Фуриосой, чтобы сбежать от тирана Несмертного Джо.',
                'image': 'https://kinogo.my/uploads/posts/2019-08/1565436329-300931421-bezumnyy-maks-doroga-yarosti.jpg',
                'youtube_id': 'hEJnMQG9ld8',
                'kinogo_url': 'https://kinogo.my/films/1230-bezumnyy-maks-doroga-yarosti-2026.html'
            },
            {
                'id': 'john_wick',
                'title': 'Джон Уик',
                'year': '2014',
                'desc': 'История бывшего наемного убийцы, который возвращается в криминальный мир, чтобы жестоко отомстить за смерть своего щенка.',
                'image': 'https://kinogo.my/uploads/posts/2019-07/1562092879-1783019840-dzhon-uik.jpg',
                'youtube_id': '2AUmvWm5ZDQ',
                'kinogo_url': 'https://kinogo.my/films/1065-dzhon-uik-hd-mdb6-io6.html'
            },
            {
                'id': 'dark_knight',
                'title': 'Темный рыцарь',
                'year': '2008',
                'desc': 'Бэтмен поднимает ставки в войне с криминалом. С помощью лейтенанта Джима Гордона и прокурора Харви Дента он намерен очистить Готэм.',
                'image': 'https://kinogo.my/uploads/posts/2019-07/1563273397-628424754-temnyy-rycar.jpg',
                'youtube_id': 'EXeTwQWrcwY',
                'kinogo_url': 'https://kinogo.my/films/2070-temnyy-rycar-2008.html'
            },
            {
                'id': 'gladiator',
                'title': 'Гладиатор',
                'year': '2000',
                'desc': 'В великой Римской империи не было военачальника, равного генералу Максимусу. Но предательство превращает его в раба-гладиатора.',
                'image': 'https://kinogo.my/uploads/posts/2019-07/1563275753-462319047-gladiator.jpg',
                'youtube_id': 'P5ieIbInFpg',
                'kinogo_url': 'https://kinogo.my/films/2088-gladiator-2000.html'
            },
            {
                'id': 'matrix',
                'title': 'Матрица',
                'year': '1999',
                'desc': 'Жизнь Томаса Андерсона разделена на две части: днем он обычный программист, а ночью — хакер Нео. Но однажды все меняется.',
                'image': 'https://kinogo.my/uploads/posts/2019-07/1563273413-1785507519-matrica.jpg',
                'youtube_id': 'm8e-FF8MsqU',
                'kinogo_url': 'https://kinogo.my/films/2045-matrica-1999.html'
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
                'image': 'https://kinogo.my/uploads/posts/2019-12/1577714595-1650178410-odin-doma.jpg',
                'youtube_id': 'f7fepI8A60A',
                'kinogo_url': 'https://kinogo.my/films/2617-odin-doma-2025.html'
            },
            {
                'id': 'hangover',
                'title': 'Мальчишник в Вегасе',
                'year': '2009',
                'desc': 'Четверо друзей устраивают безбашенный мальчишник в Лас-Вегасе. Утром они просыпаются и не могут вспомнить абсолютно ничего.',
                'image': 'https://kinogo.my/uploads/posts/2019-08/1565181745-1815344315-malchishnik-v-vegase.jpg',
                'youtube_id': 'tcdUjAybleA',
                'kinogo_url': 'https://kinogo.my/films/2350-malchishnik-v-vegase-2009.html'
            },
            {
                'id': 'mask',
                'title': 'Маска',
                'year': '1994',
                'desc': 'Скромный банковский служащий находит волшебную маску, которая превращает его в неуязвимое и безумное мультяшное существо.',
                'image': 'https://kinogo.my/uploads/posts/2020-02/1582200236-47671842-maska.jpg',
                'youtube_id': 'hOqWS2uJeQU',
                'kinogo_url': 'https://kinogo.my/films/3120-maska-1994.html'
            },
            {
                'id': 'intouchables',
                'title': '1+1 (Неприкасаемые)',
                'year': '2011',
                'desc': 'Пострадавший в результате несчастного случая аристократ Филипп нанимает в качестве помощника человека, который менее всего подходит для этой работы.',
                'image': 'https://kinogo.my/uploads/posts/2019-08/1566411516-2001155986-11.jpg',
                'youtube_id': '0aR8t76MmEE',
                'kinogo_url': 'https://kinogo.my/films/1410-1-plyus-1-2011.html'
            },
            {
                'id': 'free_guy',
                'title': 'Главный герой',
                'year': '2021',
                'desc': 'У сотрудника крупного банка всё идёт по плану, пока он не выясняет, что окружающий его мир — это часть видеоигры.',
                'image': 'https://kinogo.my/uploads/posts/2021-09/1632731885-308696803-glavnyy-geroy.jpg',
                'youtube_id': 'X2m-0sM-s1E',
                'kinogo_url': 'https://kinogo.my/films/4450-glavnyy-geroy-2021.html'
            }
        ]
    },
    'fantasy': {
        'title': 'Фэнтези & Фантастика',
        'list': [
            {
                'id': 'harry_potter',
                'title': 'Гарри Поттер и Философский камень',
                'year': '2001',
                'desc': 'Мальчик-сирота узнает, что он волшебник, и отправляется учиться в знаменитую школу магии Хогвартс.',
                'image': 'https://kinogo.my/uploads/posts/2019-12/1575459380-459815049-garri-potter-i-filosofskiy-kamen.jpg',
                'youtube_id': 'mNgwNXKafMc',
                'kinogo_url': 'https://kinogo.my/films/2540-garri-potter-1.html'
            },
            {
                'id': 'interstellar',
                'title': 'Интерстеллар',
                'year': '2014',
                'desc': 'Когда засуха приводит человечество к продовольственному кризису, коллектив исследователей отправляется сквозь червоточину.',
                'image': 'https://kinogo.my/uploads/posts/2019-07/1563271118-1856372554-interstellar.jpg',
                'youtube_id': 'zSWdZVtXT7E',
                'kinogo_url': 'https://kinogo.my/films/1120-interstellar-2014.html'
            },
            {
                'id': 'avatar',
                'title': 'Аватар',
                'year': '2009',
                'desc': 'Бывший морской пехотинец Джейк Салли парализован. Он получает задание совершить путешествие вглубь планеты Пандора.',
                'image': 'https://kinogo.my/uploads/posts/2020-01/1579717758-2041261314-avatar.jpg',
                'youtube_id': '5PSNL1qE6VY',
                'kinogo_url': 'https://kinogo.my/films/3005-avatar-2009.html'
            },
            {
                'id': 'lord_of_rings',
                'title': 'Властелин колец: Братство Кольца',
                'year': '2001',
                'desc': 'В Средиземье скромный хоббит Фродо Бэггинс получает задание уничтожить всемогущее Кольцо Всевластья.',
                'image': 'https://kinogo.my/uploads/posts/2019-08/1566838383-1498774780-vlastelin-kolec-bratstvo-kolca.jpg',
                'youtube_id': 'V75dMMIW2B4',
                'kinogo_url': 'https://kinogo.my/films/1990-vlastelin-kolec-1.html'
            },
            {
                'id': 'inception',
                'title': 'Начало',
                'year': '2010',
                'desc': 'Кобб — талантливый вор, лучший в опасном искусстве извлечения: он крадет ценные секреты из глубин подсознания во время сна.',
                'image': 'https://kinogo.my/uploads/posts/2019-07/1563273449-346513511-nachalo.jpg',
                'youtube_id': 'CPTIgILtna8',
                'kinogo_url': 'https://kinogo.my/films/2099-nachalo-2010.html'
            }
        ]
    },
    'horror': {
        'title': 'Ужасы & Триллеры',
        'list': [
            {
                'id': 'conjuring',
                'title': 'Заклятие',
                'year': '2013',
                'desc': 'Детективы, расследующие паранормальные явления, сталкиваются с самым жутким делом в своей практике в доме уединенной фермы.',
                'image': 'https://kinogo.my/uploads/posts/2019-08/1565431613-225345758-zaklyatie.jpg',
                'youtube_id': 'k10ETZ41q5o',
                'kinogo_url': 'https://kinogo.my/films/1520-zaklyatie-2013.html'
            },
            {
                'id': 'it_movie',
                'title': 'Оно',
                'year': '2017',
                'desc': 'Когда в городке Дерри начинают пропадать дети, группа подростков сталкивается со своими величайшими страхами в лице клоуна Пеннивайза.',
                'image': 'https://kinogo.my/uploads/posts/2019-11/1572718104-585327891-ono.jpg',
                'youtube_id': 'FnCdOQsX5kc',
                'kinogo_url': 'https://kinogo.my/films/3820-ono-2017.html'
            },
            {
                'id': 'shining',
                'title': 'Сияние',
                'year': '1980',
                'desc': 'Джек Торренс приезжает в элегантный уединенный отель, чтобы поработать смотрителем во время мертвого сезона вместе с семьей.',
                'image': 'https://kinogo.my/uploads/posts/2021-03/1614777598-1324747716-siyanie.jpg',
                'youtube_id': 'S014oGZiSdI',
                'kinogo_url': 'https://kinogo.my/films/5510-siyanie-1980.html'
            },
            {
                'id': 'a_quiet_place',
                'title': 'Тихое место',
                'year': '2018',
                'desc': 'История одной семьи, которая вынуждена жить в полной темноте и тишине, чтобы не привлечь ужасных монстров, реагирующих на любой звук.',
                'image': 'https://kinogo.my/uploads/posts/2020-01/1577903264-1065934522-tihoe-mesto.jpg',
                'youtube_id': 'YPY7J-flzE8',
                'kinogo_url': 'https://kinogo.my/films/4112-tihoe-mesto-2018.html'
            },
            {
                'id': 'astral',
                'title': 'Астрал',
                'year': '2010',
                'desc': 'Джош и Рене переезжают в новый дом, но не успевают распаковать вещи, как начинаются странные события: предметы двигаются, слышны звуки.',
                'image': 'https://kinogo.my/uploads/posts/2019-12/1575459397-1582885938-astral.jpg',
                'youtube_id': 'E1YbOMDI5mk',
                'kinogo_url': 'https://kinogo.my/films/2810-astral-2010.html'
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

# 1. index.html
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
        <a href="/genre/horror">Ужасы</a>
        <a href="/about">О проекте</a>
    </nav>
    <div class="hero">
        <h1>Films_Iliaz <span class="accent">Ultra 10x</span></h1>
        <p>Добро пожаловать на абсолютно новую, полностью переработанную развлекательную платформу. Высокая скорость работы, живые отзывы, встроенный плеер и чистый дизайн.</p>
        <a href="/genre/action" class="browse-btn">Войти в медиатеку</a>
    </div>
</body>
</html>'''

with open(os.path.join(TEMPLATES_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(index_html_template.replace('REPLACE_WITH_SHARED_CSS', SHARED_CSS))

# 2. genre.html
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
        <a href="/genre/horror">Ужасы</a>
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
                    
                    <a href="{{ film.kinogo_url }}" target="_blank" style="text-decoration: none; grid-column: span 2;">
                        <button class="play-movie-btn" style="width: 100%;">🎬 Смотреть фильм</button>
                    </a>

                    <div class="button-group">
                        <button class="watch-btn" onclick="openYoutubePlayer('{{ film.youtube_id }}')">▶ Трейлер</button>
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
                                    <span>\${r.author}</span>
                                    <span class="review-stars">\${starsHtml}</span>
                                </div>
                                <div class="review-text">\${r.comment}</div>
                            </div>
                        `;
                    });
                }

                const ratingBadge = document.getElementById('rating-' + filmId);
                if (reviews.length > 0) {
                    const sum = reviews.reduce((acc, curr) => acc + curr.rating, 0);
                    const avg = (sum / reviews.length).toFixed(1);
                    ratingBadge.innerHTML = `⭐ \${avg}/5 (\${reviews.length} отз.)`;
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

        function openYoutubePlayer(videoId) {
            playClickSound(700, 0.08);
            const modal = document.getElementById('videoModal');
            const iframe = document.getElementById('videoPlayer');
            iframe.src = `https://www.youtube.com/embed/\${videoId}?autoplay=1&rel=0`;
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
                const card = btn.closest('.film-card');
                const title = card.querySelector('.film-title').innerText;
                if (likedFilms.includes(title)) {
                    btn.classList.add('liked');
                }
            });

            loadReviewsAndRating();
        });
    </script>
</body>
</html>'''

with open(os.path.join(TEMPLATES_DIR, 'genre.html'), 'w', encoding='utf-8') as f:
    f.write(genre_html_template.replace('REPLACE_WITH_SHARED_CSS', SHARED_CSS))

# 3. about.html
about_html_template = '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>О проекте | Films_Iliaz</title>
    <style>
        REPLACE_WITH_SHARED_CSS
        .about-box {
            background: rgba(18, 18, 22, 0.85); 
            border-radius: 24px; 
            padding: 40px;
            max-width: 800px;
            margin: 50px auto;
            border: 1px solid rgba(255, 255, 255, 0.04);
            box-shadow: 0 15px 35px rgba(0,0,0,0.6); 
            text-align: center;
        }
        h1 { margin-top: 0; }
        p { color: #9ca3af; line-height: 1.8; font-size: 1.1rem; }
    </style>
</head>
<body>
    <nav>
        <a href="/" class="logo">Films_Iliaz</a>
        <a href="/genre/action">Боевики</a>
        <a href="/genre/comedy">Комедии</a>
        <a href="/genre/fantasy">Фэнтези</a>
        <a href="/genre/horror">Ужасы</a>
        <a href="/about">О проекте</a>
    </nav>
    <div class="container">
        <div class="about-box">
            <h1>О проекте <span class="accent">Films_Iliaz</span></h1>
            <p>Это приватная кинематографическая платформа нового поколения. Мы объединили стильный футуристический интерфейс с высокой скоростью работы и возможностью смотреть любимые фильмы во встроенном проигрывателе.</p>
            <p>Наш проект активно развивается, впереди еще много крутых фич!</p>
        </div>
    </div>
</body>
</html>'''

with open(os.path.join(TEMPLATES_DIR, 'about.html'), 'w', encoding='utf-8') as f:
    f.write(about_html_template.replace('REPLACE_WITH_SHARED_CSS', SHARED_CSS))


# --- РОУТЫ (МАРШРУТЫ) FLASK ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/genre/<genre_name>')
def genre(genre_name):
    genre_data = FILMS_DB.get(genre_name)
    if not genre_data:
        return "Жанр не найден", 404
    
    return render_template(
        'genre.html', 
        genre_title=genre_data['title'], 
        films=genre_data['list']
    )

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
