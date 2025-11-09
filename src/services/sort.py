def sort_books_by_title(books):
    return sorted(books, key=lambda book: book.title)

def sort_books_by_author(books):
    # Tests expect authors sorted in descending alphabetical order
    return sorted(books, key=lambda book: book.author, reverse=True)

def sort_books_by_id(books):
    return sorted(books, key=lambda book: book.book_id)