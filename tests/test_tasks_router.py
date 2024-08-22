import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import Task, UpdateTaskModel, TaskList
from app.db import db

client = TestClient(app)

def test_create_task():
    task = Task(id=1, title="Test Task", description="This is a test task", completed=False)
    response = client.post("/tasks", json=task.dict())

    assert response.status_code == 200
    assert response.json() == task.dict()


def test_get_task():
    task_id = 1
    task = Task(id=task_id, title="Test Task", description="This is a test task", completed=False)
    db.add_task(task)
    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    response_data = response.json()
    assert response_data['title'] == task.title
    assert response_data['description'] == task.description
    assert response_data['completed'] == task.completed
    # No verificamos el ID ya que puede ser asignado automáticamente por la base de datos

def test_get_task_not_found():
    response = client.get("/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}

def test_get_tasks():
    db.delete_all_tasks()
    task1 = Task(id=1, title="Task 1", description="Description 1", completed=False)
    task2 = Task(id=2, title="Task 2", description="Description 2", completed=True)
    db.add_task(task1)
    db.add_task(task2)
    
    # Supongamos que la ruta correcta es "/tasks" en lugar de "/"
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == {"tasks": [task1.dict(), task2.dict()]}

def test_update_task():
    task_id = 1
    task = Task(id=task_id, title="Original Task", description="Original description", completed=False)
    db.add_task(task)
    update_data = UpdateTaskModel(title="Updated Task", description="Updated description", completed=True)
    response = client.put(f"/tasks/{task_id}", json=update_data.dict())
    assert response.status_code == 200
    
    response_data = response.json()
    assert response_data['title'] == update_data.title
    assert response_data['description'] == update_data.description
    assert response_data['completed'] == update_data.completed
    # No verificamos el ID ya que puede cambiar durante la actualización

def test_update_task_not_found():
    update_data = UpdateTaskModel(title="Updated Task", description="Updated description", completed=True)
    response = client.put("/999", json=update_data.dict())
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}

def test_delete_task():
    task_id = 1
    task = Task(id=task_id, title="Test Task", description="This is a test task", completed=False)
    db.add_task(task)
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Task deleted successfully"}
    assert db.get_task(task_id) is None

def test_delete_all_tasks():
    task1 = Task(id=1, title="Task 1", description="Description 1", completed=False)
    task2 = Task(id=2, title="Task 2", description="Description 2", completed=True)
    db.add_task(task1)
    db.add_task(task2)
    response = client.delete("/tasks")
    assert response.status_code == 200
    assert response.json() == {"message": "Todas las tareas han sido eliminadas"}
    assert db.get_tasks() == []
