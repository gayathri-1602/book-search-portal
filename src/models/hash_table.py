class HashTable:
    def __init__(self):
        self.table = {}

    def insert(self, book):
        self.table[book.book_id] = book

    def search(self, book_id):
        return self.table.get(book_id, None)

    def remove(self, book_id):
        return self.table.pop(book_id, None)

    def update(self, book):
        # Insert or replace
        self.table[book.book_id] = book