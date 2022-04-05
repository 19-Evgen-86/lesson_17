from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    db.init_app(app)

    from views import view
    app.register_blueprint(view)

    return app
