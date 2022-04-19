from http import HTTPStatus

from app.configs.database import db
from app.decorators import validate_fields
from app.exceptions import AttributeTypeError, AttributeValueError
from app.models.eisenhower_model import Eisenhower
from app.models.task_model import Task
from app.services import create_task_categories, populate_eisenhower
from flask import jsonify, request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import Session

fields = ["name", "description", "duration", "importance", "urgency", "categories"]


@validate_fields(fields, "description")
def post_task() -> dict:
    data = request.get_json()
    session: Session = db.session

    populate_eisenhower()

    try:
        task_categories = data.pop("categories")

        task = Task(**data)
            
        eisenhower = session.query(Eisenhower).filter_by(type=task.type).first()

        task.eisenhower_id = eisenhower.id

        create_task_categories(task, task_categories)

        session.add(task)
        session.commit()

        return jsonify({
            "id": task.id,
            "name": task.name,
            "description": task.description,
            "duration": task.duration,
            "classification": eisenhower.type,
            "categories": [category.name for category in task.categories]
        }), HTTPStatus.CREATED

    except AttributeTypeError as err:
        session.rollback()
        return {"msg": f"key `{err.args[0]}` must be an integer!."}, HTTPStatus.UNPROCESSABLE_ENTITY

    except AttributeValueError as err:
        session.rollback()
        return {"msg": f"{err.args[0]} expected value 1 or 2!."}, HTTPStatus.UNPROCESSABLE_ENTITY

    except IntegrityError:
        session.rollback()
        return jsonify({"msg": f"name: {data['name']}; already registered"}), HTTPStatus.CONFLICT

    finally:
        session.close()
    


@validate_fields(fields, fields)
def patch_task(id: int) -> dict:
    data  = request.get_json()
    session: Session = db.session

    try:
        task = session.query(Task).get(id)
        
        if not task:
            return {"msg": "task not found!"}, HTTPStatus.NOT_FOUND

        for key, value in data.items():
            setattr(task, key, value)

        eisenhower = session.query(Eisenhower).filter_by(type=task.type).first()
        task.eisenhower_id = eisenhower.id
        
        session.add(task)
        session.commit()

        return jsonify({
            "id": task.id,
            "name": task.name,
            "description": task.description,
            "duration": task.duration,
            "classification": eisenhower.type,
            "categories": [category.name for category in task.categories]
        }), HTTPStatus.OK

    except AttributeTypeError as err:
        session.rollback()
        return {"msg": f"key `{err.args[0]}` must be an integer!."}, HTTPStatus.UNPROCESSABLE_ENTITY

    except AttributeValueError as err:
        session.rollback()
        return {"msg": f"{err.args[0]} expected value 1 or 2!."}, HTTPStatus.UNPROCESSABLE_ENTITY

    except IntegrityError:
        session.rollback()
        return jsonify({"msg": f"name: {data['name']}; already registered"}), HTTPStatus.CONFLICT
    
    finally:
        session.close()
        

def delete_task(id: int) -> dict:
    session: Session = db.session
    task = session.query(Task).get(id)

    if not task:
        return {"msg": "task not found!"}, HTTPStatus.NOT_FOUND

    session.delete(task)
    session.commit()

    return "", HTTPStatus.NO_CONTENT
