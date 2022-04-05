from flask import jsonify
from flask_restx import Resource, abort

from app import db
from app.models import Director
from app.shcemas import DirectorSchema
from views import view

director_ns = view.namespace('directors')

directors_schema = DirectorSchema(many=True)
director_schema = DirectorSchema()


@director_ns.route("/")
class DirectorsView(Resource):
    def get(self):
        directors = db.session.query(Director).all()
        return jsonify(directors_schema.dump(directors), 200)


@director_ns.route("/<int:id>")
class DirectorView(Resource):
    def get(self, id):
        director = db.session.query(Director).get(id)

        if director is None:
            abort(404, "director not found")

        return jsonify(directors_schema.dump(director), 200)
