from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# User input
class TaskIn(BaseModel):
    title: str


# You never want the client to be able to
# set the id or the done field on creation,
# so you use a separate input model that
# doesn't expose those fields.
class Task(BaseModel):
    id: UUID
    title: str
    done: bool = False


# in-memory database, lives as long as process
# runs (real app would use PostgreSQL)
db: list[Task] = []


# ==============================
# API ENDPOINTS
# ==============================
@app.post("/tasks", response_model=Task, status_code=201)
def create_task(payload: TaskIn):
    task = Task(id=uuid4(), title=payload.title)
    db.append(task)
    return task


@app.get("/tasks", response_model=list[Task])
def list_tasks():
    return db


@app.patch("/tasks/{task_id}/complete", response_model=Task)
def complete_task(task_id: UUID):
    for task in db:
        if task.id == task_id:  #  if the client sends a non-UUID string, FastAPI
            # returns a 422 error before function is called.
            task.done = True
            return task
    raise HTTPException(status_code=404, detail="Task not found")
