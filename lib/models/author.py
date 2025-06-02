import unittest
from lib.db.connection import get_connection_cm
from lib.models.article import Article

class Author:
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"<Author id={self.id} name={self.name}>"

    @classmethod
    def create(cls, name):
        with get_connection_cm() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO authors (name) VALUES (?)", (name,))
            conn.commit()
            author_id = cursor.lastrowid
        return cls(author_id, name)

    @classmethod
    def find_by_name(cls, name):
        with get_connection_cm() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM authors WHERE name = ?", (name,))
            row = cursor.fetchone()
        if row:
            return cls(*row)
        return None

    def add_article(self, magazine, title):
        return Article.create(title, self.id, magazine.id)

    def articles(self):
        return Article.find_by_author(self.id)

    def magazines(self):
        from lib.models.magazine import Magazine
        with get_connection_cm() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT m.id, m.name, m.category
                FROM magazines m
                JOIN articles a ON m.id = a.magazine_id
                WHERE a.author_id = ?
            """, (self.id,))
            rows = cursor.fetchall()
        return [Magazine(*row) for row in rows]

    def topic_areas(self):
        with get_connection_cm() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT m.category
                FROM magazines m
                JOIN articles a ON m.id = a.magazine_id
                WHERE a.author_id = ?
            """, (self.id,))
            rows = cursor.fetchall()
        return [row[0] for row in rows]

    def save(self):
        with get_connection_cm() as conn:
            cursor = conn.cursor()
            if self.id is None:
                cursor.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
                self.id = cursor.lastrowid
            else:
                cursor.execute("UPDATE authors SET name = ? WHERE id = ?", (self.name, self.id))
            conn.commit()

    @classmethod
    def top_author(cls):
        with get_connection_cm() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT a.id, a.name, COUNT(ar.id) as article_count
                FROM authors a
                JOIN articles ar ON a.id = ar.author_id
                GROUP BY a.id
                ORDER BY article_count DESC
                LIMIT 1
            """)
            row = cursor.fetchone()
        if row:
            return cls(row[0], row[1])
        return None

# --- Unit tests (for development only, best in a separate test file) ---

class TestAuthor(unittest.TestCase):
    def setUp(self):
        from lib.models.magazine import Magazine
        with get_connection_cm() as conn:
            cursor = conn.cursor()
            cursor.executescript("""
                DELETE FROM articles;
                DELETE FROM authors;
                DELETE FROM magazines;
            """)
            conn.commit()

        self.author = Author.create("Jane Doe")
        self.mag1 = Magazine.create("Nature Weekly", "Science")
        self.mag2 = Magazine.create("Tech Digest", "Technology")

    def test_create_author(self):
        self.assertIsInstance(self.author, Author)
        self.assertEqual(self.author.name, "Jane Doe")

    def test_add_article(self):
        article = self.author.add_article(self.mag1, "Climate Change")
        from lib.models.article import Article
        self.assertIsInstance(article, Article)
        self.assertEqual(article.title, "Climate Change")

    def test_articles_method(self):
        self.author.add_article(self.mag1, "A1")
        self.author.add_article(self.mag2, "A2")
        self.assertEqual(len(self.author.articles()), 2)

    def test_magazines_method(self):
        self.author.add_article(self.mag1, "Sci A")
        self.author.add_article(self.mag2, "Tech B")
        magazine_names = [mag.name for mag in self.author.magazines()]
        self.assertIn("Nature Weekly", magazine_names)
        self.assertIn("Tech Digest", magazine_names)

    def test_topic_areas(self):
        self.author.add_article(self.mag1, "X")
        self.author.add_article(self.mag2, "Y")
        categories = self.author.topic_areas()
        self.assertIn("Science", categories)
        self.assertIn("Technology", categories)
