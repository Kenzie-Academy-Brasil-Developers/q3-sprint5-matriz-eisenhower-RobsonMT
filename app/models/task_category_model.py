from dataclasses import dataclass

from app.configs.database import db
from sqlalchemy import Column, ForeignKey, Integer


@dataclass
class TaskCategory(db.Model):
    id: int
    task_id: int
    category_id: int

    __tablename__ = "tasks_categories"

    id = Column(Integer, primary_key=True, unique=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
