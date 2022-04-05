from flask import jsonify
from flask_restx import Resource, abort

from app import db
from app.models import Genre
from app.shcemas import GenreSchema
from views import view

genre_ns = view.namespace('genres')

genres_schema = GenreSchema(many=True)
genre_schema = GenreSchema()


@genre_ns.route("/")
class GenresView(Resource):
    def get(self):
        genres = db.session.query(Genre).all()
        return jsonify(genres_schema.dump(genres), 200)


@genre_ns.route("/<int:id>")
class GenreView(Resource):
    def get(self, id):
        genre = db.session.query(Genre).get(id)

        if genre is None:
            abort(404, "genre not found")

        return jsonify(genre_schema.dump(director), 200)
