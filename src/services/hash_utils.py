def hash_book(book):
    return hash(book.book_id)

def hash_table_size(table):
    return len(table)

def is_book_in_table(table, book_id):
    return book_id in table