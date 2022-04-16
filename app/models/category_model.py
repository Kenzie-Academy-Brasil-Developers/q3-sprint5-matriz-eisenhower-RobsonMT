from dataclasses import dataclass

from app.configs.database import db
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship, validates


@dataclass
class Category(db.Model):

    id: int
    name: str
    description: str

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)

    tasks = relationship("Task", secondary="tasks_categories", backref="categories")


    @validates("name")
    def validate_name(self, key, value):
       
        if value.__class__ != str:
            raise TypeError(key)

        return value.title()
       
        
    @validates("description")
    def validate_description(self, key, value):

        if value.__class__ != str:
            raise TypeError(key)

        return value.capitalize()

