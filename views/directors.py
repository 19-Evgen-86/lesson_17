from flask import jsonify, request
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
        """
        получаем всеx режиссеров
        :return:
        """
        directors = db.session.query(Director.name).all()
        return jsonify(directors_schema.dump(directors), 200)

    def post(self):
        """
        Добавляет данные о режиссере в БД
        """
        try:
            # проверяем полученный JSON по схеме и создаем объект модели Movie
            director_dict = Director(**directors_schema.load(request.json))
            with db.session.begin():
                db.session.add(director_dict)
            return jsonify({"message": "Add director success"}, 200)

        except Exception as e:
            return jsonify({"error by insert": e.__repr__()}, 404)


@director_ns.route("/<int:id>")
class DirectorView(Resource):
    def get(self, id):
        """
        Получаем информацию о режиссере по ID
        :param id:
        :return:
        """

        director = db.session.query(Director.name).get(id)

        if director is None:
            abort(404, "director not found")

        return jsonify(directors_schema.dump(director), 200)

    def put(self, id):
        """
        Обновляет данные о режиссере  по запросу методом PUT
        :param id:
        :return:
        """
        try:
            director_dict = director_schema.load(request.json)
            with db.session.begin():
                db.session.query(Director).filter(Director.id == id).update(director_dict)
            return jsonify({"message": "update(put) movie success"}, 200)

        except Exception as e:
            return jsonify({"error by put": e.__repr__()}, 404)

    def patch(self, id):
        """
             Обновляет данные о режиссере по запросу методом PATCH
             :param id:
             :return:
        """
        try:
            director_dict = director_schema.load(request.json)
            with db.session.begin():
                db.session.query(Director).filter(Director.id == id).update(director_dict)
            return jsonify({"message": "update(patch) movie success"}, 200)

        except Exception as e:
            return jsonify({"error by patch": e.__repr__()}, 404)

    def delete(self, id):
        """
        Удаляет режиссера по ID
        :param id:
        :return:
        """

        try:
            with db.session.begin():
                db.session.query(Director).filter(Director.id == id).delete()
            return jsonify({"message": "delete movie success"}, 200)

        except Exception as e:
            return jsonify({"error by delete": e.__repr__()}, 404)
