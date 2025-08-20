### README for Doxify

---

#### Description:
**Doxify** is a web application for searching and managing local databases. It allows users to upload databases in various formats (CSV, Excel, TXT), perform searches across them, and manage those databases. The app tracks search history and provides the ability to delete databases with confirmation.

---

#### Key Features:
- **Search Databases:** Perform text-based searches within uploaded databases.
- **Supported Formats:** Supports `.csv`, `.xlsx`, `.xls`, and `.txt` database files.
- **Database Management:** Upload new databases and delete selected ones.
- **Search History:** Save and view previous search queries.
- **Simple and intuitive interface.**

---

#### Installation:

1. Clone the repository or download the project:

```bash
git clone https://github.com/Tool-xx/doxify.git
cd doxify
```

2. Install required dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python app.py
```

---

#### Usage:

- Once the app is running, you can upload databases via the interface and search for text matches within them.
- View all uploaded databases on the main page, where a delete button is displayed next to each.
- When deleting a database, a confirmation prompt will appear.
- All search queries are saved in the search history.

---

#### Requirements:

- flask>=2.3.0
- pywebview>=4.0.0
- pandas>=2.0.0
- openpyxl>=3.0.0
- requests>=2.28.0
- Other dependencies in `requirements.txt`


---

