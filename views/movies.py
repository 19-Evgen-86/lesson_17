from flask import jsonify, request, Blueprint
from flask_restx import Resource, abort, Api

from app import db
from app.models import Movie
from app.shcemas import MovieSchema

movies = Blueprint("movies", __name__, url_prefix="/api")
api = Api(movies)

movies_ns = api.namespace('movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movies_ns.route("/")
class MoviesApi(Resource):
    """
    класс для работы с коллекциями из БД
    """
    def get(self):
        """
         получаем все фильмы
        :return:
        """
        movies = db.session.query(Movie).all()
        return jsonify(movies_schema.dump(movies), 200)

    def post(self):
        """
        Добавляет данные о фильме в БД
        """
        try:
            # проверяем полученный JSON по схеме и создаем объект модели Movie
            movie_dict = Movie(**movie_schema.load(request.json))
            with db.session.begin():
                db.session.add(movie_dict)
            return jsonify({"message": "Add movie success"}, 200)

        except Exception as e:
            return jsonify({"error by insert": e.__repr__()}, 404)


@movies_ns.route("/<int:id>")
class MovieApi(Resource):
    """
    класс для работы с объектом из БД по ID
    """
    def get(self, id):
        """
        Получаем информацию о фильме по ID
        :param id:
        :return:
        """
        movie = db.session.query(Movie).filter(Movie.id == id).first()
        if movie is None:
            abort(404, " movie not found")
        return jsonify(movie_schema.dump(movie), 200)

    def put(self, id):
        """
        Обновляет данные о фильме  по запросу методом PUT
        :param id:
        :return:
        """
        try:
            movie_dict = movie_schema.load(request.json)
            with db.session.begin():
                db.session.query(Movie).filter(Movie.id == id).update(movie_dict)
            return jsonify({"message": "update(put) movie success"}, 200)

        except Exception as e:
            return jsonify({"error by put": e.__repr__()}, 404)

    def patch(self, id):
        """
             Обновляет данные о фильме по запросу методом PATCH
             :param id:
             :return:
        """
        try:
            movie_dict = movie_schema.load(request.json)
            with db.session.begin():
                db.session.query(Movie).filter(Movie.id == id).update(movie_dict)
            return jsonify({"message": "update(patch) movie success"}, 200)

        except Exception as e:
            return jsonify({"error by patch": e.__repr__()}, 404)

    def delete(self, id):
        """
        Удаляет фильм по ID
        :param id:
        :return:
        """

        try:
            with db.session.begin():
                db.session.query(Movie).filter(Movie.id == id).delete()
            return jsonify({"message": "delete movie success"}, 200)

        except Exception as e:
            return jsonify({"error by delete": e.__repr__()}, 404)
