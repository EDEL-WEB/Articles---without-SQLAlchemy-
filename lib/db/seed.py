# lib/db/seed.py

from lib.db.connection import get_connection

def seed_db():
    conn = get_connection("my_database.db") 
    cursor = conn.cursor()
    

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS magazines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author_id INTEGER,
            magazine_id INTEGER,
            FOREIGN KEY(author_id) REFERENCES authors(id),
            FOREIGN KEY(magazine_id) REFERENCES magazines(id)
        )
    """)
    
    cursor.execute("INSERT INTO authors (name) VALUES (?)", ("Test Author",))
    cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", ("Test Magazine", "Test Category"))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    seed_db()
