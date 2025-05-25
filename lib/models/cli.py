from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import get_connection

def print_header(title):
    print(f"\n{'=' * 50}\n{title}\n{'=' * 50}")

def list_authors():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM authors")
    rows = cursor.fetchall()
    conn.close()
    print_header("All Authors")
    for row in rows:
        print(f"{row[0]}: {row[1]}")

def list_magazines():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, category FROM magazines")
    rows = cursor.fetchall()
    conn.close()
    print_header("All Magazines")
    for row in rows:
        print(f"{row[0]}: {row[1]} (Category: {row[2]})")

def create_author():
    name = input("Enter author name: ")
    author = Author.create(name)
    print(f"Author '{author.name}' created with ID {author.id}.")

def create_magazine():
    name = input("Enter magazine name: ")
    category = input("Enter magazine category: ")
    magazine = Magazine.create(name, category)
    print(f"Magazine '{magazine.name}' created with ID {magazine.id}.")

def add_article():
    list_authors()
    author_id = int(input("Enter author ID: "))
    author = Author.find_by_id(author_id)
    if not author:
        print("Author not found.")
        return

    list_magazines()
    magazine_id = int(input("Enter magazine ID: "))
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, category FROM magazines WHERE id = ?", (magazine_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        print("Magazine not found.")
        return

    from lib.models.magazine import Magazine
    magazine = Magazine(*row)

    title = input("Enter article title: ")
    article = author.add_article(magazine, title)
    print(f"Article '{title}' added for author '{author.name}' in magazine '{magazine.name}'.")

def view_author_articles():
    list_authors()
    author_id = int(input("Enter author ID to view their articles: "))
    author = Author.find_by_id(author_id)
    if author:
        articles = author.articles()
        print_header(f"Articles by {author.name}")
        for article in articles:
            print(f"{article.title} (Magazine ID: {article.magazine_id})")
    else:
        print("Author not found.")

def view_magazine_contributors():
    list_magazines()
    magazine_id = int(input("Enter magazine ID to view contributors: "))
    from lib.models.magazine import Magazine
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, category FROM magazines WHERE id = ?", (magazine_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        magazine = Magazine(*row)
        contributors = magazine.contributors()
        print_header(f"Contributors to {magazine.name}")
        for contributor in contributors:
            print(contributor.name)
    else:
        print("Magazine not found.")

def view_topic_areas():
    list_authors()
    author_id = int(input("Enter author ID to view topic areas: "))
    author = Author.find_by_id(author_id)
    if author:
        topics = author.topic_areas()
        print_header(f"Topic Areas for {author.name}")
        for topic in topics:
            print(topic)
    else:
        print("Author not found.")

def menu():
    while True:
        print_header("Magazine Publishing CLI")
        print("1. List all authors")
        print("2. List all magazines")
        print("3. Create a new author")
        print("4. Create a new magazine")
        print("5. Add a new article")
        print("6. View author's articles")
        print("7. View magazine contributors")
        print("8. View author topic areas")
        print("9. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            list_authors()
        elif choice == "2":
            list_magazines()
        elif choice == "3":
            create_author()
        elif choice == "4":
            create_magazine()
        elif choice == "5":
            add_article()
        elif choice == "6":
            view_author_articles()
        elif choice == "7":
            view_magazine_contributors()
        elif choice == "8":
            view_topic_areas()
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    menu()
