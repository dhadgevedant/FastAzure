from fastapi import FastAPI, HTTPException
from schemas import TodoCreate, TodoResponse
from sqs_service import send_todo_created_event

app = FastAPI(
    title="Todo API with AWS SQS"
)

todos = []


@app.get("/")
def home():
    return {
        "message": "Todo API Running"
    }


@app.get("/todos")
def get_todos():
    return todos


@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            return todo

    raise HTTPException(
        status_code=404,
        detail="Todo not found"
    )


@app.post(
    "/todos",
    response_model=TodoResponse
)
def create_todo(todo: TodoCreate):

    new_todo = {
        "id": len(todos) + 1,
        "title": todo.title,
        "description": todo.description,
        "completed": False
    }

    todos.append(new_todo)

    try:
        send_todo_created_event(
            new_todo
        )
    except Exception as e:
        print("SQS Error:", e)

    return new_todo


@app.put("/todos/{todo_id}")
def update_todo(
        todo_id: int,
        todo: TodoCreate
):
    for item in todos:
        if item["id"] == todo_id:
            item["title"] = todo.title
            item["description"] = (
                todo.description
            )

            return item

    raise HTTPException(
        status_code=404,
        detail="Todo not found"
    )


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):

    for todo in todos:
        if todo["id"] == todo_id:
            todos.remove(todo)

            return {
                "message": "Deleted"
            }

    raise HTTPException(
        status_code=404,
        detail="Todo not found"
    )