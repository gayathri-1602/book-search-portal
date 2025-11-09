def search_books(books, query=None, filters=None):
    """
    Search books with advanced filtering and sorting.
    
    Arguments:
    - books: list of Book instances
    - query: search term for title/author/description (optional)
    - filters: dict with filter criteria (optional):
        - genre: string
        - year_from: int
        - year_to: int
        - language: string
    
    Returns: list of matching Book instances
    """
    results = books

    # Text search across multiple fields
    if query:
        query = query.lower()
        results = [
            book for book in results
            if query in book.title.lower() or
               query in book.author.lower() or
               (book.description and query in book.description.lower())
        ]

    # Apply filters if provided
    if filters:
        if 'genre' in filters:
            results = [b for b in results if b.genre == filters['genre']]
        
        if 'year_from' in filters:
            results = [b for b in results if b.publication_year >= filters['year_from']]
            
        if 'year_to' in filters:
            results = [b for b in results if b.publication_year <= filters['year_to']]
            
        if 'language' in filters:
            results = [b for b in results if b.language == filters['language']]

    return results


def binary_search(books, query):
    """
    Perform binary search on a sorted list of books.
    
    Arguments:
    - books: sorted list of Book instances
    - query: search term for title
    
    Returns: matching Book instance or None
    """
    if not books:
        return None
        
    left = 0
    right = len(books) - 1
    
    while left <= right:
        mid = (left + right) // 2
        book = books[mid]
        
        # Case-insensitive comparison
        if book.title.lower() == query.lower():
            return book
        elif book.title.lower() < query.lower():
            left = mid + 1
        else:
            right = mid - 1
            
    return None


def sort_books(books, sort_by='title', reverse=False):
    """
    Sort books by the specified field.
    
    Arguments:
    - books: list of Book instances
    - sort_by: field to sort by ('title', 'author', 'year', 'genre')
    - reverse: if True, sort in descending order
    
    Returns: sorted list of Book instances
    """
    if sort_by == 'year':
        key = lambda x: x.publication_year or 0  # Handle None values
    elif sort_by == 'author':
        key = lambda x: x.author
    elif sort_by == 'genre':
        key = lambda x: x.genre or ''  # Handle None values
    else:  # default to title
        key = lambda x: x.title
        
    return sorted(books, key=key, reverse=reverse)