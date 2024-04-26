#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_restful import Api, Resource
from flask_migrate import Migrate

from models import db, Author, Publisher, Book

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.get("/")
def index():
    return "Hello world"


# write your routes here!
class AuthorsByID(Resource):

    def get(self, id):
        author = Author.query.get(id)

        if author is None:
            make_response({"error": "Author not found"}, 404)
        else:
            return make_response(
                {
                    "id": author.id,
                    "name": author.name,
                    "pen_name": author.pen_name,
                    "books": [book.to_dict() for book in author.books],
                },
                200,
            )

    def delete(self, id):

        author = Author.query.get(id)

        if author is None:
            return make_response({"error": "Author not found"}, 404)
        else:
            db.session.delete(author)
            db.session.commit()
            return make_response({"message": "Author deleted"}, 200)


api.add_resource(AuthorsByID, "/authors/<int:id>")


class Books(Resource):
    def get(self):

        try:
            books = [book.to_dict() for book in Book.query.all()]
            return make_response(books, 200)
        except Exception:
            return make_response({"error": "Books not found"}, 404)

    def post(self):

        try:
            data = request.json

            new_book = Book(
                title=data["title"],
                page_count=data["page_count"],
                author_id=data["author_id"],
                publisher_id=data["publisher_id"],
            )

            db.session.add(new_book)
            db.session.commit()

            return make_response(new_book.to_dict(), 201)

        except Exception:
            return make_response({"error": "Invalid data"}, 400)


api.add_resource(Books, "/books")


class PublisherByID(Resource):

    def get(self, id):

        publisher = Publisher.query.get(id)

        if publisher is None:
            return make_response({"error": "Publisher not found"}, 404)
        else:
            return make_response(
                {
                    "id": publisher.id,
                    "name": publisher.name,
                    "founding_year": publisher.founding_year,
                    "authors": [
                        book.author.to_dict(rules=("-books",))
                        for book in publisher.books
                    ],
                },
                200,
            )


api.add_resource(PublisherByID, "/publishers/<int:id>")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
