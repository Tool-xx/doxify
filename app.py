from flask import Flask, render_template, request, redirect, url_for, flash
import os
import csv
import json
import sqlite3
import pandas as pd
import webbrowser  # Import the webbrowser module

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Папка для загруженных файлов
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Хранилище для истории поиска
search_history = []

# Главная страница с формами для загрузки и поиска
@app.route('/')
def index():
    # Получаем список всех загруженных баз данных
    uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('search.html', history=search_history, files=uploaded_files)

# Маршрут для загрузки базы данных
@app.route('/select_file', methods=['POST'])
def select_file():
    if 'file' not in request.files:
        flash('Файл не выбран!')
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        flash('Нет выбранного файла!')
        return redirect(url_for('index'))

    # Сохраняем загруженный файл в папку
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    flash(f'Файл {file.filename} успешно загружен!')
    return redirect(url_for('index'))

# Маршрут для удаления базы данных
@app.route('/delete_file/<filename>', methods=['POST'])
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        os.remove(file_path)
        flash(f'База данных {filename} удалена.')
    except Exception as e:
        flash(f'Не удалось удалить файл: {str(e)}')

    return redirect(url_for('index'))

# Маршрут для поиска по выбранной базе данных
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
            cursor.execute("SELECT * FROM your_table_name")  # Замените your_table_name на имя таблицы в базе
            rows = cursor.fetchall()
            for row in rows:
                if search_term.lower() in str(row).lower():
                    results.append(row)

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

    # Добавляем запрос в историю
    search_history.append(search_term)

    return render_template('results.html', results=results)

# Запуск приложения
if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    # Открыть веб-браузер с вашим сайтом
    webbrowser.open('http://127.0.0.1:5000/')
    
    app.run(debug=True)
