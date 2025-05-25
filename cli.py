# cli.py

from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def main():
    print("\n=== Welcome to the Articles CLI ===\n")
    while True:
        print("Options:")
        print("1. Create Author")
        print("2. Create Magazine")
        print("3. Add Article")
        print("4. List Articles by Author")
        print("5. List Magazines by Author")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter author name: ")
            author = Author.create(name)
            print(f"Author '{author.name}' created with ID {author.id}.")

        elif choice == "2":
            name = input("Enter magazine name: ")
            category = input("Enter magazine category: ")
            magazine = Magazine.create(name, category)
            print(f"Magazine '{magazine.name}' created with ID {magazine.id}.")

        elif choice == "3":
            author_id = int(input("Enter author ID: "))
            magazine_id = int(input("Enter magazine ID: "))
            title = input("Enter article title: ")
            author = Author.find_by_id(author_id)
            magazine = Magazine(magazine_id, "", "") 
            article = author.add_article(magazine, title)
            print(f"Article '{title}' added for author ID {author_id} and magazine ID {magazine_id}.")

        elif choice == "4":
            author_id = int(input("Enter author ID: "))
            author = Author.find_by_id(author_id)
            if author:
                for article in author.articles():
                    print(f"- {article.title}")
            else:
                print("Author not found.")

        elif choice == "5":
            author_id = int(input("Enter author ID: "))
            author = Author.find_by_id(author_id)
            if author:
                for mag in author.magazines():
                    print(f"- {mag.name} ({mag.category})")
            else:
                print("Author not found.")

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
