import sys
import os
import unittest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import get_connection

# Add root path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

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
        self.assertIsInstance(self.author, Author)
        self.assertEqual(self.author.name, "Test Author")

    def test_add_article(self):
        article = self.author.add_article(self.magazine, "Test Article")
        self.assertIsInstance(article, Article)
        self.assertEqual(article.title, "Test Article")
        self.assertEqual(article.author_id, self.author.id)
        self.assertEqual(article.magazine_id, self.magazine.id)

    def test_articles_method(self):
        self.author.add_article(self.magazine, "Article 1")
        self.author.add_article(self.magazine, "Article 2")
        self.assertEqual(len(self.author.articles()), 2)

    def test_magazines_method(self):
        self.author.add_article(self.magazine, "Article 1")
        self.author.add_article(self.magazine, "Article 2")
        magazine_names = [mag.name for mag in self.author.magazines()]
        self.assertIn("Test Magazine", magazine_names)

    def test_topic_areas(self):
        self.author.add_article(self.magazine, "Article 1")
        self.author.add_article(self.magazine, "Article 2")
        topics = self.author.topic_areas()
        self.assertIn("Test Category", topics)

if __name__ == "__main__":
    unittest.main()
