Articles and Magazines Management System
A Python project that manages Authors, Magazines, and Articles using SQLite with raw SQL and object-oriented programming (OOP). This project includes a command-line interface (CLI) for easy interaction.

Table of Contents
Project Overview

Features

Folder Structure

Setup and Installation

How to Clone the Repository

User Interaction (CLI)

How to Use the Python Classes

Database Schema

Contributing

License

Project Overview
This application allows you to:

Create authors, magazines, and articles.

Query articles by author.

Find magazines an author contributes to.

List contributors of a magazine.

Identify authors who contributed more than 2 articles to a magazine.

Use a simple CLI to interact with your data.

Features
Persistent storage with SQLite database.

Raw SQL queries for database operations.

Object-oriented design with Author, Magazine, and Article classes.

CLI for user-friendly interaction.

Modular structure to keep code organized and maintainable.

Folder Structure
bash
Copy
Edit
Articles---without-SQLAlchemy/
│
├── cli.py                     # Command-line interface entry point  
├── README.md                  # This documentation file  
├── python.ini                 # Python environment config (optional)  
├── lib/                       # Main application package  
│   ├── db/                    # Database utilities  
│   │   └── connection.py      # Database connection helper  
│   └── models/                # Model classes for entities  
│       ├── __init__.py        # (Optional) package init  
│       ├── author.py          # Author model and methods  
│       ├── magazine.py        # Magazine model and methods  
│       └── article.py         # Article model and methods  
└── venv/                      # Virtual environment (should be in .gitignore)  
Setup and Installation
1. Prerequisites
Python 3.x installed on your machine

SQLite installed or use the built-in Python sqlite3 module (no separate install needed)

2. Clone the repository
git clone https://github.com/EDEL-WEB/Articles---without-SQLAlchemy.git
cd Articles---without-SQLAlchemy
3. Create and activate a virtual environment (recommended)

python3 -m venv venv
source venv/bin/activate
4. Install dependencie
Currently, this project uses only Python standard libraries, so no additional installations are needed.

5. Initialize the database
Create your SQLite database file and tables using the provided schema or a setup script (not included here). You can use the schema under Database Schema.

User Interaction (CLI)
The project includes a cli.py file for interacting with your data through the command line.

How to run the CLI
Make sure you are in the project root directory:
python cli.py
What you can do in the CLI
Add new authors, magazines, and articles.

View all authors, magazines, or articles.

List all articles by a specific author.

List all magazines an author contributes to.

Find contributors to a magazine.

Find authors who have contributed more than 2 articles to a magazine.

Exit the CLI gracefully.

The CLI will present a menu and prompt you to enter your choice.

How to Use the Python Classes
If you want to work with the project programmatically:

from lib.models.author import Author
from lib.models.magazine import Magazine

# Create an author and magazine
author = Author.create("Alice Smith")
magazine = Magazine.create("Health Weekly", "Health")

# Add an article
article = author.add_article(magazine, "Benefits of Meditation")

# List all articles by the author
articles = author.articles()
for art in articles:
    print(art.title)

# List magazines author contributes to
mags = author.magazines()
print([m.name for m in mags])
Database Schema
Your SQLite database should include the following tables:

sql

CREATE TABLE authors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE magazines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL
);

CREATE TABLE articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author_id INTEGER NOT NULL,
    magazine_id INTEGER NOT NULL,
    FOREIGN KEY(author_id) REFERENCES authors(id),
    FOREIGN KEY(magazine_id) REFERENCES magazines(id)
);

AUTHOR: EDEL OMONDI
