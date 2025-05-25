import sys
import os
import unittest
import sqlite3

# Add root path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from lib.db.connection import get_connection
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

class TestAuthor(unittest.TestCase):
    def setUp(self):
        # Initialize the in-memory DB schema
        self.conn = get_connection()
        with open("lib/db/schema.sql") as f:
            self.conn.executescript(f.read())

        # Now create author and magazine
        self.author = Author.create("Test Author")
        self.magazine = Magazine.create("Test Magazine", "Test Category")

    def tearDown(self):
        self.conn.close()

    def test_create_author(self):
        self.assertIsNotNone(self.author.id)

    def test_add_article(self):
        article = self.author.add_article(self.magazine, "Test Article")
        self.assertEqual(article.title, "Test Article")
        self.assertEqual(article.author_id, self.author.id)
        self.assertEqual(article.magazine_id, self.magazine.id)

    def test_articles(self):
        self.author.add_article(self.magazine, "Test Article")
        articles = self.author.articles()
        self.assertTrue(len(articles) > 0)

    def test_magazines(self):
        self.author.add_article(self.magazine, "Test Article")
        magazines = self.author.magazines()
        self.assertTrue(len(magazines) > 0)

    def test_topic_areas(self):
        self.author.add_article(self.magazine, "Test Article")
        topics = self.author.topic_areas()
        self.assertIn("Test Category", topics)

if __name__ == "__main__":
    unittest.main()
