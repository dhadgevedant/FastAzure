from sqlalchemy.orm import Session
import models
import schemas


def create_todo(db: Session, todo: schemas.TodoCreate):
    db_todo = models.Todo(
        title=todo.title,
        description=todo.description
    )

    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def get_todos(db: Session):
    return db.query(models.Todo).all()


def get_todo(db: Session, todo_id: int):
    return (
        db.query(models.Todo)
        .filter(models.Todo.id == todo_id)
        .first()
    )


def update_todo(
        db: Session,
        todo_id: int,
        todo: schemas.TodoUpdate
):
    db_todo = get_todo(db, todo_id)

    if not db_todo:
        return None

    update_data = todo.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_todo, key, value)

    db.commit()
    db.refresh(db_todo)

    return db_todo


def delete_todo(db: Session, todo_id: int):
    db_todo = get_todo(db, todo_id)

    if not db_todo:
        return None

    db.delete(db_todo)
    db.commit()

    return db_todo