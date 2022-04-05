from flask import jsonify
from flask_restx import Resource, abort

from app import db
from app.models import Movie, Director
from app.shcemas import MovieSchema
from views import view

director_ns = view.namespace('directors')

movies_schema = MovieSchema(many=True)


@director_ns.route("/<int:id>")
class MovieByDirectorView(Resource):
    def get(self, id):
        movies = db.session.query(Movie).filter(Movie.director_id == id).all()
        director = db.session.query(Director).filter(Director.id == id).first()

        if director is None:
            abort(404, "director not found")

        return jsonify(movies_schema.dump(movies), 200)
