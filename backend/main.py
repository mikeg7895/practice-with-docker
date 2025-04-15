from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "postgresql://postgres:lNf0Bqf1Po47pBBm1JgF@database-1.czmsk6ei6chk.us-east-2.rds.amazonaws.com/tasks"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class TaskDB(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    completed = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)

class Task(BaseModel):
    id: int
    title: str
    description: str
    completed: bool = False

    class Config:
        orm_mode = True 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def index():
    return {"message": "Hello hadrisson"}

# Endpoint para obtener todas las tareas
@app.get("/tasks", response_model=List[Task])
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(TaskDB).all()
    return tasks

# Endpoint para obtener una tarea por su ID
@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Endpoint para crear una nueva tarea
@app.post("/tasks", response_model=Task)
def create_task(task: Task, db: Session = Depends(get_db)):
    # Validar que no exista una tarea con el mismo ID
    if db.query(TaskDB).filter(TaskDB.id == task.id).first():
        raise HTTPException(status_code=400, detail="Task with this ID already exists")
    new_task = TaskDB(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# Endpoint para actualizar una tarea existente
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.title = updated_task.title
    task.description = updated_task.description
    task.completed = updated_task.completed
    db.commit()
    db.refresh(task)
    return task

# Endpoint para eliminar una tarea
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}
