from dataclasses import dataclass

from app.configs.database import db
from app.exceptions import AttributeTypeError
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import backref, relationship, validates


@dataclass
class Category(db.Model):

    id: int
    name: str
    description: str

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)

    tasks = relationship(
        "Task",
        secondary="tasks_categories", 
        backref=backref("categories", uselist=True)
    )


    @validates("name", "description")
    def validate_values(self, key, value):
       
        if value.__class__ != str:
            raise AttributeTypeError(key)

        return value.capitalize()
