from flask import jsonify
from flask_restx import Resource, abort

from app import db
from app.models import Movie, Genre
from app.shcemas import MovieSchema
from views import view

genre_ns = view.namespace('genres')
movies_schema = MovieSchema(many=True)


@genre_ns.route("/<int:id>")
class MovieByGenreView(Resource):
    def get(self, id):
        movies = db.session.query(Movie).filter(Movie.genre_id == id).all()
        genre = db.session.query(Genre).filter(Genre.id == id).first()

        if genre is None:
            abort(404, "genre not found")

        return jsonify(movies_schema.dump(movies), 200)
