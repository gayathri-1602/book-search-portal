import unittest
from src.models.hash_table import HashTable
from src.models.book import Book

class TestHashTable(unittest.TestCase):
    def setUp(self):
        self.hash_table = HashTable()
        self.book1 = Book(book_id=1, title="Book One", author="Author A")
        self.book2 = Book(book_id=2, title="Book Two", author="Author B")
        self.book3 = Book(book_id=3, title="Book Three", author="Author C")
        self.hash_table.insert(self.book1)
        self.hash_table.insert(self.book2)
        self.hash_table.insert(self.book3)

    def test_insert(self):
        self.assertEqual(len(self.hash_table.table), 3)
        self.assertIn(1, self.hash_table.table)
        self.assertIn(2, self.hash_table.table)
        self.assertIn(3, self.hash_table.table)

    def test_search_existing_book(self):
        result = self.hash_table.search(1)
        self.assertEqual(result.title, "Book One")

    def test_search_non_existing_book(self):
        result = self.hash_table.search(4)
        self.assertIsNone(result)

    def test_search_after_insert(self):
        book4 = Book(book_id=4, title="Book Four", author="Author D")
        self.hash_table.insert(book4)
        result = self.hash_table.search(4)
        self.assertEqual(result.title, "Book Four")

if __name__ == '__main__':
    unittest.main()