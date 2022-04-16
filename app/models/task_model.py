from dataclasses import dataclass

from app.configs.database import db
from sqlalchemy import Column, ForeignKey, Integer, String, Text


@dataclass
class Task(db.Model):

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    duration = Column(Integer)
    importance = Column(Integer)
    urgency = Column(Integer)
    eisenhower_id = Column(Integer, ForeignKey("eisenhowers.id"), nullable=False)
