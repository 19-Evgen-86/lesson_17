from flask_restx import Api
from flask import Blueprint

views = Blueprint("views", __name__, url_prefix="/views")
view = Api(views)

from views import movies
from views import directors
from views import ganres
