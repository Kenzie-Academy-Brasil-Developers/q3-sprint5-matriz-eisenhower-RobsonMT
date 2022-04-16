from http import HTTPStatus

from app.configs.database import db
from app.models.category_model import Category
from flask import jsonify, request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy.orm.session import Session


def create_category():
    data = request.get_json()
    session: Session = db.session

    try:
        category = Category(**data)
    except TypeError as err:
        return {"msg": f"key {err} should be string"}, HTTPStatus.UNPROCESSABLE_ENTITY

    try:
        session.add(category)
        session.commit()

        return jsonify(category), HTTPStatus.CREATED
    except IntegrityError:
        session.rollback()
        return {"msg": "category already exists!"}, HTTPStatus.CONFLICT


def update_category(id:int):
    data = request.get_json()
    session: Session = db.session

    try:
        category = Category.query.get(id)

        for key, value in data.items():
            setattr(category, key, value)

        session.commit()

        return jsonify(category), HTTPStatus.OK
    except AttributeError:
        session.rollback()
        return {"msg": "category not found!"}, HTTPStatus.NOT_FOUND
    except IntegrityError:
        session.rollback()
        return {"msg": "category already exists!"}, HTTPStatus.CONFLICT
    

def delete_category(id:int):
    session: Session = db.session
    category = Category.query.get(id)

    try:
        session.delete(category)
        session.commit()

        return "", HTTPStatus.NO_CONTENT
    except UnmappedInstanceError:
        session.rollback()
        return {"msg": "category not found!"}, HTTPStatus.NOT_FOUND
