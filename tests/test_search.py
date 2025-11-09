import unittest
from src.models.book import Book
from src.services.search import binary_search

class TestSearch(unittest.TestCase):

    def setUp(self):
        self.books = [
            Book(book_id=1, title="The Great Gatsby", author="F. Scott Fitzgerald"),
            Book(book_id=2, title="1984", author="George Orwell"),
            Book(book_id=3, title="To Kill a Mockingbird", author="Harper Lee"),
            Book(book_id=4, title="Pride and Prejudice", author="Jane Austen"),
            Book(book_id=5, title="The Catcher in the Rye", author="J.D. Salinger"),
        ]
        self.books.sort(key=lambda book: book.title)  # Sort books by title for binary search

    def test_binary_search_found(self):
        result = binary_search(self.books, "1984")
        self.assertIsNotNone(result)
        self.assertEqual(result.book_id, 2)

    def test_binary_search_not_found(self):
        result = binary_search(self.books, "Moby Dick")
        self.assertIsNone(result)

    def test_binary_search_empty_list(self):
        result = binary_search([], "1984")
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()