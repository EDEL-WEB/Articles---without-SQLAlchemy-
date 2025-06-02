from lib.db.connection import get_connection, get_connection_cm

class Article:
    def __init__(self, id, title, author_id, magazine_id):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id

    def __repr__(self):
        return f"<Article id={self.id} title={self.title}>"

    @classmethod
    def create(cls, title, author_id, magazine_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
            (title, author_id, magazine_id)
        )
        conn.commit()
        article_id = cursor.lastrowid
        conn.close()
        return cls(article_id, title, author_id, magazine_id)

    @classmethod
    def all(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, author_id, magazine_id FROM articles")
        rows = cursor.fetchall()
        conn.close()
        return [cls(*row) for row in rows]

    @classmethod
    def find_by_author(cls, author_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, author_id, magazine_id FROM articles WHERE author_id = ?", (author_id,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(*row) for row in rows]

    @classmethod
    def find_by_magazine(cls, magazine_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, author_id, magazine_id FROM articles WHERE magazine_id = ?", (magazine_id,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(*row) for row in rows]

class Magazine:
    def __init__(self, id=None, name=None, category=None):
        self.id = id
        self.name = name
        self.category = category

    def __repr__(self):
        return f"<Magazine id={self.id} name={self.name} category={self.category}>"

    @classmethod
    def create(cls, name, category):
        with get_connection_cm() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (name, category))
            conn.commit()
            magazine_id = cursor.lastrowid
        return cls(magazine_id, name, category)

    def save(self):
        with get_connection_cm() as conn:
            cursor = conn.cursor()
            if self.id is None:
                cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (self.name, self.category))
                self.id = cursor.lastrowid
            else:
                cursor.execute("UPDATE magazines SET name = ?, category = ? WHERE id = ?", (self.name, self.category, self.id))
            conn.commit()

    @classmethod
    def find_by_category(cls, category):
        with get_connection_cm() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, category FROM magazines WHERE category = ?", (category,))
            row = cursor.fetchone()
        if row:
            return cls(*row)
        return None

    @classmethod
    def find_by_name(cls, name):
        with get_connection_cm() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, category FROM magazines WHERE name = ?", (name,))
            row = cursor.fetchone()
        if row:
            return cls(*row)
        return None

    def contributors(self):
        from lib.models.author import Author
        with get_connection_cm() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT a.id, a.name
                FROM authors a
                JOIN articles ar ON a.id = ar.author_id
                WHERE ar.magazine_id = ?
            """, (self.id,))
            rows = cursor.fetchall()
        return [Author(row[0], row[1]) for row in rows]

    def article_titles(self):
        with get_connection_cm() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT title FROM articles WHERE magazine_id = ?", (self.id,))
            rows = cursor.fetchall()
        return [row[0] for row in rows]

    def contributing_authors(self):
        from lib.models.author import Author
        with get_connection_cm() as conn:
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
        return [Author(row[0], row[1]) for row in rows]

    @classmethod
    def with_multiple_authors(cls):
        with get_connection_cm() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT m.id, m.name, m.category
                FROM magazines m
                JOIN articles a ON m.id = a.magazine_id
                GROUP BY m.id
                HAVING COUNT(DISTINCT a.author_id) > 1
            """)
            rows = cursor.fetchall()
        return [cls(*row) for row in rows]

    @classmethod
    def article_counts(cls):
        with get_connection_cm() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT m.id, m.name, m.category, COUNT(a.id) as article_count
                FROM magazines m
                LEFT JOIN articles a ON m.id = a.magazine_id
                GROUP BY m.id
            """)
            rows = cursor.fetchall()
        return [{"id": row[0], "name": row[1], "category": row[2], "article_count": row[3]} for row in rows]
