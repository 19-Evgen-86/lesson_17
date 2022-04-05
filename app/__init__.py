from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    db.init_app(app)
    with app.app_context():
        from app import models
        from app.migrate import migrate
        from views import views
        # cоздаем БД
        db.create_all()
        # заносим данные
        migrate()
        # регистрируем Blueprint
        app.register_blueprint(views)

        return app
