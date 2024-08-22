"""
Provides an API router for managing tasks.

The `tasks_router` is an instance of `APIRouter` that defines the following endpoints:

- `POST /`: Creates a new task.
- `GET /{task_id}`: Retrieves a task by its ID.
- `GET /`: Retrieves a list of all tasks.
- `PUT /{task_id}`: Updates a task by its ID.
- `DELETE /{task_id}`: Deletes a task by its ID.
- `DELETE /`: Deletes all tasks.

The router uses the `db` module to interact with the task data store.
"""

"""
Este módulo proporciona un enrutador API para gestionar tareas.
Define endpoints para crear, leer, actualizar y eliminar tareas.
"""

from fastapi import APIRouter, HTTPException, Path, Body
from app.models import Task, UpdateTaskModel, TaskList
from app.db import db

tasks_router = APIRouter()

# Crea una nueva tarea
@tasks_router.post("/", response_model=Task)
async def create_task(task: Task = Body(..., example={"title": "New Task", "description": "Task description", "completed": False})):
    return db.add_task(task)

# Obtiene una tarea específica por su ID
@tasks_router.get("/{task_id}", response_model=Task)
async def get_task(task_id: int = Path(..., gt=0)):
    task = db.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return task

# Obtiene todas las tareas
@tasks_router.get("/", response_model=TaskList)
async def get_tasks():
    tasks = db.get_tasks()
    return TaskList(tasks=tasks)

# Actualiza una tarea existente
@tasks_router.put("/{task_id}", response_model=Task)
async def update_task(
    task_id: int = Path(..., gt=0),
    task_update: UpdateTaskModel = Body(..., example={"title": "Updated Task", "description": "Updated description", "completed": True})
):
    updated_task = db.update_task(task_id, task_update)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return updated_task

# Elimina una tarea específica
@tasks_router.delete("/{task_id}")
async def delete_task(task_id: int = Path(..., gt=0)):
    db.delete_task(task_id)
    return {"message": "Task deleted successfully"}

# Elimina todas las tareas
@tasks_router.delete("/")
async def delete_all_tasks():
    db.delete_all_tasks()
    return {"message": "Todas las tareas han sido eliminadas"}
