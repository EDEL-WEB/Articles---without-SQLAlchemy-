from faker import Faker
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import get_connection
import random

fake = Faker()

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
    try:
        author_id = int(input("Enter author ID: "))
    except ValueError:
        print("Invalid author ID.")
        return
    author = Author.find_by_id(author_id)
    if not author:
        print("Author not found.")
        return

    list_magazines()
    try:
        magazine_id = int(input("Enter magazine ID: "))
    except ValueError:
        print("Invalid magazine ID.")
        return
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, category FROM magazines WHERE id = ?", (magazine_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        print("Magazine not found.")
        return

    magazine = Magazine(*row)
    title = input("Enter article title: ")
    article = author.add_article(magazine, title)
    print(f"Article '{title}' added for author '{author.name}' in magazine '{magazine.name}'.")

def view_author_articles():
    list_authors()
    try:
        author_id = int(input("Enter author ID to view their articles: "))
    except ValueError:
        print("Invalid author ID.")
        return
    author = Author.find_by_id(author_id)
    if author:
        articles = author.articles()
        print_header(f"Articles by {author.name}")
        if not articles:
            print("No articles found.")
        for article in articles:
            print(f"{article.title} (Magazine ID: {article.magazine_id})")
    else:
        print("Author not found.")

def view_magazine_contributors():
    list_magazines()
    try:
        magazine_id = int(input("Enter magazine ID to view contributors: "))
    except ValueError:
        print("Invalid magazine ID.")
        return
    magazine = Magazine.find_by_id(magazine_id)
    if magazine:
        contributors = magazine.contributors()
        print_header(f"Contributors to {magazine.name}")
        if not contributors:
            print("No contributors found.")
        for contributor in contributors:
            print(contributor.name)
    else:
        print("Magazine not found.")

def view_topic_areas():
    list_authors()
    try:
        author_id = int(input("Enter author ID to view topic areas: "))
    except ValueError:
        print("Invalid author ID.")
        return
    author = Author.find_by_id(author_id)
    if author:
        topics = author.topic_areas()
        print_header(f"Topic Areas for {author.name}")
        if not topics:
            print("No topic areas found.")
        for topic in topics:
            print(topic)
    else:
        print("Author not found.")

def list_magazines_by_author():
    list_authors()
    try:
        author_id = int(input("Enter author ID to list their magazines: "))
    except ValueError:
        print("Invalid author ID.")
        return
    author = Author.find_by_id(author_id)
    if author:
        magazines = author.magazines()
        print_header(f"Magazines by {author.name}")
        if magazines:
            for magazine in magazines:
                print(f"- {magazine.name} ({magazine.category})")
        else:
            print("No magazines found.")
    else:
        print("Author not found.")

def list_articles_by_author_name():
    name = input("Enter author name: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM authors WHERE name = ?", (name,))
    row = cursor.fetchone()
    if row:
        author = Author.find_by_id(row[0])
        articles = author.articles()
        print_header(f"Articles by {author.name}")
        for article in articles:
            print(f"{article.title}")
    else:
        print("Author not found.")

def most_prolific_author():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.name, COUNT(ar.id) as article_count
        FROM authors a
        JOIN articles ar ON a.id = ar.author_id
        GROUP BY a.id
        ORDER BY article_count DESC
        LIMIT 1
    """)
    row = cursor.fetchone()
    conn.close()
    if row:
        print_header("Most Prolific Author")
        print(f"{row[0]} with {row[1]} articles")
    else:
        print("No data available.")

def seed_data():
    num_authors = 10
    num_magazines = 5
    articles_per_author = 3

    authors = [Author.create(fake.name()) for _ in range(num_authors)]
    magazines = [Magazine.create(fake.company(), fake.bs()) for _ in range(num_magazines)]

    for author in authors:
        for _ in range(articles_per_author):
            magazine = random.choice(magazines)
            title = fake.sentence(nb_words=6)
            Article.create(title, author.id, magazine.id)

    print(f"✅ Seeded {num_authors} authors, {num_magazines} magazines, and {num_authors * articles_per_author} articles.")

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
        print("9. List magazines by author")
        print("10. List articles by author's name")
        print("11. Show most prolific author")
        print("12. Seed fake data")
        print("13. Exit")
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
            list_magazines_by_author()
        elif choice == "10":
            list_articles_by_author_name()
        elif choice == "11":
            most_prolific_author()
        elif choice == "12":
            seed_data()
        elif choice == "13":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\nExiting. Goodbye!")
