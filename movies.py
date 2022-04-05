from flask import jsonify
from flask_restx import Resource, abort

from app import db
from app.models import Movie
from app.shcemas import MovieSchema
from views import view

movies_ns = view.namespace('movies')

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
