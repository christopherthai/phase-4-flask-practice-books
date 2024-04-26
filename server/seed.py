#!/usr/bin/env python3

from app import app
from models import db, Author, Publisher, Book  # models go here
from faker import Faker

faker = Faker()

if __name__ == "__main__":
    with app.app_context():
        Author.query.delete()
        Publisher.query.delete()
        Book.query.delete()

        print("Seeding database...")

        author1 = Author(name="JK Rowling", pen_name="JK")
        author2 = Author(name="Stephen King", pen_name="Stephen")
        author3 = Author(name="Margaret Atwood", pen_name="Marge")
        author4 = Author(name="Jane Austen", pen_name="Jane")

        publisher1 = Publisher(name="ABC Publications", founding_year=1990)
        publisher2 = Publisher(name="XYZ Books", founding_year=1985)

        book1 = Book(title="Emma", page_count=200, author=author4, publisher=publisher1)
        book2 = Book(title="HP1", page_count=300, author=author1, publisher=publisher2)
        book3 = Book(title="HP2", page_count=300, author=author1, publisher=publisher2)
        book4 = Book(title="HP3", page_count=200, author=author1, publisher=publisher2)
        book5 = Book(title="It", page_count=300, author=author2, publisher=publisher1)
        book6 = Book(
            title="Carrie", page_count=100, author=author2, publisher=publisher1
        )
        book7 = Book(
            title="Oryx and Crake", page_count=500, author=author3, publisher=publisher2
        )
        book8 = Book(
            title="The Blind Assassin",
            page_count=300,
            author=author3,
            publisher=publisher1,
        )

        db.session.add_all(
            [
                author1,
                author2,
                author3,
                author4,
                publisher1,
                publisher2,
                book1,
                book2,
                book3,
                book4,
                book5,
                book6,
                book7,
                book8,
            ]
        )

        db.session.commit()

        # write your seeds here!

        print("Seeding complete!")
