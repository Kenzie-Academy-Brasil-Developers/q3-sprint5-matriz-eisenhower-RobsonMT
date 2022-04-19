from flask import Blueprint
from app.controllers import task_controller

bp_task = Blueprint("tasks", __name__, url_prefix="tasks")

bp_task.post("")(task_controller.post_task)
bp_task.patch("/<int:id>")(task_controller.patch_task)
bp_task.delete("/<int:id>")(task_controller.delete_task)

