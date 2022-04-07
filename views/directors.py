from flask import jsonify, request
from flask_restx import Resource, abort, Namespace

from app.models import Director, db
from app.shcemas import DirectorSchema

# directors = Blueprint("directors", __name__, url_prefix="/api")
director_ns = Namespace('directors')

# director_ns = api.namespace('directors')
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
        return directors_schema.dump(directors), 200

    def post(self):
        """
        Добавляет данные о режиссере в БД
        """
        try:
            # проверяем полученный JSON по схеме и создаем объект модели Movie
            director_dict = Director(**directors_schema.load(request.json))
            with db.session.begin():
                db.session.add(director_dict)
            return {"message": "Add director success"}, 200

        except Exception as e:
            return {"error by insert": e.__repr__()}, 404


@director_ns.route("/<int:id>")
class DirectorView(Resource):
    def get(self, id):
        """
        Получаем информацию о режиссере по ID
        :param id:
        :return:
        """
        director = db.session.query(Director).get(id)
        if director is None:
            abort(404, "director not found")

        return director_schema.dump(director), 200

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
            return {"message": "update(put) director success"}, 200

        except Exception as e:
            return {"error by put": e.__repr__()}, 404

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
            return jsonify({"message": "update(patch) director success"}, 200)

        except Exception as e:
            return {"error by patch": e.__repr__()}, 404

    def delete(self, id):
        """
        Удаляет режиссера по ID
        :param id:
        :return:
        """

        try:
            with db.session.begin():
                db.session.query(Director).filter(Director.id == id).delete()
            return {"message": "delete director success"}, 200

        except Exception as e:
            return {"error by delete": e.__repr__()}, 404
