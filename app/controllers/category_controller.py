from http import HTTPStatus

from app.configs.database import db
from app.decorators import validate_fields
from app.exceptions import AttributeTypeError
from app.models.category_model import Category
from app.services import serialize_categories
from flask import jsonify, request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy.orm.session import Session

fields = ["name", "description"]

@validate_fields(fields, "description")
def post_category() -> dict:
    data = request.get_json()
    session: Session = db.session

    try:
        category = Category(**data)
    except AttributeTypeError as err:
        return {"msg": f"key {err} should be string"}, HTTPStatus.UNPROCESSABLE_ENTITY

    try:
        session.add(category)
        session.commit()

        return jsonify(category), HTTPStatus.CREATED
    except IntegrityError:
        session.rollback()
        return {"msg": "category already exists!"}, HTTPStatus.CONFLICT

    finally:
        session.close()

@validate_fields(fields, fields)
def patch_category(id: int) -> dict:
    data = request.get_json()
    session: Session = db.session

    try:
        category = session.query(Category).get(id)

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
    
    finally:
        session.close()
    

def delete_category(id: int) -> dict:
    session: Session = db.session
    category = session.query(Category).get(id)

    try:
        session.delete(category)
        session.commit()
        
        return "", HTTPStatus.NO_CONTENT
    except UnmappedInstanceError:
        session.rollback()
        return {"msg": "category not found!"}, HTTPStatus.NOT_FOUND

    finally:
        session.close()


def get_categories() -> dict:
    session: Session = db.session
    categories = session.query(Category).all()

    response = serialize_categories(categories)

    return jsonify(response), HTTPStatus.OK
