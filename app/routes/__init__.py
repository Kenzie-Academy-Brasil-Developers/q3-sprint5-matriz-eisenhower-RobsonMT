from flask import Blueprint, Flask

from .category_blueprint import bp_category
from .task_blueprint import bp_task

bp_api = Blueprint("api", __name__, url_prefix="/api")


def init_app(app: Flask):
    bp_api.register_blueprint(bp_category)
    bp_api.register_blueprint(bp_task)
 
    app.register_blueprint(bp_api)
