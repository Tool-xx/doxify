import webview
import os
import csv
import json
import sqlite3
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import threading
import logging
import sys
import re
from datetime import datetime
from functools import wraps
import html

# Отключаем все логи
logging.getLogger('werkzeug').disabled = True
logging.getLogger('flask').disabled = True

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
app.config['EXPORT_FOLDER'] = 'exports'

# Отключаем логирование Flask
app.logger.disabled = True

# Создаем папки если их нет
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
if not os.path.exists(app.config['EXPORT_FOLDER']):
    os.makedirs(app.config['EXPORT_FOLDER'])

search_history = []

# Мультиязычная поддержка
LANGUAGES = {
    'en': {
        'title': 'Doxify - Database Search Tool',
        'upload': 'Upload Database',
        'uploaded': 'Uploaded Databases',
        'search': 'Search Database',
        'search_term': 'Enter search query...',
        'select_file': 'Select database...',
        'search_btn': 'Search',
        'no_files': 'No files uploaded',
        'delete_confirm': 'Delete database "{}"?',
        'results_title': 'Search Results',
        'results_count': 'Records found: {}',
        'back': 'New Search',
        'nothing_found': 'Nothing found for your query',
        'try_again': 'Try changing search conditions',
        'export_html': 'Export to HTML',
        'advanced_search': 'Advanced Search',
        'regex_search': 'Regex Search',
        'case_sensitive': 'Case Sensitive',
        'whole_word': 'Whole Word',
        'export_success': 'HTML exported successfully',
        'export_error': 'Error exporting HTML',
        'file_uploaded': 'File {} successfully uploaded!',
        'file_deleted': 'Database {} deleted.',
        'file_error': 'Failed to delete file: {}',
        'search_error': 'Select database before searching.',
        'format_error': 'File format not supported!',
        'process_error': 'File processing error: {}'
    },
    'ru': {
        'title': 'Doxify - Поиск по базам данных',
        'upload': 'Загрузить базу данных',
        'uploaded': 'Загруженные базы данных',
        'search': 'Поиск по базе данных',
        'search_term': 'Введите запрос для поиска...',
        'select_file': 'Выберите базу...',
        'search_btn': 'Найти',
        'no_files': 'Файлы не загружены',
        'delete_confirm': 'Удалить базу данных "{}"?',
        'results_title': 'Результаты поиска',
        'results_count': 'Найдено записей: {}',
        'back': 'Новый поиск',
        'nothing_found': 'Ничего не найдено по вашему запросу',
        'try_again': 'Попробуйте изменить условия поиска',
        'export_html': 'Экспорт в HTML',
        'advanced_search': 'Расширенный поиск',
        'regex_search': 'Поиск по regex',
        'case_sensitive': 'Чувствительность к регистру',
        'whole_word': 'Целое слово',
        'export_success': 'HTML успешно экспортирован',
        'export_error': 'Ошибка экспорта HTML',
        'file_uploaded': 'Файл {} успешно загружен!',
        'file_deleted': 'База данных {} удалена.',
        'file_error': 'Не удалось удалить файл: {}',
        'search_error': 'Выберите базу данных перед поиском.',
        'format_error': 'Формат файла не поддерживается!',
        'process_error': 'Ошибка обработки файла: {}'
    }
}

def get_language():
    return request.args.get('lang', 'ru')

def lang_context(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        lang = get_language()
        return func(*args, **kwargs, lang=lang)
    return wrapper

@app.route('/')
@lang_context
def index(lang):
    uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('search.html', 
                         history=search_history, 
                         files=uploaded_files,
                         lang=lang,
                         tr=LANGUAGES[lang])

@app.route('/select_file', methods=['POST'])
@lang_context
def select_file(lang):
    if 'file' not in request.files:
        flash(LANGUAGES[lang]['file_error'].format('No file selected'), 'error')
        return redirect(url_for('index', lang=lang))

    file = request.files['file']
    if file.filename == '':
        flash(LANGUAGES[lang]['file_error'].format('No file selected'), 'error')
        return redirect(url_for('index', lang=lang))

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    flash(LANGUAGES[lang]['file_uploaded'].format(file.filename), 'success')
    return redirect(url_for('index', lang=lang))

@app.route('/delete_file/<filename>', methods=['POST'])
@lang_context
def delete_file(filename, lang):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        os.remove(file_path)
        flash(LANGUAGES[lang]['file_deleted'].format(filename), 'success')
    except Exception as e:
        flash(LANGUAGES[lang]['file_error'].format(str(e)), 'error')

    return redirect(url_for('index', lang=lang))

def advanced_search(text, pattern, case_sensitive=False, whole_word=False, regex=False):
    """Расширенный поиск с поддержкой разных режимов"""
    if not text or not pattern:
        return False
        
    if not case_sensitive:
        text = text.lower()
        pattern = pattern.lower()

    if regex:
        try:
            flags = 0 if case_sensitive else re.IGNORECASE
            return bool(re.search(pattern, text, flags))
        except re.error:
            return False
    elif whole_word:
        words = re.findall(r'\b\w+\b', text)
        return any(word == pattern for word in words)
    else:
        return pattern in text

@app.route('/search', methods=['POST'])
@lang_context
def search(lang):
    search_term = request.form['search_term']
    selected_file = request.form['selected_file']
    search_type = request.form.get('search_type', 'simple')
    case_sensitive = 'case_sensitive' in request.form
    whole_word = 'whole_word' in request.form

    if not selected_file:
        flash(LANGUAGES[lang]['search_error'], 'error')
        return redirect(url_for('index', lang=lang))

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], selected_file)
    results = []
    file_extension = os.path.splitext(file_path)[1].lower()

    try:
        if file_extension == '.csv':
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    row_text = ' '.join(str(v) for v in row.values())
                    if advanced_search(row_text, search_term, case_sensitive, whole_word, search_type == 'regex'):
                        results.append(row)

        elif file_extension == '.json':
            with open(file_path, 'r', encoding='utf-8') as jsonfile:
                data = json.load(jsonfile)
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            item_text = ' '.join(str(v) for v in item.values())
                        else:
                            item_text = str(item)
                        if advanced_search(item_text, search_term, case_sensitive, whole_word, search_type == 'regex'):
                            results.append(item)
                elif isinstance(data, dict):
                    item_text = ' '.join(str(v) for v in data.values())
                    if advanced_search(item_text, search_term, case_sensitive, whole_word, search_type == 'regex'):
                        results.append(data)

        elif file_extension == '.xlsx':
            df = pd.read_excel(file_path)
            for _, row in df.iterrows():
                row_text = ' '.join(str(v) for v in row.values)
                if advanced_search(row_text, search_term, case_sensitive, whole_word, search_type == 'regex'):
                    results.append(row.to_dict())

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
                    row_text = ' '.join(str(v) for v in row)
                    if advanced_search(row_text, search_term, case_sensitive, whole_word, search_type == 'regex'):
                        results.append(dict(zip(col_names, row)))
            conn.close()

        elif file_extension == '.txt':
            with open(file_path, 'r', encoding='utf-8') as txtfile:
                for line in txtfile:
                    if advanced_search(line, search_term, case_sensitive, whole_word, search_type == 'regex'):
                        results.append({"line": line.strip(), "file": selected_file})

        else:
            flash(LANGUAGES[lang]['format_error'], 'error')
            return redirect(url_for('index', lang=lang))

    except Exception as e:
        flash(LANGUAGES[lang]['process_error'].format(str(e)), 'error')
        return redirect(url_for('index', lang=lang))

    search_history.append({
        'term': search_term,
        'file': selected_file,
        'type': search_type,
        'case_sensitive': case_sensitive,
        'whole_word': whole_word,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'results_count': len(results)
    })
    
    return render_template('results.html', 
                         results=results, 
                         search_term=search_term,
                         search_type=search_type,
                         case_sensitive=case_sensitive,
                         whole_word=whole_word,
                         lang=lang,
                         tr=LANGUAGES[lang])

def generate_html_export(results, search_term, search_params):
    """Генерация HTML отчета"""
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"doxify_export_{timestamp}.html"
    filepath = os.path.join(app.config['EXPORT_FOLDER'], filename)
    
    # Создаем красивый HTML отчет
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Doxify Export - {search_term}</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #2d2d2d 100%);
                color: #ffffff;
                margin: 0;
                padding: 20px;
                min-height: 100vh;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: rgba(255, 255, 255, 0.02);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                padding: 30px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            }}
            .header {{
                text-align: center;
                margin-bottom: 30px;
                background: linear-gradient(45deg, #ff2a6d, #ff6b9d, #00ff88);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-size: 2.5em;
                font-weight: 800;
            }}
            .search-info {{
                background: rgba(255, 42, 109, 0.1);
                padding: 20px;
                border-radius: 15px;
                margin-bottom: 30px;
                border-left: 4px solid #ff2a6d;
            }}
            .results-count {{
                background: rgba(0, 255, 136, 0.1);
                padding: 15px;
                border-radius: 10px;
                text-align: center;
                margin-bottom: 20px;
                font-size: 1.2em;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                background: rgba(0, 0, 0, 0.3);
                border-radius: 15px;
                overflow: hidden;
                margin-bottom: 30px;
            }}
            th {{
                background: linear-gradient(45deg, #ff2a6d, #ff6b9d);
                padding: 15px;
                text-align: left;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            td {{
                padding: 12px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                background: rgba(255, 255, 255, 0.05);
            }}
            tr:hover td {{
                background: rgba(255, 255, 255, 0.1);
            }}
            .footer {{
                text-align: center;
                margin-top: 30px;
                color: #b3b3b3;
                font-size: 0.9em;
            }}
            .param-badge {{
                background: rgba(255, 42, 109, 0.2);
                padding: 4px 8px;
                border-radius: 12px;
                margin: 0 5px;
                font-size: 0.8em;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">DOXIFY EXPORT REPORT</div>
            
            <div class="search-info">
                <h2>Search Details</h2>
                <p><strong>Search Term:</strong> {html.escape(search_term)}</p>
                <p><strong>Search Type:</strong> <span class="param-badge">{search_params['type']}</span></p>
                <p><strong>Parameters:</strong> 
                    <span class="param-badge">Case Sensitive: {search_params['case_sensitive']}</span>
                    <span class="param-badge">Whole Word: {search_params['whole_word']}</span>
                </p>
                <p><strong>Export Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>

            <div class="results-count">
                <h3>Results Found: {len(results)}</h3>
            </div>
    """
    
    if results:
        html_content += """
            <table>
                <thead>
                    <tr>
        """
        # Заголовки таблицы
        for key in results[0].keys():
            html_content += f"<th>{html.escape(str(key))}</th>"
        html_content += """
                    </tr>
                </thead>
                <tbody>
        """
        
        # Данные таблицы
        for result in results:
            html_content += "<tr>"
            for value in result.values():
                html_content += f"<td>{html.escape(str(value))}</td>"
            html_content += "</tr>"
        
        html_content += """
                </tbody>
            </table>
        """
    else:
        html_content += """
            <div style="text-align: center; padding: 40px;">
                <h3>No results found for this search query</h3>
                <p>Try modifying your search parameters or using different keywords</p>
            </div>
        """
    
    html_content += f"""
            <div class="footer">
                <p>Generated by Doxify Database Search Tool</p>
                <p>© 2024 Doxify. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Сохраняем файл
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return filename, filepath

@app.route('/export_html')
@lang_context
def export_html(lang):
    try:
        search_term = request.args.get('search_term', '')
        search_type = request.args.get('search_type', 'simple')
        case_sensitive = request.args.get('case_sensitive', 'false') == 'true'
        whole_word = request.args.get('whole_word', 'false') == 'true'
        
        # Получаем результаты из сессии или параметров
        results = []
        results_json = request.args.get('results', '[]')
        try:
            results = json.loads(results_json)
        except:
            pass
        
        search_params = {
            'type': search_type,
            'case_sensitive': 'Yes' if case_sensitive else 'No',
            'whole_word': 'Yes' if whole_word else 'No'
        }
        
        filename, filepath = generate_html_export(results, search_term, search_params)
        
        flash(LANGUAGES[lang]['export_success'], 'success')
        return send_file(
            filepath,
            as_attachment=True,
            download_name=filename,
            mimetype='text/html'
        )
        
    except Exception as e:
        flash(f"{LANGUAGES[lang]['export_error']}: {str(e)}", 'error')
        return redirect(url_for('index', lang=lang))

@app.route('/change_language/<language>')
def change_language(language):
    if language in LANGUAGES:
        return redirect(url_for('index', lang=language))
    return redirect(url_for('index'))

def run_flask():
    from werkzeug.serving import WSGIRequestHandler
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    
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
