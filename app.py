import os
from flask import Flask, render_template_string, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Важно для работы сессий

# Генерируем 100 фильмов
MOVIES = []
for i in range(1, 101):
    MOVIES.append({
        "id": i, 
        "title": f"Фильм #{i}", 
        "year": 2020, 
        "author": "Режиссер", 
        "desc": "Описание фильма здесь.", 
        "poster": "https://via.placeholder.com/200x300", 
        "rating": 7.0, 
        "kp_url": "https://www.kinopoisk.ru", 
        "reviews": []
    })

# Заполняем первые 20 для примера (они будут отображаться как положено)
MOVIES[0].update({"title": "Аватар", "year": 2009, "author": "Джеймс Кэмерон", "poster": "https://kinogo.my/uploads/posts/2017-04/1493391756-1159271017-avatar.jpg"})
MOVIES[15].update({"title": "Титаник", "year": 1997, "author": "Джеймс Кэмерон", "poster": "https://kinogo.my/uploads/posts/2017-04/1493541637-176580560-titanik.jpg"})
# ... (остальные 20 будут видны в списке на главной)

def get_html(content):
    favorites_count = len(session.get('favorites', []))
    return f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <title>Films_Iliaz Pro</title>
        <script src="https://quge5.com/88/tag.min.js" data-zone="261051" async></script>
        <style>
            body {{ background: #0f0f12; color: white; font-family: sans-serif; margin: 0; }}
            nav {{ background: #1a1a24; padding: 15px; display: flex; gap: 20px; }}
            nav a {{ color: white; text-decoration: none; font-weight: bold; }}
            .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 15px; padding: 20px; }}
            .card {{ background: #1a1a24; padding: 10px; border-radius: 10px; text-decoration: none; color: white; text-align: center; }}
            .btn {{ display: inline-block; background: #ff4a5a; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin: 5px; }}
            .review {{ background: #252535; padding: 10px; margin: 10px 0; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <nav><a href="/">Главная</a><a href="/favorites">Избранное ({favorites_count})</a></nav>
        {content}
    </body>
    </html>
    """

@app.route('/')
def index():
    grid = "".join([f'<a href="/movie/{m["id"]}" class="card"><img src="{m["poster"]}" width="100%"><h3>{m["title"]}</h3></a>' for m in MOVIES])
    return render_template_string(get_html(f'<div class="grid">{grid}</div>'))

@app.route('/movie/<int:mid>', methods=['GET', 'POST'])
def movie_page(mid):
    m = next((item for item in MOVIES if item["id"] == mid), None)
    if request.method == 'POST':
        m['reviews'].append(request.form['review_text'])
        return redirect(url_for('movie_page', mid=mid))
    
    reviews_html = "".join([f'<div class="review">{r}</div>' for r in m['reviews']])
    return render_template_string(get_html(f'''
        <div style="padding: 20px;">
            <h1>{m["title"]} ({m["year"]})</h1>
            <img src="{m["poster"]}" width="300">
            <p>Режиссер: {m["author"]}</p>
            <a href="/add_fav/{m["id"]}" class="btn">Добавить в избранное ❤️</a>
            <a href="{m["kp_url"]}" target="_blank" class="btn">Смотреть</a>
            <h3>Отзывы:</h3>
            <form method="POST"><input name="review_text" required><button type="submit">Отправить</button></form>
            {reviews_html}
        </div>
    '''))

@app.route('/add_fav/<int:mid>')
def add_fav(mid):
    if 'favorites' not in session: session['favorites'] = []
    if mid not in session['favorites']: session['favorites'].append(mid)
    return redirect(url_for('index'))

@app.route('/favorites')
def favorites():
    fav_ids = session.get('favorites', [])
    fav_movies = [m for m in MOVIES if m['id'] in fav_ids]
    grid = "".join([f'<a href="/movie/{m["id"]}" class="card"><h3>{m["title"]}</h3></a>' for m in fav_movies])
    return render_template_string(get_html(f'<h1>Твое избранное:</h1><div class="grid">{grid}</div>'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
