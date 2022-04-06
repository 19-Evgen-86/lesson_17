from flask import jsonify, request
from flask_restx import Resource, abort, Namespace

from app.models import Genre, db
from app.shcemas import GenreSchema

# genres = Blueprint("genres", __name__, url_prefix="/api")
genre_ns = Namespace('genres')

# genre_ns = api.namespace('genres')

genres_schema = GenreSchema(many=True)
genre_schema = GenreSchema()


@genre_ns.route("/")
class GenresView(Resource):
    def get(self):
        genres = db.session.query(Genre).all()
        return jsonify(genres_schema.dump(genres), 200)

    def post(self):
        """
        Добавляет данные о жанре в БД
        """
        try:
            # проверяем полученный JSON по схеме и создаем объект модели Movie
            genre_dict = Genre(**genre_schema.load(request.json))
            with db.session.begin():
                db.session.add(genre_dict)
            return jsonify({"message": "Add genre success"}, 200)

        except Exception as e:
            return jsonify({"error by insert": e.__repr__()}, 404)


@genre_ns.route("/<int:id>")
class GenreView(Resource):
    def get(self, id):
        genre = db.session.query(Genre).get(id)
        if genre is None:
            abort(404, "genre not found")
        return jsonify(genre_schema.dump(genre), 200)

    def put(self, id):
        try:
            genre_dict = genre_schema.load(request.json)
            with db.session.begin():
                db.session.query(Genre).filter(Genre.id == id).update(genre_dict)
            return jsonify({"message": "update(put) genre success"}, 200)

        except Exception as e:
            return jsonify({"error by put": e.__repr__()}, 404)

    def patch(self, id):

        try:
            genre_dict = genre_schema.load(request.json)
            with db.session.begin():
                db.session.query(Genre).filter(Genre.id == id).update(genre_dict)
            return jsonify({"message": "update(patch) genre success"}, 200)

        except Exception as e:
            return jsonify({"error by patch": e.__repr__()}, 404)

    def delete(self, id):
        try:
            with db.session.begin():
                db.session.query(Genre).filter(Genre.id == id).delete()
            return jsonify({"message": "delete genre success"}, 200)

        except Exception as e:
            return jsonify({"error by delete": e.__repr__()}, 404)
