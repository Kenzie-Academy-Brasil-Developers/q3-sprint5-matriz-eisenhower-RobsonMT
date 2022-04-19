from app.configs.database import db
from app.models.category_model import Category
from sqlalchemy.orm.session import Session


def create_task_categories(task, task_categories) -> None:

    session: Session = db.session

    for item in task_categories:
        
        search = "{}".format(item.capitalize())

        category = session.query(Category).filter_by(name=search).first()

        if category:
            task.categories.append(category)
        
        else:
            new_category = Category(name=item)
            session.add(new_category)
            session.commit()
            
            category = session.query(Category).filter_by(name=search).first()
            task.categories.append(category)
