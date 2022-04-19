from dataclasses import dataclass

from app.configs.database import db
from app.exceptions import AttributeTypeError, AttributeValueError
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import validates


@dataclass
class Task(db.Model):

    id: int
    name: str
    description: str
    duration: int
    importance: int
    urgency: int
    eisenhower_id: int

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    duration = Column(Integer)
    importance = Column(Integer)
    urgency = Column(Integer)
    eisenhower_id = Column(Integer, ForeignKey("eisenhowers.id"), nullable=False)

    @validates("importance", "urgency")
    def validade_importance_urgency(self, key, value):

        if value.__class__ != int:
            raise AttributeTypeError(key)

        if value < 1 or value > 2:
            raise AttributeValueError(key)

        return value

    @property
    def type(self):

        eisenhower_dict = {
            (1, 1): "Do It First",
            (1, 2): "Delegate It",
            (2, 1): "Schedule It",
            (2, 2): "Delete It",
        }

        return eisenhower_dict[self.importance, self.urgency]
