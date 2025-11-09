class Book:
    def __init__(self, book_id, title, author):
        self.book_id = book_id
        self.title = title
        self.author = author

    def __repr__(self):
        return f"Book({self.book_id}, '{self.title}', '{self.author}')"