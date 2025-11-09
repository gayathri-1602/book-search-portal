# Book Search Portal

A small Flask app demonstrating searching, sorting, and a simple SQLite-backed data model.

## Quick start (Windows PowerShell)

```powershell
# from project root
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python seed_db.py   # creates data/books.db and inserts sample books
python -m src.app   # starts the dev server
```

Open http://127.0.0.1:5000/ and search for titles (e.g. `1984`).

## Run tests

```powershell
.\.venv\Scripts\Activate.ps1
python -m pytest -q
```

## Notes
- The app uses SQLite at `data/books.db` by default.
- There is an API endpoint `/api/search?query=...` that returns JSON results used by the frontend JS.
- To reset data, delete `data/books.db` and re-run `python seed_db.py`.

## Project layout (key files)

```
src/
   app.py            # Flask app entry
   models/
      db.py           # SQLAlchemy models and helpers
      book.py
      hash_table.py
   routes/
      books.py        # search routes (HTML + API)
   templates/
      index.html
      results.html
   static/
      css/styles.css
      js/main.js
seed_db.py          # creates DB and seeds sample data
requirements.txt
README.md
```

If you'd like, I can also add a small admin UI to add/remove books or integrate Flask-Migrate for schema migrations.