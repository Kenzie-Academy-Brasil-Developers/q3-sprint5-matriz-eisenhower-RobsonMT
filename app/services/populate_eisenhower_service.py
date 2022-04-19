from app.configs.database import db
from app.models.eisenhower_model import Eisenhower
from sqlalchemy.orm.session import Session


def populate_eisenhower() -> None:
    session: Session = db.session
    classifications = ["Do It First", "Delegate It", "Schedule It", "Delete It"]
    eisenhowers = session.query(Eisenhower).all()

    new_eisenhowers_list = []

    if not eisenhowers:
        for type in classifications:
            new_eisenhower = Eisenhower(**{"type":type})
            new_eisenhowers_list.append(new_eisenhower)

        session.add_all(new_eisenhowers_list)
        session.commit()
