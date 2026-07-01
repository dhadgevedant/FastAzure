from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
import crud
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="To-Do API",
    description="Simple CRUD API using FastAPI and Pydantic",
    version="1.0.0"
)


@app.get("/")
def home():
    return {"message": "Welcome to the To-Do API"}


@app.post(
    "/todos",
    response_model=schemas.TodoResponse,
    status_code=201
)
def create_todo(
        todo: schemas.TodoCreate,
        db: Session = Depends(get_db)
):
    return crud.create_todo(db, todo)


@app.get(
    "/todos",
    response_model=list[schemas.TodoResponse]
)
def get_todos(
        db: Session = Depends(get_db)
):
    return crud.get_todos(db)


@app.get(
    "/todos/{todo_id}",
    response_model=schemas.TodoResponse
)
def get_todo(
        todo_id: int,
        db: Session = Depends(get_db)
):
    todo = crud.get_todo(db, todo_id)

    if not todo:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    return todo


@app.put(
    "/todos/{todo_id}",
    response_model=schemas.TodoResponse
)
def update_todo(
        todo_id: int,
        todo: schemas.TodoUpdate,
        db: Session = Depends(get_db)
):
    updated = crud.update_todo(
        db,
        todo_id,
        todo
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    return updated


@app.delete("/todos/{todo_id}")
def delete_todo(
        todo_id: int,
        db: Session = Depends(get_db)
):
    deleted = crud.delete_todo(
        db,
        todo_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    return {
        "message": "Todo deleted successfully"
    }