from flask import Flask

from app.migrate import migrate
from app.models import db, create_db
from views.genres import genres
from views.movies import movies
from views.directors import directors


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    db.init_app(app)
    with app.app_context():
        create_db()
        migrate()
        app.register_blueprint(directors)
        app.register_blueprint(genres)
        app.register_blueprint(movies)
    return app
