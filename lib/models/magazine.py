from lib.db.connection import get_connection
from lib.models.article import Article

class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

    @classmethod
    def create(cls, name, category):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO magazines (name, category) VALUES (?, ?)",
            (name, category)
        )
        conn.commit()
        magazine_id = cursor.lastrowid
        conn.close()
        return cls(magazine_id, name, category)

    def contributors(self):
        from lib.models.author import Author  # import here
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT a.id, a.name
            FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            WHERE ar.magazine_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Author(*row) for row in rows]

    def contributing_authors(self):
        from lib.models.author import Author  # import here as well
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.id, a.name
            FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            WHERE ar.magazine_id = ?
            GROUP BY a.id
            HAVING COUNT(ar.id) > 2
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Author(*row) for row in rows]
