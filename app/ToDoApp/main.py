from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException,Depends,Path
import models
from models import Todos
from database import engine,SessionLocal
from starlette import status
from pydantic import BaseModel,Field

app = FastAPI()


models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency =  Annotated[Session,Depends(get_db)]

class TodoCreate(BaseModel):
    title: str = Field(max_length=200)
    priority: int = Field(gt=0, lt=4)
    completed: bool = Field(default=False)


class TodoUpdate(BaseModel):
    completed : bool 

@app.get("/all-todo/",status_code=status.HTTP_200_OK)
async def all_books(db: db_dependency):
    return db.query(Todos).all()



@app.get("/get-todo/{todo_id}",status_code=status.HTTP_200_OK)
async def get_todo(db: db_dependency, todo_id: int):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.post("/create-todo/", status_code=status.HTTP_201_CREATED)
async def create_todo(todo_in: TodoCreate, db: db_dependency):
    todo_model = Todos(**todo_in.model_dump())
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model


@app.post("/update-todo/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo(todo_id: int, todo_in: TodoUpdate, db: db_dependency):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.completed = todo_in.completed
    db.commit()
    db.refresh(todo)
    return todo


@app.delete("/delete-todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo( db: db_dependency,todo_id: int = Path(gt=0) ):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()