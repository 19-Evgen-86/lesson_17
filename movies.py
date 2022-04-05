from flask import jsonify, request
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

    def post(self):
        movie = MovieSchema.load(request.json)
        movie_dict = Movie(**movie)
        with db.session.begin():
            db.session.add(movie_dict)


@movies_ns.route("/<int:id>")
class MovieView(Resource):
    def get(self, id):
        movie = db.session.query(Movie).filter(Movie.id == id).first()
        if movie is None:
            abort(404, " movie not found")
        return jsonify(movie_schema.dump(movie), 200)

    def put(self, id):
        movie = MovieSchema.load(request.json)
        with db.session.begin():
            db.session.query(Movie).filter(Movie.id == id).update(movie)

    def delete(self, id):
        with db.session.begin():
            db.session.query(Movie).filter(Movie.id == id).delete()
