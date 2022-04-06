from flask import Flask
from flask_restx import Api

from app.config import Config
from app.migrate import migrate

from app.models import db
from views.directors import director_ns
from views.genres import genre_ns
from views.movies import movies_ns


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    return app


def register_extensions(app):
    with app.app_context():
        db.init_app(app)

        db.create_all()
        migrate()

        api = Api(app)
        api.add_namespace(director_ns)
        api.add_namespace(genre_ns)
        api.add_namespace(movies_ns)


app = create_app(Config)

if __name__ == '__main__':
    app.run()
