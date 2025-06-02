from lib.db.connection import get_connection

def fix_article_titles():
    conn = get_connection()
    cursor = conn.cursor()
    
    
    cursor.execute("""
        UPDATE articles
        SET title = 'Untitled Article'
        WHERE title GLOB '[0-9]*'
    """)
    
    
    updates = {
        21: 'Politics and Governance Insights',
        33: 'Health Advances and Discoveries',
        40: 'Science Innovations and Breakthroughs',
        55: 'Economic Trends and Analysis'
    }
    
    for article_id, new_title in updates.items():
        cursor.execute(
            "UPDATE articles SET title = ? WHERE id = ?",
            (new_title, article_id)
        )
    
    conn.commit()
    conn.close()
    print("Article titles updated successfully.")

if __name__ == "__main__":
    fix_article_titles()
