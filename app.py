from flask import Flask, render_template_string, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'super_secret_key'

# База фильмов
MOVIES = [
    {"id": 1, "title": "Аватар", "year": 2009, "rating": 7.9, "kinogo_link": "https://kinogo.my/films/146-avatar-2009.html", "poster": "https://kinogo.my/uploads/posts/2017-04/1493391756-1159271017-avatar.jpg", "desc": "Бывший морпех Джейк Салли прикован к инвалидному креслу. Получив задание, он отправляется на базу корпорации на Пандоре, где люди добывают редкий минерал. Джейк вынужден вселиться в аватара — тело, созданное путем генной инженерии с использованием ДНК местных жителей на'ви."},
    {"id": 2, "title": "Властелин колец: Братство Кольца", "year": 2001, "rating": 8.6, "kinogo_link": "https://kinogo.my/films/2500-vlastelin-kolec-bratstvo-kolca-2001.html", "poster": "https://kinogo.my/uploads/posts/2019-07/1563720942-490328414-vlastelin-kolec-bratstvo-kolca.jpg", "desc": "Сказания о Средиземье — это хроника Войны Кольца, войны, длившейся не одну тысячу лет. Хоббит Фродо Бэггинс получает жребий уничтожить Кольцо Всевластия."},
    {"id": 3, "title": "Интерстеллар", "year": 2014, "rating": 8.6, "kinogo_link": "https://kinogo.my/films/5211-interstellar-2014.html", "poster": "https://kinogo.my/uploads/posts/2017-04/1491114790-991695033-interstellar.jpg", "desc": "Когда засуха и пыльные бури приводят человечество к продовольственному кризису, группа ученых отправляется сквозь червоточину в космос в поисках нового дома для людей."},
    {"id": 4, "title": "Начало", "year": 2010, "rating": 8.7, "kinogo_link": "https://kinogo.my/films/3821-nachalo-2010.html", "poster": "https://kinogo.my/uploads/posts/2017-04/1491114986-2049908774-nachalo.jpg", "desc": "Кобб — талантливый вор, крадущий ценные секреты из глубин подсознания во время сна. Редкие способности сделали его ключевым игроком в промышленном шпионаже."},
    {"id": 5, "title": "Темный рыцарь", "year": 2008, "rating": 8.5, "kinogo_link": "https://kinogo.my/films/3154-temnyy-rycar-2008.html", "poster": "https://kinogo.my/uploads/posts/2020-04/1585997266-939135485-temnyy-rycar.jpg", "desc": "Бэтмен вступает в войну с криминалом Готэма, но ситуация выходит из-под контроля с появлением безумного гения по имени Джокер."},
    {"id": 6, "title": "Матрица", "year": 1999, "rating": 8.5, "kinogo_link": "https://kinogo.my/films/1301-matrica-1999.html", "poster": "https://kinogo.my/uploads/posts/2020-01/1578316075-753251593-matrica.jpg", "desc": "Хакер Нео узнает шокирующую правду: привычный мир — это искусственная иллюзия, созданная зловещими машинами."},
    {"id": 7, "title": "Гладиатор", "year": 2000, "rating": 8.6, "kinogo_link": "https://kinogo.my/films/2140-gladiator-2000.html", "poster": "https://kinogo.my/uploads/posts/2017-04/1493391510-611397561-gladiator.jpg", "desc": "Римский полководец Максим предан завистливым сыном императора и становится гладиатором, ищущим мести."},
    {"id": 8, "title": "Маска", "year": 1994, "rating": 8.0, "kinogo_link": "https://kinogo.my/films/2451-maska-1994.html", "poster": "https://kinogo.my/uploads/posts/2023-11/1699995824-1618804087-maska.jpg", "desc": "Робкий банковский служащий находит древнюю маску, которая превращает его в неуязвимого и эксцентричного мультяшного героя."},
    {"id": 9, "title": "Сияние", "year": 1980, "rating": 8.4, "kinogo_link": "https://kinogo.my/films/4120-siyanie-1980.html", "poster": "https://kinogo.my/uploads/posts/2024-01/1704798751-1904935975-siyanie.jpg", "desc": "Джек Торренс устраивается смотрителем в уединенный отель на зиму, где зловещая атмосфера постепенно сводит его с ума."},
    {"id": 10, "title": "Гарри Поттер и философский камень", "year": 2001, "rating": 8.2, "kinogo_link": "https://kinogo.my/films/1125-garri-potter-i-filosofskiy-kamen-2001.html", "poster": "https://kinogo.my/uploads/posts/2019-07/1563015062-1572996915-garri-potter-i-filosofskiy-kamen.jpg", "desc": "Мальчик-сирота узнает, что он волшебник, и отправляется учиться в школу магии Хогвартс."},
    {"id": 11, "title": "Бойцовский клуб", "year": 1999, "rating": 8.7, "kinogo_link": "https://kinogo.my/films/710-boycovskiy-klub-1999.html", "poster": "https://kinogo.my/uploads/posts/2017-04/1491114704-1886867375-boycovskiy-klub.jpg", "desc": "Страдающий бессонницей офисный клерк знакомится с харизматичным Тайлером Дерденом, создавая тайный подпольный клуб."},
    {"id": 12, "title": "Криминальное чтиво", "year": 1994, "rating": 8.6, "kinogo_link": "https://kinogo.my/films/1204-kriminalnoe-chtivo-1994.html", "poster": "https://kinogo.my/uploads/posts/2023-11/1700692804-555184796-kriminalnoe-chtivo.jpg", "desc": "Несколько переплетающихся криминальных историй из жизни лос-анджелесских гангстеров, боксеров и наемников."},
    {"id": 13, "title": "Леон", "year": 1994, "rating": 8.7, "kinogo_link": "https://kinogo.my/films/1250-leon-1994.html", "poster": "https://kinogo.my/uploads/posts/2019-07/1564070804-298906622-leon.jpg", "desc": "Профессиональный киллер Леон берет под свою опеку девочку Матильду, чью семью убили коррумпированные агенты."},
    {"id": 14, "title": "Зеленая миля", "year": 1999, "rating": 9.1, "kinogo_link": "https://kinogo.my/films/1010-zelenaya-milya-1999.html", "poster": "https://kinogo.my/uploads/posts/2017-10/1509302130-598249484-zelenaya-milya.jpg", "desc": "История о заключенном-гиганте с чудесным даром исцеления, ожидающем смертной казни в тюремном блоке."},
    {"id": 15, "title": "Форрест Гамп", "year": 1994, "rating": 8.9, "kinogo_link": "https://kinogo.my/films/2111-forrest-gamp-1994.html", "poster": "https://kinogo.my/uploads/posts/2020-02/1581515741-1303433223-forrest-gamp.jpg", "desc": "Добрая история жизни наивного парня, который благодаря чистой душе невольно становится участником главных исторических событий США."},
    {"id": 16, "title": "Титаник", "year": 1997, "rating": 8.3, "kinogo_link": "https://kinogo.my/films/3200-titanik-1997.html", "poster": "https://kinogo.my/uploads/posts/2017-04/1493541637-176580560-titanik.jpg", "desc": "Чувствительная история любви юных пассажиров разворачивается на фоне крушения гигантского лайнера."},
    {"id": 17, "title": "Побег из Шоушенка", "year": 1994, "rating": 9.1, "kinogo_link": "https://kinogo.my/films/3500-pobeg-iz-shoushenka-1994.html", "poster": "https://kinogo.my/uploads/posts/2017-04/1493224416-1754132569-pobeg-iz-shoushenka.jpg", "desc": "Банкир Энди попадает в суровую тюрьму, но силой ума и надежды завоевывает уважение и планирует побег."},
    {"id": 18, "title": "Терминатор 2: Судный день", "year": 1991, "rating": 8.7, "kinogo_link": "https://kinogo.my/films/3100-terminator-2-sudnyy-den-1991.html", "poster": "https://kinogo.my/uploads/posts/2020-03/1584109913-1352932125-terminator-2-sudnyy-den.jpg", "desc": "Перепрограммированный робот защищает юного Джона Коннора от более совершенного жидкого киборга из будущего."},
    {"id": 19, "title": "Крестный отец", "year": 1972, "rating": 8.7, "kinogo_link": "https://kinogo.my/films/1500-krestnyy-otec-1972.html", "poster": "https://kinogo.my/uploads/posts/2019-11/1572705738-814634704-krestnyy-otec.jpg", "desc": "Монументальная криминальная драма о влиятельном сицилийском клане Корлеоне."},
    {"id": 20, "title": "Назад в будущее", "year": 1985, "rating": 8.6, "kinogo_link": "https://kinogo.my/films/2300-nazad-v-buduschee-1985.html", "poster": "https://kinogo.my/uploads/posts/2020-06/1591629086-1280450088-nazad-v-buduschee.jpg", "desc": "Подросток случайно перемещается в прошлое на машине времени и должен свести своих молодых родителей."},
    
    # Фильмы с 21 по 32
    {"id": 21, "title": "Парк Юрского периода", "year": 1993, "rating": 8.1, "kinogo_link": "https://kinogo.my/films/4500-park-yurskogo-perioda-1993.html", "poster": "https://kinogo.my/uploads/posts/2021-06/1623720375-40215794-park-yurskogo-perioda.jpg", "desc": "Профессор приглашает ученых на секретный остров, где в результате генной инженерии удалось воссоздать живых динозавров."},
    {"id": 22, "title": "Пятый элемент", "year": 1997, "rating": 8.1, "kinogo_link": "https://kinogo.my/films/4600-pyatyy-element-1997.html", "poster": "https://kinogo.my/uploads/posts/2021-06/1623864452-372053901-pyatyy-element.jpg", "desc": "Будущее, Нью-Йорк. Водителю такси случайно падает на пассажирское сиденье загадочная девушка, способная спасти мир от зла."},
    {"id": 23, "title": "Индиана Джонс: В поисках утраченного ковчега", "year": 1981, "rating": 8.0, "kinogo_link": "https://kinogo.my/films/4700-indiana-dzhons-v-poiskah-utrachennogo-kovchega-1981.html", "poster": "https://kinogo.my/uploads/posts/2024-01/1704797556-682424946-indiana-dzhons-v-poiskah-utrachennogo-kovchega.png", "desc": "Археолог-авантюрист Индиана Джонс отправляется на поиски древнего библейского артефакта, опережая нацистов."},
    {"id": 24, "title": "Пираты Карибского моря: Проклятие Черной жемчужины", "year": 2003, "rating": 8.3, "kinogo_link": "https://kinogo.my/films/4800-piraty-karibskogo-morya-proklyatie-chernoy-zhemchuzhiny-2003.html", "poster": "https://kinogo.my/uploads/posts/2019-08/1565167181-936370868-piraty-karibskogo-morya-proklyatie-chernoy-zhemchuzhiny.jpg", "desc": "Эксцентричный капитан Джек Воробей объединяется с молодым кузнецом, чтобы спасти украденную губернаторскую дочь от проклятых пиратов."},
    {"id": 25, "title": "Список Шиндлера", "year": 1993, "rating": 8.8, "kinogo_link": "https://kinogo.my/films/4900-spisok-shindlera-1993.html", "poster": "https://kinogo.my/uploads/posts/2023-11/1700493703-788980300-spisok-shindlera.jpg", "desc": "Реальная история немецкого промышленника Оскара Шиндлера, спасшего жизни более тысячи польских евреев во время Холокоста."},
    {"id": 26, "title": "Унесенные призраками", "year": 2001, "rating": 8.5, "kinogo_link": "https://kinogo.my/films/5000-unesennye-prizrakami-2001.html", "poster": "https://kinogo.my/uploads/posts/2021-07/1625748716-674485052-unesennye-prizrakami.jpg", "desc": "Маленькая Тихиро попадает в таинственный волшебный мир, населенный духами и ведьмами, где ее родителей превращают в свиней."},
    {"id": 27, "title": "Молчание ягнят", "year": 1991, "rating": 8.3, "kinogo_link": "https://kinogo.my/films/5100-molchanie-yagnyat-1991.html", "poster": "https://kinogo.my/uploads/posts/2020-08/1596896527_molchanie-yagnyat.jpg", "desc": "Стажерка ФБР обращается за помощью к блестящему маньяку-психиатру Ганнибалу Лектеру, чтобы поймать другого серийного убийцу."},
    {"id": 28, "title": "Семь", "year": 1995, "rating": 8.3, "kinogo_link": "https://kinogo.my/films/5200-sem-1995.html", "poster": "https://kinogo.my/uploads/posts/2020-05/1588850405-557635205-sem-par-nechistyh.jpg", "desc": "Детективы расследуют серию жутких убийств, совершенных религиозным фанатиком в наказание за семь смертных грехов."},
    {"id": 29, "title": "Престиж", "year": 2006, "rating": 8.5, "kinogo_link": "https://kinogo.my/films/5300-prestizh-2006.html", "poster": "https://kinogo.my/uploads/posts/2019-10/1570689607-1914808766-prestizh.jpg", "desc": "Два фокусника-иллюзиониста из Лондона ведут ожесточенное соперничество, перерастающее в смертельную войну секретов."},
    {"id": 30, "title": "Отступники", "year": 2006, "rating": 8.5, "kinogo_link": "https://kinogo.my/films/5400-otstupniki-2006.html", "poster": "https://kinogo.my/uploads/posts/2019-05/1556979754-1670443593-otstupniki.jpg", "desc": "История двойного агента в полиции и крота в мафии, пытающихся вычислить друг друга в Бостоне."},
    {"id": 31, "title": "Чужой", "year": 1979, "rating": 8.1, "kinogo_link": "https://kinogo.my/films/5500-chuzhoy-1979.html", "poster": "https://kinogo.my/uploads/posts/2025-04/1745563772-2067796298-chuzhoy-carstvo-cheloveka.jpg", "desc": "Экипаж космического корабля принимает сигнал с неизвестной планеты и случайно сталкивается со смертоносным внеземным монстром."},
    {"id": 32, "title": "Психо", "year": 1960, "rating": 8.2, "kinogo_link": "https://kinogo.my/films/5600-psiho-1960.html", "poster": "https://kinogo.my/uploads/posts/2024-10/1729934796-2128314619-psihopatka.jpg", "desc": "Секретарша, похитившая крупную сумму денег, останавливается на ночлег в уединенном мотеле, которым управляет странный молодой человек."},
]

# Автозаполнение остальных фильмов (с 33 по 100)
extra_titles = [
    "Хороший, плохой, злой", "Достучаться до небес", "Карты, деньги, два ствола",
    "Большой куш", "Игры разума", "Области тьмы", "Поймай меня, если сможешь",
    "Остров проклятых", "Шестое чувство", "Мстители", "Железный человек", "Трансформеры",
    "Хоббит: Нежданное путешествие", "Бегущий по лезвию", "Безумный Макс: Дорога ярости", "Джанго освобожденный",
    "Храброе сердце", "Армагеддон", "День сурка", "Красотка", "Привидение",
    "Терминатор", "Чужие", "Хищник", "Крепкий орешек", "Смертельное оружие",
    "Скорость", "Патруль", "Волк с Уолл-стрит", "Доктор Стрэндж", "Тор",
    "Стражи Галактики", "Человек-паук", "Бэтмен: Начало", "Хэнкок", "Я — легенда",
    "Элизиум", "Голодные игры", "Сумерки", "Дюна", "Прометей", "Прибытие",
    "Гравитация", "Луна 2112", "Район №9", "Сфера", "Фантастические твари",
    "Хроники Нарнии", "Золотой компас", "Знакомьтесь, Джо Блэк", "Город ангелов",
    "Экипаж", "Легенда №17", "Движение вверх", "Время первых"
]

for i in range(33, 101):
    t_name = extra_titles[(i - 33) % len(extra_titles)] + (f" (Часть {i})" if i > 85 else "")
    MOVIES.append({
        "id": i,
        "title": t_name,
        "year": 1990 + (i % 33),
        "rating": round(7.0 + (i % 20) / 10, 1),
        "kinogo_link": "https://kinogo.my/",
        "poster": "https://via.placeholder.com/200x300",
        "desc": f"Захватывающий драматический и приключенческий фильм «{t_name}», рассказывающий уникальную историю с неожиданными поворотами судьбы, яркими героями и глубоким смыслом."
    })

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
        .btn{{display:inline-block; background:#ff4a5a; padding:10px 15px; color:white; text-decoration:none; border-radius:5px; margin:5px 5px 5px 0; cursor:pointer; border:none; font-weight:bold; font-size:14px;}}
        .search-box{{margin-left:auto; display:flex; gap:5px;}}
        .search-box input{{padding:6px; border-radius:5px; border:none;}}
        .search-box button{{padding:6px 12px; background:#ff4a5a; color:white; border:none; border-radius:5px; cursor:pointer;}}
        
        /* Стили для модального окна (окошка плеера) */
        .modal {{ display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.85); align-items: center; justify-content: center; }}
        .modal-content {{ background: #1a1a24; padding: 20px; border-radius: 12px; width: 90%; max-width: 900px; position: relative; box-shadow: 0 4px 20px rgba(0,0,0,0.5); }}
        .close-btn {{ position: absolute; right: 15px; top: 10px; color: #aaa; font-size: 30px; font-weight: bold; cursor: pointer; }}
        .close-btn:hover {{ color: #fff; }}
        .player-frame {{ width: 100%; height: 500px; border: none; border-radius: 8px; background: #000; margin-top: 10px; }}
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
                        <button onclick="openPlayer()" class="btn">▶ Смотреть</button>
                        <a href="/add_fav/{mid}" class="btn" style="background:#333;">В Избранное</a>
                    </div>
                </div>
                <div style="flex:1; min-width:280px; background:#1a1a24; padding:20px; border-radius:10px;">
                    <h3 style="margin-top:0; color:#ff4a5a;">Описание фильма</h3>
                    <p style="font-size:16px; line-height:1.6; color:#ccc;">{m.get("desc", "")}</p>
                </div>
            </div>
            
            <!-- Модальное окно с плеером kinogo.my -->
            <div id="playerModal" class="modal">
                <div class="modal-content">
                    <span class="close-btn" onclick="closePlayer()">&times;</span>
                    <h2 style="margin-top:0; color:#ff4a5a;">{m["title"]}</h2>
                    <iframe src="{m["kinogo_link"]}" class="player-frame" allowfullscreen></iframe>
                </div>
            </div>

            <script>
                function openPlayer() {{
                    document.getElementById('playerModal').style.display = 'flex';
                }}
                function closePlayer() {{
                    document.getElementById('playerModal').style.display = 'none';
                }}
                window.onclick = function(event) {{
                    var modal = document.getElementById('playerModal');
                    if (event.target == modal) {{
                        modal.style.display = 'none';
                    }}
                }}
            </script>

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
