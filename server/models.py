from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


# write your models here!
class Author(db.Model, SerializerMixin):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    pen_name = db.Column(db.String)

    books = db.relationship("Book", back_populates="author", cascade="all, delete")
    publishers = association_proxy("book", "publisher")

    serialize_rules = ("-books.author", "-publishers.authors")

    def __repr__(self):
        return f"<Author id={self.id} name={self.name} pen_name={self.pen_name} />"


class Publisher(db.Model, SerializerMixin):
    __tablename__ = "publishers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    founding_year = db.Column(db.Integer, nullable=False)

    serialize_rules = "-books.publisher"

    books = db.relationship("Book", back_populates="publisher")
    authors = association_proxy("books", "author")

    @validates("founding_year")
    def validates_year(self, key, value):
        if 1600 <= value <= 2024:
            return value
        else:
            raise ValueError("1600 <= value <= 2024")

    def __repr__(self):
        return f"<Publisher id={self.id} name={self.name} founding_year={self.founding_year} />"


class Book(db.Model, SerializerMixin):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    page_count = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"))
    publisher_id = db.Column(db.Integer, db.ForeignKey("publishers.id"))

    author = db.relationship("Author", back_populates="books", cascade="all, delete")
    publisher = db.relationship(
        "Publisher", cascade="all,delete", back_populates="books"
    )

    serialize_rules = ("-author.books", "-publisher.books")

    @validates("page_count")
    def validates_pages(self, key, value):
        if value <= 0:
            raise ValueError("Page must be greater than 0")
        else:
            return value

    def __repr__(self):
        return f"<Book id={self.id} title={self.title} page_count={self.page_count} />"
