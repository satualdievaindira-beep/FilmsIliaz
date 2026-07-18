import os
import urllib.request
import urllib.error
from flask import Flask, render_template_string, request, redirect, url_for, Response, session, flash

app = Flask(__name__)

# Полная конфигурация приложения
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'supersecretkey_films_iliaz_2026_secure')
app.config['DEBUG'] = True

# --- ПОЛНАЯ БАЗА ДАННЫХ ФИЛЬМОВ С ВАШИМИ ОБНОВЛЕННЫМИ ССЫЛКАМИ НА ПОСТЕРЫ ---
MOVIES = [
    # === ФАНТАСТИКА И ПРИКЛЮЧЕНИЯ ===
    {
        "id": 1,
        "title": "Аватар",
        "genre": "Фантастика",
        "poster": "https://kinogo.my/uploads/posts/2017-04/1493391756-1159271017-avatar.jpg",
        "year": 2009,
        "director": "Джеймс Кэмерон",
        "rating": 7.9,
        "duration": "162 мин.",
        "description": "Бывший морской пехотинец Джейк Салли, прикованный к инвалидному креслу, получает задание отправиться на далекую планету Пандора. Там корпорации добывают редкий минерал, имеющий огромное значение для Земли. Чтобы дышать на Пандоре, создана программа Аватар — гибрид человека и местной расы На'ви. Погружаясь в этот новый мир, Джейк влюбляется в культуру коренных жителей и встает перед выбором: чью сторону занять в грядущей битве за будущее планеты.",
        "cast": "Сэм Уортингтон, Зои Салдана, Сигурни Уивер, Стивен Лэнг"
    },
    {
        "id": 2,
        "title": "Властелин колец: Братство Кольца",
        "genre": "Фантастика",
        "poster": "https://kinogo.my/uploads/posts/2019-07/1563720942-490328414-vlastelin-kolec-bratstvo-kolca.jpg",
        "year": 2001,
        "director": "Питер Джексон",
        "rating": 8.6,
        "duration": "178 мин.",
        "description": "В спокойной деревушке Хоббитон молодой хоббит Фродо Бэггинс получает в наследство от своего дяди Бильбо магическое Кольцо Всевластья. Хранитель этого кольца обладает невероятной силой, но и Саурон, Темный Властелин Средиземья, жаждет вернуть его. Великий маг Гэндальф отправляет Фродо в опасное путешествие к Роковой горе в сердце Мордора — единственному месту, где Кольцо может быть уничтожено. Вместе с ним выдвигается Братство, состоящее из людей, эльфа, гнома и хоббитов.",
        "cast": "Элайджа Вуд, Иэн Маккеллен, Вигго Мортенсен, Шон Бин, Орландо Блум"
    },
    {
        "id": 3,
        "title": "Гарри Поттер и Философский камень",
        "genre": "Фантастика",
        "poster": "https://kinogo.my/uploads/posts/2019-07/1563015062-1572996915-garri-potter-i-filosofskiy-kamen.jpg",
        "year": 2001,
        "director": "Крис Коламбус",
        "rating": 8.2,
        "duration": "152 мин.",
        "description": "Гарри Поттер — обычный сирота, живущий под лестницей в доме своих жестоких родственников Дурслей. В свой 11-й день рождения мальчик узнает, что его родители были могущественными волшебниками, а сам он зачислен в Школу чародейства и волшебства Хогвартс. Там Гарри обретает настоящих друзей, Рона и Гермиону, осваивает полеты на метле и магические заклинания, а также сталкивается лицом к лицу с темной тайной, связанной со смертью его родителей.",
        "cast": "Дэниэл Рэдклифф, Руперт Гринт, Эмма Уотсон, Ричард Харрис"
    },
    {
        "id": 4,
        "title": "Интерстеллар",
        "genre": "Фантастика",
        "poster": "https://kinogo.my/uploads/posts/2017-04/1491114790-991695033-interstellar.jpg",
        "year": 2014,
        "director": "Кристофер Нолан",
        "rating": 8.6,
        "duration": "169 мин.",
        "description": "В недалеком будущем человечество сталкивается с глобальным продовольственным кризисом и песчаными бурями, которые грозят уничтожить всё живое на Земле. Группа ученых и исследователей использует недавно обнаруженный пространственно-временной тоннель (червоточину), чтобы обойти ограничения космических полетов и найти планету, пригодную для переселения людей. Бывший пилот НАСА Купер вынужден оставить свою семью, чтобы возглавить экспедицию, цена которой — выживание человеческого рода.",
        "cast": "Мэттью Макконахи, Энн Хэтэуэй, Джессика Честейн, Майкл Кейн"
    },
    {
        "id": 5,
        "title": "Матрица",
        "genre": "Фантастика",
        "poster": "https://kinogo.my/uploads/posts/2020-01/1578316075-753251593-matrica.jpg",
        "year": 1999,
        "director": "Лана Вачовски, Лилли Вачовски",
        "rating": 8.5,
        "duration": "136 мин.",
        "description": "Жизнь Томаса Андерсона разделена на две части: днем он обычный программист в крупной компании, а ночью — хакер по имени Нео. Однажды с ним связывается таинственный Морфеус, который открывает ему ужасающую правду. Мир, который Нео считал реальностью, — это симуляция, созданная машинами, чтобы контролировать и использовать энергию человеческих тел. Теперь Нео должен пробудиться в реальном мире и возглавить восстание против искусственного интеллекта в качестве Избранного.",
        "cast": "Киану Ривз, Лоренс Фишбёрн, Кэрри-Энн Мосс, Хьюго Уивинг"
    },
    {
        "id": 6,
        "title": "Начало",
        "genre": "Фантастика",
        "poster": "https://kinogo.my/uploads/posts/2017-04/1491114986-2049908774-nachalo.jpg",
        "year": 2010,
        "director": "Кристофер Нолан",
        "rating": 8.7,
        "duration": "148 мин.",
        "description": "Доминик Кобб — непревзойденный специалист по извлечению ценных секретов из глубин подсознания во время сна, когда человеческий разум наиболее уязвим. Его уникальные способности сделали его ценным игроком в мире промышленного шпионажа, но превратили в беглеца. Чтобы вернуть свою прежнюю жизнь и получить шанс вернуться к детям, Коббу предстоит совершить невозможное — не украсть мысль, а наоборот, запустить идею в мозг наследника огромной бизнес-империи.",
        "cast": "Леонардо Ди Каприо, Джозеф Гордон-Левитт, Эллиот Пейдж, Том Харди, Киллиан Мёрфи"
    },

    # === БОЕВИКИ И ДРАМЫ ===
    {
        "id": 7,
        "title": "Темный рыцарь",
        "genre": "Боевики",
        "poster": "https://kinogo.my/uploads/posts/2020-03/1585250490_the-dark-knight-2008.jpg",
        "year": 2008,
        "director": "Кристофер Нолан",
        "rating": 8.5,
        "duration": "152 мин.",
        "description": "Бэтмен поднимает ставки в бесконечной войне с организованной преступностью Готэма. Объединив усилия с честным окружным прокурором Харви Дентом и лейтенантом Джимом Гордоном, супергерой добивается ощутимых результатов на улицах города. Но вскоре хрупкий порядок рушится под натиском хаоса, когда появляется безумный преступный гений, известный как Джокер, цель которого — не деньги, а полное уничтожение моральных принципов жителей Готэма.",
        "cast": "Кристиан Бейл, Хит Леджер, Аарон Экхарт, Мэгги Джилленхол, Гэри Олдмен"
    },
    {
        "id": 8,
        "title": "Гладиатор",
        "genre": "Боевики",
        "poster": "https://kinogo.my/uploads/posts/2019-11/1574343110_gladiator-2000.jpg",
        "year": 2000,
        "director": "Ридли Скотт",
        "rating": 8.6,
        "duration": "155 мин.",
        "description": "Генерал Максимус — величайший военачальник Римской империи, преданный своему правителю Марку Аврелию. Однако коварный сын императора, Коммод, убивает отца, захватывает власть и отдает приказ казнить Максимуса и всю его семью. Чудом избежав гибели, раненый генерал попадает в рабство и становится гладиатором. Его мастерство в бою и железная воля быстро делают его любимцем публики, и теперь его главная цель — добраться до Рима и отомстить тирану на арене Колизея.",
        "cast": "Рассел Кроу, Хоакин Феникс, Конни Нильсен, Оливер Рид"
    },

    # === КОМЕДИИ ===
    {
        "id": 9,
        "title": "Мальчишник в Вегасе",
        "genre": "Комедии",
        "poster": "https://kinogo.my/uploads/posts/2017-04/1491158875-2116979171-malchishnik-v-vegase.jpg",
        "year": 2009,
        "director": "Тодд Филлипс",
        "rating": 7.9,
        "duration": "100 мин.",
        "description": "Трое закадычных друзей отправляются в Лас-Вегас на грандиозный мальчишник своего приятеля Дага за пару дней до его свадьбы. Проснувшись на следующее утро в роскошном номере отеля, они обнаруживают в ванной живого тигра, в шкафу — младенца, а у одного из них выбит зуб. Но самое страшное — сам Даг бесследно исчез. Друзьям, страдающим от тяжелого похмелья, предстоит восстановить цепочку безумных ночных событий, чтобы найти жениха и успеть доставить его на церемонию.",
        "cast": "Брэдли Купер, Эд Хелмс, Зак Галифианакис, Джастин Барта"
    },
    {
        "id": 10,
        "title": "Маска",
        "genre": "Комедии",
        "poster": "https://kinogo.my/uploads/posts/2023-11/1699995824-1618804087-maska.jpg",
        "year": 1994,
        "director": "Чак Рассел",
        "rating": 8.0,
        "duration": "101 мин.",
        "description": "Скромный, застенчивый и неудачливый работник банка Стэнли Ипкисс случайно находит старинную деревянную маску. Стоит ему надеть её, как он превращается в эксцентричное, практически неуязвимое мультяшное существо с ярко-зеленым лицом. Маска освобождает все скрытые желания и суперсилы Стэнли: он грабит банк, очаровывает роковую певицу Тину Карлайл и встает на пути у опасной банды гангстеров, терроризирующей город.",
        "cast": "Джим Керри, Кэмерон Диас, Питер Ригерт, Питер Грин"
    },
    {
        "id": 11,
        "title": "Главный герой",
        "genre": "Комедии",
        "poster": "https://kinogo.my/uploads/posts/2021-09/1632400100_free-guy-2021.jpg",
        "year": 2021,
        "director": "Шон Леви",
        "rating": 7.2,
        "duration": "115 мин.",
        "description": "У сотрудника крупного банка по имени Парень вся жизнь отточена до мелочей: кофе по утрам, веселая болтовня, ограбление банка бандитами по расписанию. Но однажды Парень узнает, что его уютный город Свободный Город — это жестокая компьютерная онлайн-игра, а сам он — всего лишь второстепенный неигровой персонаж (NPC). Парень решает изменить свой программный код, привлечь внимание прекрасной девушки-игрока и стать настоящим героем, чтобы спасти свой цифровой мир от закрытия.",
        "cast": "Райан Рейнольдс, Джоди Комер, Лил Rel Ховери, Тайка Вайтити"
    },

    # === УЖАСЫ ===
    {
        "id": 12,
        "title": "Заклятие",
        "genre": "Ужасы",
        "poster": "https://kinogo.my/uploads/posts/2020-03/1583751212-1153530858-zaklyatie.jpg",
        "year": 2013,
        "director": "Джеймс Ван",
        "rating": 7.4,
        "duration": "112 мин.",
        "description": "Основанная на реальных материалах из практики исследователей паранормальных явлений Эда и Лоррейн Уоррен. Семья Перрон переезжает в уединенный фермерский дом и сразу начинает сталкиваться со странными звуками, хлопающими дверьми и жуткими видениями. Поняв, что дом одержим древней демонической сущностью, супруги вызывают на помощь Уорренов. Специалистам предстоит вступить в самое страшное и опасное противостояние в своей жизни, чтобы изгнать зло.",
        "cast": "Вера Фармига, Патрик Уилсон, Рон Ливингстон, Лили Тейлор"
    },
    {
        "id": 13,
        "title": "Оно",
        "genre": "Ужасы",
        "poster": "https://kinogo.my/uploads/posts/2019-10/1570100719-126843975-ono.jpg",
        "year": 2017,
        "director": "Энди Мускетти",
        "rating": 7.3,
        "duration": "135 мин.",
        "description": "В тихом провинциальном городке Дерри в штате Мэн начинают бесследно исчезать дети. Несколько затравленных школьников из «Клуба неудачников» объединяются, когда каждый из них сталкивается со своим глубинным страхом. Вскоре они понимают, что виной всему — древнее зло, просыпающееся каждые 27 лет, которое принимает форму жуткого танцующего клоуна Пеннивайза, заманивающего детей яркими красными шарами.",
        "cast": "Джейден Мартелл, Билл Скарсгард, Финн Вулфхард, София Лиллис"
    },
    {
        "id": 14,
        "title": "Сияние",
        "genre": "Ужасы",
        "poster": "https://kinogo.my/uploads/posts/2024-01/1704798751-1904935975-siyanie.jpg",
        "year": 1980,
        "director": "Стэнли Кубрик",
        "rating": 8.4,
        "duration": "144 мин.",
        "description": "Писатель Джек Торренс устраивается зимним смотрителем в шикарный отель «Оверлук», отрезанный от внешнего мира снежными завалами. Джек планирует провести это время в тишине вместе со своей женой Венди и маленьким сыном Дэнни, работая над новой книгой. Однако отель хранит в своих стенах мрачные тайны прошлого. Дэнни, обладающий телепатическим даром ('сиянием'), начинает видеть призраков, а рассудок Джека под влиянием зловещего места начинает стремительно разрушаться.",
        "cast": "Джек Николсон, Шелли Дювалл, Дэнни Ллойд, Скэтмэн Крозерс"
    },
    {
        "id": 15,
        "title": "Тихое место",
        "genre": "Ужасы",
        "poster": "https://kinogo.my/uploads/posts/2019-10/1570971117-511240173-tihoe-mesto.jpg",
        "year": 2018,
        "director": "Джон Красински",
        "rating": 7.1,
        "duration": "90 мин.",
        "description": "Земля подверглась нападению смертоносных инопланетных существ. Эти монстры абсолютно слепы, но обладают невероятно острым слухом. Семья Эбботт с детьми выживает на изолированной ферме, где каждый аспект их быта подчинен одному правилу — не издавать ни единого звука. Они общаются на языке жестов, ходят босиком по песчаным тропинкам и заменяют посуду на листья. Но сохранять абсолютную тишину становится невыносимо трудно, особенно когда в семье ожидается прибавление.",
        "cast": "Эмили Блант, Джон Красински, Миллисент Симмондс, Ноа Джуп"
    },
    {
        "id": 16,
        "title": "Астрал",
        "genre": "Ужасы",
        "poster": "https://kinogo.my/uploads/posts/2020-02/1582196735-58106119-astral.jpg",
        "year": 2010,
        "director": "Джеймс Ван",
        "rating": 6.8,
        "duration": "103 мин.",
        "description": "Молодые супруги Джош и Рене переезжают со своими детьми в новый дом. Не успевают они разобрать вещи, как вокруг начинают происходить пугающие мистические вещи: предметы двигаются сами, слышатся шаги, а их маленький сын Далтон падает с лестницы и впадает в необъяснимую кому. Врачи разводят руками. Приглашенные специалисты по паранормальным явлениям выясняют, что мальчик связан с потусторонним миром духов — Астралом, и демоны пытаются захватить его тело.",
        "cast": "Патрик Уилсон, Роуз Бирн, Тай Симпкинс, Лин Шэй"
    }
]

# Инициализация отзывов в памяти
REVIEWS = {movie["id"]: [] for movie in MOVIES}

# --- МАСШТАБНЫЙ HTML ШАБЛОН ГЛАВНОЙ СТРАНИЦЫ (INDEX_HTML) ---
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
            --primary-hover: #e03d4c;
            --text-main: #ffffff;
            --text-muted: #a0a0b0;
            --accent: #28a745;
        }
        body {
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-dark);
            color: var(--text-main);
            margin: 0;
            padding: 0;
            min-height: 100vh;
        }
        header {
            background: linear-gradient(135deg, #161623 0%, #0b0b11 100%);
            padding: 30px 20px;
            text-align: center;
            border-bottom: 4px solid var(--primary);
            box-shadow: 0 4px 20px rgba(0,0,0,0.6);
        }
        header h1 {
            margin: 0;
            font-size: 3rem;
            color: var(--primary);
            text-transform: uppercase;
            letter-spacing: 3px;
            text-shadow: 0 2px 10px rgba(255, 74, 90, 0.4);
        }
        header p {
            margin: 10px 0 0 0;
            color: var(--text-muted);
            font-size: 1.1rem;
        }
        .container {
            max-width: 1300px;
            margin: 40px auto;
            padding: 0 25px;
        }
        .genre-section {
            margin-bottom: 60px;
        }
        .genre-header {
            display: flex;
            align-items: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #252535;
            padding-bottom: 10px;
        }
        .genre-title {
            font-size: 2rem;
            font-weight: 700;
            color: #f1f1f6;
            margin: 0;
            position: relative;
        }
        .genre-title::after {
            content: '';
            position: absolute;
            bottom: -12px;
            left: 0;
            width: 80px;
            height: 4px;
            background-color: var(--primary);
            border-radius: 2px;
        }
        .movies-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
            gap: 35px;
        }
        .movie-card {
            background-color: var(--card-bg);
            border-radius: 14px;
            overflow: hidden;
            box-shadow: 0 6px 18px rgba(0,0,0,0.4);
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            text-decoration: none;
            color: inherit;
            display: flex;
            flex-direction: column;
            border: 1px solid #222232;
        }
        .movie-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 12px 28px rgba(255, 74, 90, 0.25);
            border-color: #383852;
        }
        .poster-wrapper {
            width: 100%;
            height: 350px;
            background-color: #12121a;
            overflow: hidden;
            position: relative;
        }
        .poster-wrapper img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.5s ease;
        }
        .movie-card:hover .poster-wrapper img {
            transform: scale(1.06);
        }
        .rating-badge {
            position: absolute;
            top: 15px;
            right: 15px;
            background-color: rgba(0, 0, 0, 0.85);
            color: #ffc107;
            padding: 5px 10px;
            border-radius: 6px;
            font-weight: bold;
            font-size: 0.95rem;
            border: 1px solid rgba(255, 193, 7, 0.4);
            backdrop-filter: blur(5px);
        }
        .movie-content {
            padding: 20px;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .movie-title {
            font-size: 1.3rem;
            font-weight: 700;
            margin: 0 0 8px 0;
            color: #ffffff;
            line-height: 1.4;
        }
        .movie-meta {
            font-size: 0.9rem;
            color: var(--text-muted);
            margin-bottom: 15px;
        }
        .action-btn {
            background-color: var(--primary);
            color: white;
            text-align: center;
            padding: 10px 0;
            border-radius: 8px;
            font-size: 0.95rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            transition: background 0.2s;
        }
        .movie-card:hover .action-btn {
            background-color: var(--primary-hover);
        }
        footer {
            text-align: center;
            padding: 40px 20px;
            color: var(--text-muted);
            border-top: 1px solid #1a1a24;
            margin-top: 40px;
            background-color: #0b0b0e;
        }
    </style>
</head>
<body>

    <header>
        <h1>Films_Iliaz</h1>
        <p>Индивидуальная онлайн-галерея твоих любимых фильмов</p>
    </header>

    <div class="container">
        {% for genre in ["Фантастика", "Боевики", "Комедии", "Ужасы"] %}
        <div class="genre-section">
            <div class="genre-header">
                <h2 class="genre-title">{{ genre }}</h2>
            </div>
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
                        <div class="action-btn">Смотреть детали</div>
                    </div>
                </a>
                {% endfor %}
            </div>
        </div>
        {% endfor %}
    </div>

    <footer>
        &copy; 2026 Films_Iliaz. Все права защищены. Разработано на Flask.
    </footer>

</body>
</html>
"""

# --- МАСШТАБНЫЙ HTML ШАБЛОН СТРАНИЦЫ ДЕТАЛЕЙ (MOVIE_HTML) ---
MOVIE_HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ movie.title }} — База Данных Films_Iliaz</title>
    <style>
        :root {
            --bg-dark: #0f0f12;
            --card-bg: #1a1a24;
            --primary: #ff4a5a;
            --primary-hover: #e03d4c;
            --text-main: #ffffff;
            --text-muted: #a0a0b0;
        }
        body {
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-dark);
            color: var(--text-main);
            margin: 0;
            padding: 0;
        }
        header {
            background-color: #161623;
            padding: 20px 40px;
            border-bottom: 3px solid var(--primary);
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        }
        header h1 {
            margin: 0;
            font-size: 2rem;
            color: var(--primary);
            text-transform: uppercase;
        }
        .back-btn {
            color: white;
            text-decoration: none;
            font-weight: 600;
            background-color: #2b2b3d;
            padding: 10px 20px;
            border-radius: 8px;
            transition: all 0.3s;
            border: 1px solid #3a3a52;
        }
        .back-btn:hover {
            background-color: var(--primary);
            border-color: var(--primary);
        }
        .container {
            max-width: 1100px;
            margin: 50px auto;
            padding: 0 25px;
        }
        .movie-main-box {
            display: flex;
            gap: 50px;
            background-color: var(--card-bg);
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.5);
            margin-bottom: 50px;
            border: 1px solid #222232;
        }
        .poster-box {
            flex-shrink: 0;
            width: 320px;
            height: 470px;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 8px 25px rgba(0,0,0,0.7);
            background-color: #121218;
        }
        .poster-box img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .info-box {
            flex-grow: 1;
        }
        .info-box h2 {
            margin: 0 0 15px 0;
            font-size: 2.8rem;
            color: #ffffff;
            line-height: 1.2;
        }
        .tags-row {
            display: flex;
            gap: 15px;
            margin-bottom: 25px;
            flex-wrap: wrap;
        }
        .badge {
            background-color: #2c2c3e;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
            color: #e0e0f0;
        }
        .badge.genre {
            background-color: var(--primary);
            color: white;
        }
        .badge.rating {
            background-color: #ffc107;
            color: #111;
        }
        .meta-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 30px;
        }
        .meta-table td {
            padding: 10px 0;
            border-bottom: 1px solid #28283a;
            font-size: 1.05rem;
        }
        .meta-table td.label {
            color: var(--text-muted);
            width: 140px;
            font-weight: 500;
        }
        .plot-title {
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 12px;
            color: #f1f1f6;
        }
        .plot-text {
            font-size: 1.1rem;
            line-height: 1.7;
            color: #d1d1d6;
            margin: 0;
        }

        /* Полный Блок Отзывов */
        .reviews-wrapper {
            background-color: var(--card-bg);
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.5);
            border: 1px solid #222232;
        }
        .reviews-wrapper h3 {
            margin: 0 0 25px 0;
            font-size: 1.8rem;
            color: var(--primary);
            border-bottom: 2px solid #28283a;
            padding-bottom: 12px;
        }
        .review-item {
            background-color: #212130;
            padding: 20px 25px;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 5px solid var(--primary);
        }
        .review-user {
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 8px;
            font-size: 1.1rem;
        }
        .review-body {
            line-height: 1.6;
            font-size: 1.05rem;
            color: #e2e2e8;
        }
        .empty-msg {
            color: var(--text-muted);
            font-style: italic;
            font-size: 1.05rem;
            margin-bottom: 30px;
        }
        
        /* Форма Нового Отзыва */
        .form-block h4 {
            font-size: 1.4rem;
            margin: 35px 0 20px 0;
            color: #ffffff;
        }
        .input-group {
            margin-bottom: 20px;
        }
        .input-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            font-size: 0.95rem;
            color: var(--text-muted);
        }
        .input-field {
            width: 100%;
            padding: 12px 15px;
            border-radius: 8px;
            border: 1px solid #3a3a52;
            background-color: #121218;
            color: white;
            font-size: 1rem;
            box-sizing: border-box;
            transition: border-color 0.2s;
        }
        .input-field:focus {
            outline: none;
            border-color: var(--primary);
        }
        textarea.input-field {
            resize: vertical;
            min-height: 120px;
        }
        .btn-submit {
            background-color: var(--primary);
            color: white;
            border: none;
            padding: 12px 28px;
            border-radius: 8px;
            font-size: 1.05rem;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s;
        }
        .btn-submit:hover {
            background-color: var(--primary-hover);
        }
    </style>
</head>
<body>

    <header>
        <h1>Films_Iliaz</h1>
        <a href="{{ url_for('index') }}" class="back-btn">← Вернуться на главную</a>
    </header>

    <div class="container">
        <!-- Блок описания фильма -->
        <div class="movie-main-box">
            <div class="poster-box">
                <img src="{{ url_for('proxy_image', url=movie.poster) }}" alt="{{ movie.title }}">
            </div>
            <div class="info-box">
                <h2>{{ movie.title }}</h2>
                
                <div class="tags-row">
                    <span class="badge genre">{{ movie.genre }}</span>
                    <span class="badge rating">★ {{ movie.rating }} / 10</span>
                    <span class="badge">{{ movie.year }} год</span>
                </div>

                <table class="meta-table">
                    <tr>
                        <td class="label">Режиссер</td>
                        <td>{{ movie.director }}</td>
                    </tr>
                    <tr>
                        <td class="label">Длительность</td>
                        <td>{{ movie.duration }}</td>
                    </tr>
                    <tr>
                        <td class="label">В главных ролях</td>
                        <td>{{ movie.cast }}</td>
                    </tr>
                </table>

                <div class="plot-title">Сюжет:</div>
                <p class="plot-text">{{ movie.description }}</p>
            </div>
        </div>

        <!-- Раздел пользовательских отзывов -->
        <div class="reviews-wrapper">
            <h3>Отзывы пользователей сайта</h3>
            
            {% if reviews %}
                {% for review in reviews %}
                <div class="review-item">
                    <div class="review-user">{{ review.name }}</div>
                    <div class="review-body">{{ review.text }}</div>
                </div>
                {% endfor %}
            {% else %}
                <p class="empty-msg">Отзывов об этом фильме пока никто не оставлял. Ты можешь стать первым!</p>
            {% endif %}

            <!-- Добавить свой отзыв -->
            <div class="form-block">
                <h4>Добавить свой отзыв</h4>
                <form action="{{ url_for('movie_detail', movie_id=movie.id) }}" method="POST">
                    <div class="input-group">
                        <label for="name">Твое имя или никнейм:</label>
                        <input type="text" id="name" name="name" class="input-field" placeholder="Введи свое имя..." required>
                    </div>
                    <div class="input-group">
                        <label for="review_text">Твое мнение о фильме:</label>
                        <textarea id="review_text" name="review_text" class="input-field" placeholder="Поделись впечатлениями, разбери сюжет или актерскую игру..." required></textarea>
                    </div>
                    <button type="submit" class="btn-submit">Опубликовать на сайте</button>
                </form>
            </div>
        </div>
    </div>

</body>
</html>
"""

# --- ОБНОВЛЕННЫЙ ПРОКСИ-ОБРАБОТЧИК (РАБОТАЕТ НА ВСТРОЕННЫХ БИБЛИОТЕКАХ) ---
@app.route('/proxy-image')
def proxy_image():
    image_url = request.args.get('url')
    if not image_url:
        return "Missing url parameter", 400
        
    try:
        # Формируем запрос со стандартными заголовками браузера
        req = urllib.request.Request(
            image_url, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Referer': 'https://kinogo.my/'
            }
        )
        # Скачиваем картинку стандартными средствами Python
        with urllib.request.urlopen(req, timeout=12) as response:
            content = response.read()
            content_type = response.headers.get('Content-Type', 'image/jpeg')
            return Response(content, content_type=content_type)
            
    except Exception as e:
        return f"Error loading image through proxy: {str(e)}", 500


# --- ОСНОВНЫЕ СЕРВЕРНЫЕ МАРШРУТЫ (ROUTES) ---

@app.route('/')
def index():
    return render_template_string(INDEX_HTML, movies=MOVIES)


@app.route('/movie/<int:movie_id>', methods=['GET', 'POST'])
def movie_detail(movie_id):
    movie = next((m for m in MOVIES if m["id"] == movie_id), None)
    if not movie:
        return "Извините, данный фильм не найден в базе данных сайта.", 404

    if request.method == 'POST':
        reviewer_name = request.form.get('name', 'Анонимный зритель').strip()
        review_text = request.form.get('review_text', '').strip()
        
        if not reviewer_name:
            reviewer_name = 'Анонимный зритель'
            
        if review_text:
            REVIEWS[movie_id].append({
                "name": reviewer_name,
                "text": review_text
            })
        return redirect(url_for('movie_detail', movie_id=movie_id))

    movie_reviews = REVIEWS.get(movie_id, [])
    return render_template_string(MOVIE_HTML, movie=movie, reviews=movie_reviews)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
