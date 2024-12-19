from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from adapter.sqllite_apapter import get_db, Task


# Инициализация FastAPI
app = FastAPI()


# Модель Pydantic для данных от пользователя
class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False

class TaskResponse(TaskCreate):
    id: int

    class Config:
        orm_mode = True


# Создать todo
@app.post("/items", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# Получить все todo 
@app.get("/items", response_model=list[TaskResponse])
def read_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks

# Получить todo по id
@app.get("/items/{item_id}", response_model=TaskResponse)
def read_task(item_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == item_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Изменить todo
@app.put("/items/{item_id}", response_model=TaskResponse)
def update_task(item_id: int, task_data: TaskCreate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == item_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task_data.dict().items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

# Удалить todo
@app.delete("/items/{item_id}", response_model=dict)
def delete_task(item_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == item_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}
