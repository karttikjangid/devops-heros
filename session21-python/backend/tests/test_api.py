import os
import pytest
import tempfile
from pathlib import Path
_test_dir = tempfile.TemporaryDirectory(prefix="session21-tests-")
os.environ["DATABASE_URL"] = "sqlite:///" + str(Path(_test_dir.name) / "test.db")

from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    # Enter the context so startup creates the schema before requests.
    with TestClient(app) as client:
        yield client

def test_health(client):
    assert client.get("/health").json() == {"status": "UP"}

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "Homework Tracker API"

def test_create_task_validation(client):
    response = client.post("/api/tasks", json={"title": "Deploy application", "priority": "HIGH", "assignee": "Student"})
    assert response.status_code == 201
    assert response.json()["title"] == "Deploy application"


def test_empty_title_rejected(client):
    response = client.post("/api/tasks", json={"title": ""})
    assert response.status_code == 422


def test_task_lifecycle(client):
    created = client.post("/api/tasks", json={"title": "Finish Session 21"})
    assert created.status_code == 201
    task_id = created.json()["id"]
    assert client.get(f"/api/tasks/{task_id}").json()["title"] == "Finish Session 21"
    updated = client.put(f"/api/tasks/{task_id}", json={"status": "DONE"})
    assert updated.status_code == 200
    assert updated.json()["status"] == "DONE"
    assert client.delete(f"/api/tasks/{task_id}").status_code == 204
    assert client.get(f"/api/tasks/{task_id}").status_code == 404
