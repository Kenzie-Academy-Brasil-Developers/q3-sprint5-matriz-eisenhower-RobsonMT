from flask import Flask, Blueprint
from .categorie_blueprint import bp_categories

bp_api = Blueprint("api", __name__, url_prefix="/api")


def init_app(app: Flask):
    bp_api.register_blueprint(bp_categories)

    app.register_blueprint(bp_api)
