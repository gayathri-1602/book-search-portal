from flask import Blueprint, request, render_template
from src.models.db import get_session, Book as DBBook
from src.models.hash_table import HashTable
from src.services.search import binary_search
from sqlalchemy import select, func


books_bp = Blueprint('books', __name__)

# Build a simple hash table from DB at module load for fast ID lookups.
# It will be (re)populated on first use.
hash_table = HashTable()
_hash_populated = False


@books_bp.route('/search', methods=['GET'])
def search_books():
    # Get search parameters
    query = request.args.get('query')
    method = request.args.get('method', 'binary')
    sort_by = request.args.get('sort', 'title')
    sort_order = request.args.get('order', 'asc')
    genre = request.args.get('genre')
    year_from = request.args.get('year_from')
    year_to = request.args.get('year_to')
    language = request.args.get('language')
    
    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)  # 10 items per page by default

    if not any([query, genre, year_from, year_to, language]):
        # Get unique genres and languages for filter dropdowns
        s = get_session()
        try:
            genres = sorted(set(g[0] for g in s.query(DBBook.genre).distinct() if g[0]))
            languages = sorted(set(l[0] for l in s.query(DBBook.language).distinct() if l[0]))
            years = sorted(set(y[0] for y in s.query(DBBook.publication_year).distinct() if y[0]))
        finally:
            s.close()
        return render_template('index.html', genres=genres, languages=languages,
                             min_year=min(years) if years else None, 
                             max_year=max(years) if years else None)

    books = []

    # Get all books and apply filters
    s = get_session()
    try:
        # Build query with filters
        stmt = select(DBBook)
        
        if query:
            stmt = stmt.where(
                DBBook.title.ilike(f"%{query}%") |
                DBBook.author.ilike(f"%{query}%") |
                DBBook.description.ilike(f"%{query}%")
            )
            
        if genre:
            stmt = stmt.where(DBBook.genre == genre)
            
        if year_from:
            try:
                year_from = int(year_from)
                stmt = stmt.where(DBBook.publication_year >= year_from)
            except ValueError:
                pass
                
        if year_to:
            try:
                year_to = int(year_to)
                stmt = stmt.where(DBBook.publication_year <= year_to)
            except ValueError:
                pass
                
        if language:
            stmt = stmt.where(DBBook.language == language)
            
        # Apply sorting
        if sort_by in ['title', 'author', 'publication_year', 'genre']:
            order_by_col = getattr(DBBook, sort_by)
            if sort_order == 'desc':
                order_by_col = order_by_col.desc()
            stmt = stmt.order_by(order_by_col)
        
        # Count total results for pagination
        total = s.scalar(select(func.count()).select_from(stmt.subquery()))
        
        # Apply pagination
        stmt = stmt.offset((page - 1) * per_page).limit(per_page)
        books = s.scalars(stmt).all()
        
        # Calculate pagination metadata
        total_pages = (total + per_page - 1) // per_page
        has_prev = page > 1
        has_next = page < total_pages
        
    finally:
        s.close()

    return render_template(
        'results.html',
        books=books,
        page=page,
        total_pages=total_pages,
        has_prev=has_prev,
        has_next=has_next,
        total=total,
        query=query,
        sort_by=sort_by,
        sort_order=sort_order,
        genre=genre,
        year_from=year_from,
        year_to=year_to,
        language=language
    )


@books_bp.route('/api/search', methods=['GET'])
def api_search():
    """Return JSON list of matching books for a query parameter 'query'."""
    query = request.args.get('query')
    method = request.args.get('method', 'binary')
    sort = request.args.get('sort', 'title')
    if not query:
        return {"books": []}

    # Ensure hash table populated when needed
    global _hash_populated
    if method == 'id' and not _hash_populated:
        s = get_session()
        try:
            all_books = s.query(DBBook).all()
            for b in all_books:
                hash_table.insert(b)
        finally:
            s.close()
        _hash_populated = True

    books = []
    if method == 'id':
        try:
            book_id = int(query)
            found = hash_table.search(book_id)
            if found:
                books = [{"book_id": found.book_id, "title": found.title, "author": found.author, "source": "HashTable"}]
        except ValueError:
            books = []
    else:
        # binary/title flow: try binary search first on ordered list
        s = get_session()
        try:
            if sort not in ('title', 'author', 'book_id'):
                sort = 'title'
            order_by_col = getattr(DBBook, sort)
            stmt = select(DBBook).order_by(order_by_col)
            results = s.scalars(stmt).all()
            found = binary_search(results, query)
            if found:
                books = [{"book_id": found.book_id, "title": found.title, "author": found.author, "source": "BinarySearch"}]
            else:
                # fallback: partial matches
                stmt2 = select(DBBook).where(DBBook.title.ilike(f"%{query}%")).order_by(order_by_col)
                results2 = s.scalars(stmt2).all()
                books = [{"book_id": b.book_id, "title": b.title, "author": b.author, "source": "Database"} for b in results2]
        finally:
            s.close()

    return {"books": books}


@books_bp.route('/admin/books', methods=['GET'])
def admin_list():
    s = get_session()
    try:
        books = s.query(DBBook).order_by(DBBook.book_id).all()
    finally:
        s.close()
    return render_template('admin_list.html', books=books)


@books_bp.route('/admin/books/add', methods=['GET', 'POST'])
def admin_add():
    if request.method == 'POST':
        book_id = int(request.form['book_id'])
        title = request.form['title'].strip()
        author = request.form['author'].strip()
        isbn = request.form.get('isbn', '').strip()
        genre = request.form.get('genre', '').strip()
        description = request.form.get('description', '').strip()
        publication_year = request.form.get('publication_year', '')
        publisher = request.form.get('publisher', '').strip()
        page_count = request.form.get('page_count', '')
        language = request.form.get('language', '').strip()
        cover_url = request.form.get('cover_url', '').strip()

        # Convert numeric fields
        publication_year = int(publication_year) if publication_year else None
        page_count = int(page_count) if page_count else None

        s = get_session()
        try:
            # Insert or ignore if book_id exists
            existing = s.query(DBBook).filter_by(book_id=book_id).first()
            book_data = {
                'book_id': book_id,
                'title': title,
                'author': author,
                'isbn': isbn or None,
                'genre': genre or None,
                'description': description or None,
                'publication_year': publication_year,
                'publisher': publisher or None,
                'page_count': page_count,
                'language': language or None,
                'cover_url': cover_url or None
            }
            
            if existing:
                for key, value in book_data.items():
                    setattr(existing, key, value)
                s.add(existing)
            else:
                b = DBBook(**book_data)
                s.add(b)
            s.commit()
            # sync hash table
            hash_table.update(DBBook(**book_data))
        finally:
            s.close()
        return ('', 302, {'Location': request.url_root + 'search'})
    return render_template('admin_form.html', book=None)


@books_bp.route('/admin/books/<int:book_id>/edit', methods=['GET', 'POST'])
def admin_edit(book_id):
    s = get_session()
    try:
        book = s.query(DBBook).filter_by(book_id=book_id).first()
    finally:
        s.close()

    if request.method == 'POST':
        title = request.form['title'].strip()
        author = request.form['author'].strip()
        isbn = request.form.get('isbn', '').strip()
        genre = request.form.get('genre', '').strip()
        description = request.form.get('description', '').strip()
        publication_year = request.form.get('publication_year', '')
        publisher = request.form.get('publisher', '').strip()
        page_count = request.form.get('page_count', '')
        language = request.form.get('language', '').strip()
        cover_url = request.form.get('cover_url', '').strip()

        # Convert numeric fields
        publication_year = int(publication_year) if publication_year else None
        page_count = int(page_count) if page_count else None

        s = get_session()
        try:
            book = s.query(DBBook).filter_by(book_id=book_id).first()
            if book:
                book.title = title
                book.author = author
                book.isbn = isbn or None
                book.genre = genre or None
                book.description = description or None
                book.publication_year = publication_year
                book.publisher = publisher or None
                book.page_count = page_count
                book.language = language or None
                book.cover_url = cover_url or None
                s.add(book)
                s.commit()
                # sync hash table
                hash_table.update(book)
        finally:
            s.close()
        return ('', 302, {'Location': request.url_root + 'search'})

    return render_template('admin_form.html', book=book)


@books_bp.route('/admin/books/<int:book_id>/delete', methods=['POST'])
def admin_delete(book_id):
    s = get_session()
    try:
        book = s.query(DBBook).filter_by(book_id=book_id).first()
        if book:
            s.delete(book)
            s.commit()
            hash_table.remove(book_id)
    finally:
        s.close()
    return ('', 302, {'Location': request.url_root + 'admin/books'})