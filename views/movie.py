from flask import Blueprint, request, jsonify
from flask_restx import Api, Resource, abort

from app.models import Movie, Director, Genre
from app.shcemas import GenreSchema, DirectorSchema, MovieSchema
from app import db

movies = Blueprint("movies", __name__, url_prefix="/movies/api")

movies_api = Api(movies)
movies_ns = movies_api.namespace('movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movies_ns.route("/")
class MoviesView(Resource):
    def get(self):
        movies = db.session.query(Movie).all()
        return jsonify(movies_schema.dump(movies), 200)


@movies_ns.route("/<int:id>")
class MovieView(Resource):
    def get(self, id):
        movie = db.session.query(Movie).filter(Movie.id == id).first()
        if movie is None:
            abort(404, " movie not found")
        return jsonify(movie_schema.dump(movie), 200)


@movies_ns.route("/directors/<int:id>")
class MovieByDirectorView(Resource):
    def get(self, id):
        movies = db.session.query(Movie).filter(Movie.director_id == id).all()
        director = db.session.query(Director).filter(Director.id == id).first()

        if director is None:
            abort(404, "director not found")

        return jsonify(movies_schema.dump(movies), 200)


@movies_ns.route("/genres/<int:id>")
class MovieByGenreView(Resource):
    def get(self, id):
        movies = db.session.query(Movie).filter(Movie.genre_id == id).all()
        genre = db.session.query(Genre).filter(Genre.id == id).first()

        if genre is None:
            abort(404, "genre not found")

        return jsonify(movies_schema.dump(movies), 200)
