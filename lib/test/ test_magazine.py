import unittest
from lib.models.magazine import Magazine
from lib.models.author import Author
from lib.models.article import Article

class TestMagazine(unittest.TestCase):
    def setUp(self):
        # Create a fresh author and magazine for each test
        self.author1 = Author.create("Author One")
        self.author2 = Author.create("Author Two")
        self.magazine = Magazine.create("Science Weekly", "Science")

    def test_create_magazine(self):
        self.assertIsNotNone(self.magazine.id)
        self.assertEqual(self.magazine.name, "Science Weekly")
        self.assertEqual(self.magazine.category, "Science")

    def test_find_by_id(self):
        found = Magazine.find_by_id(self.magazine.id)
        self.assertIsNotNone(found)
        self.assertEqual(found.name, self.magazine.name)

    def test_articles(self):
        article = self.author1.add_article(self.magazine, "Quantum Physics")
        articles = self.magazine.articles()
        self.assertTrue(len(articles) > 0)
        self.assertEqual(articles[0].title, "Quantum Physics")

    def test_contributors(self):
        self.author1.add_article(self.magazine, "Quantum Physics")
        self.author2.add_article(self.magazine, "Black Holes")
        contributors = self.magazine.contributors()
        self.assertEqual(len(contributors), 2)
        names = [a.name for a in contributors]
        self.assertIn("Author One", names)
        self.assertIn("Author Two", names)

    def test_article_titles(self):
        self.author1.add_article(self.magazine, "Space Exploration")
        self.author1.add_article(self.magazine, "AI and Science")
        titles = self.magazine.article_titles()
        self.assertIn("Space Exploration", titles)
        self.assertIn("AI and Science", titles)

    def test_contributing_authors(self):
        # Add multiple 
        self.author1.add_article(self.magazine, "Title 1")
        self.author1.add_article(self.magazine, "Title 2")
        self.author1.add_article(self.magazine, "Title 3")
        self.author2.add_article(self.magazine, "Single Article")

        contributing = self.magazine.contributing_authors()
        names = [a.name for a in contributing]
        self.assertIn("Author One", names)
        self.assertNotIn("Author Two", names)

if __name__ == '__main__':
    unittest.main()
