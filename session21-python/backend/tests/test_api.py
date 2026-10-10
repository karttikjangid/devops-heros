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
    assert response.json()["service"] == "TaskBoard API"

def test_create_task_validation(client):
    response = client.post("/api/tasks", json={"title": "Deploy application", "priority": "HIGH", "assignee": "Student"})
    assert response.status_code == 201
    assert response.json()["title"] == "Deploy application"
