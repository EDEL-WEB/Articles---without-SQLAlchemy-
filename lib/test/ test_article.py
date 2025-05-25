import unittest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

class TestArticle(unittest.TestCase):
    def setUp(self):
        # Create test data: authors, magazine
        self.author = Author.create("Jane Doe")
        self.magazine = Magazine.create("Tech Today", "Technology")

    def test_create_article(self):
        article = Article.create(self.author.id, self.magazine.id, "The Future of AI")
        self.assertIsNotNone(article.id)
        self.assertEqual(article.title, "The Future of AI")
        self.assertEqual(article.author_id, self.author.id)
        self.assertEqual(article.magazine_id, self.magazine.id)

    def test_find_by_magazine(self):
        
        Article.create(self.author.id, self.magazine.id, "AI Trends")
        Article.create(self.author.id, self.magazine.id, "Quantum Computing")

        articles = Article.find_by_magazine(self.magazine.id)
        self.assertTrue(len(articles) >= 2)
        titles = [article.title for article in articles]
        self.assertIn("AI Trends", titles)
        self.assertIn("Quantum Computing", titles)

    def test_article_fields(self):
        article = Article.create(self.author.id, self.magazine.id, "Deep Learning")
        self.assertEqual(article.author_id, self.author.id)
        self.assertEqual(article.magazine_id, self.magazine.id)
        self.assertEqual(article.title, "Deep Learning")

if __name__ == '__main__':
    unittest.main()
