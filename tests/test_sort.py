import unittest
from src.models.book import Book
from src.services.sort import sort_books_by_title, sort_books_by_author

class TestSortFunctions(unittest.TestCase):

    def setUp(self):
        self.books = [
            Book(book_id=1, title="The Great Gatsby", author="F. Scott Fitzgerald"),
            Book(book_id=2, title="1984", author="George Orwell"),
            Book(book_id=3, title="To Kill a Mockingbird", author="Harper Lee"),
        ]

    def test_sort_books_by_title(self):
        sorted_books = sort_books_by_title(self.books)
        self.assertEqual(sorted_books[0].title, "1984")
        self.assertEqual(sorted_books[1].title, "The Great Gatsby")
        self.assertEqual(sorted_books[2].title, "To Kill a Mockingbird")

    def test_sort_books_by_author(self):
        sorted_books = sort_books_by_author(self.books)
        self.assertEqual(sorted_books[0].author, "Harper Lee")
        self.assertEqual(sorted_books[1].author, "George Orwell")
        self.assertEqual(sorted_books[2].author, "F. Scott Fitzgerald")

if __name__ == '__main__':
    unittest.main()