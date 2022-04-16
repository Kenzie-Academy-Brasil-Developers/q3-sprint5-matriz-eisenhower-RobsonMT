from flask import Blueprint
from app.controllers import categorie_controller

bp_categories = Blueprint("categories", __name__, url_prefix="categories")

bp_categories.post("")(categorie_controller.create_category)
bp_categories.patch("/<int:id>")(categorie_controller.update_category)
bp_categories.delete("/<int:id>")(categorie_controller.delete_category)
