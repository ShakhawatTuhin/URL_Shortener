import random
import sqlite3
import string
from ctypes import HRESULT

from flask import Flask, request, render_template, redirect

app = Flask(__name__, template_folder='templates')

def generate_short_url():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_url TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form.get('url')
        print(f"Received URL: {original_url}")  # Debug: Check what is received

        if not original_url:
            return "Error: URL cannot be empty!", 400

        short_url = generate_short_url()


        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO urls (original_url, short_url) VALUES (?, ?)", (original_url, short_url))
        conn.commit()
        conn.close()

        return render_template('result.html', short_url= short_url)
    return render_template('index.html')


@app.route('/<short_url>')
def redirect_to_url(short_url):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT original_url FROM urls WHERE short_url = ?", (short_url,))
    result = cursor.fetchone()
    conn.close()


    if result:
        return redirect(result[0])
    return "URL not found!", 404

if __name__ == '__main__':
    app.run(debug=True)


