from flask import Blueprint
from app.controllers import category_controller

bp_category = Blueprint("categories", __name__)

bp_category.get("/")(category_controller.get_categories)
bp_category.post("/categories")(category_controller.post_category)
bp_category.patch("categories/<int:id>")(category_controller.patch_category)
bp_category.delete("categories/<int:id>")(category_controller.delete_category)