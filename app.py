import webview
import os
import csv
import json
import sqlite3
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash
import threading
import logging
import sys

# Полностью отключаем все логи Flask
logging.getLogger('werkzeug').disabled = True
logging.getLogger('flask').disabled = True

# Перенаправляем stdout и stderr чтобы подавить вывод
class HiddenOutput:
    def write(self, s):
        pass
    def flush(self):
        pass

sys.stdout = HiddenOutput()
sys.stderr = HiddenOutput()

# Создаем Flask приложение
app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'uploads'

# Отключаем логирование Flask
app.logger.disabled = True

# Создаем папку для загрузок если её нет
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

search_history = []

@app.route('/')
def index():
    uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('search.html', history=search_history, files=uploaded_files)

@app.route('/select_file', methods=['POST'])
def select_file():
    if 'file' not in request.files:
        flash('Файл не выбран!')
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        flash('Нет выбранного файла!')
        return redirect(url_for('index'))

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    flash(f'Файл {file.filename} успешно загружен!')
    return redirect(url_for('index'))

@app.route('/delete_file/<filename>', methods=['POST'])
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        os.remove(file_path)
        flash(f'База данных {filename} удалена.')
    except Exception as e:
        flash(f'Не удалось удалить файл: {str(e)}')

    return redirect(url_for('index'))

@app.route('/search', methods=['POST'])
def search():
    search_term = request.form['search_term']
    selected_file = request.form['selected_file']

    if not selected_file:
        flash('Выберите базу данных перед поиском.')
        return redirect(url_for('index'))

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], selected_file)
    results = []
    file_extension = os.path.splitext(file_path)[1].lower()

    try:
        if file_extension == '.csv':
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if search_term.lower() in str(row).lower():
                        results.append(row)

        elif file_extension == '.json':
            with open(file_path, 'r', encoding='utf-8') as jsonfile:
                data = json.load(jsonfile)
                for item in data:
                    if search_term.lower() in str(item).lower():
                        results.append(item)

        elif file_extension == '.xlsx':
            df = pd.read_excel(file_path)
            results = df[df.apply(lambda row: search_term.lower() in row.astype(str).str.lower().to_string(), axis=1)].to_dict(orient='records')

        elif file_extension == '.db':
            conn = sqlite3.connect(file_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            if tables:
                table_name = tables[0][0]
                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()
                col_names = [description[0] for description in cursor.description]
                for row in rows:
                    if search_term.lower() in str(row).lower():
                        results.append(dict(zip(col_names, row)))
            conn.close()

        elif file_extension == '.txt':
            with open(file_path, 'r', encoding='utf-8') as txtfile:
                for line in txtfile:
                    if search_term.lower() in line.lower():
                        results.append({"line": line.strip()})

        else:
            flash('Формат файла не поддерживается!')
            return redirect(url_for('index'))

    except Exception as e:
        flash(f'Ошибка обработки файла: {str(e)}')
        return redirect(url_for('index'))

    search_history.append(search_term)
    return render_template('results.html', results=results)

def run_flask():
    # Запускаем Flask без логов и сообщений
    from werkzeug.serving import WSGIRequestHandler
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    
    # Запускаем с минимальным выводом
    app.run(
        host='127.0.0.1', 
        port=5000, 
        debug=False, 
        use_reloader=False,
        threaded=True
    )

if __name__ == '__main__':
    # Запускаем Flask в отдельном потоке
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Даем серверу время запуститься
    import time
    time.sleep(2)
    
    # Создаем и сразу открываем наше окно
    window = webview.create_window(
        'Doxify - Database Search Tool',
        'http://127.0.0.1:5000/',
        width=1200,
        height=800,
        min_size=(800, 600),
        text_select=True,
        confirm_close=True
    )
    
    # Запускаем приложение
    webview.start()
