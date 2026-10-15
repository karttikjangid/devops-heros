import os
import pytest
import tempfile
from pathlib import Path
_test_dir = tempfile.TemporaryDirectory(prefix="session21-tests-")
os.environ["DATABASE_URL"] = "sqlite:///" + str(Path(_test_dir.name) / "test.db")

from fastapi.testclient import TestClient
from app.main import app
from app.db import Base, engine

@pytest.fixture(autouse=True)
def database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    # Each test uses its own clean SQLite tables.
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


def test_required_fields_cannot_be_set_to_null(client):
    task_id = client.post("/api/tasks", json={"title": "Keep valid data"}).json()["id"]
    for field in ["title", "description", "priority", "status", "assignee"]:
        assert client.put(f"/api/tasks/{task_id}", json={field: None}).status_code == 422
    assert client.get(f"/api/tasks/{task_id}").json()["title"] == "Keep valid data"


def test_assignment_details(client):
    payload = {"title": "Capstone", "session_number": 21, "due_date": "2026-10-31"}
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == 201
    task = response.json()
    assert task["session_number"] == 21
    assert task["due_date"] == "2026-10-31"
    cleared = client.put(f"/api/tasks/{task['id']}", json={"due_date": None})
    assert cleared.status_code == 200
    assert cleared.json()["due_date"] is None


def test_invalid_session_rejected(client):
    for session in [0, 22]:
        assert client.post("/api/tasks", json={"title": "Invalid", "session_number": session}).status_code == 422


def test_stats_and_missing_tasks(client):
    assert client.get("/api/tasks/stats").json() == {"total": 0, "todo": 0, "inProgress": 0, "done": 0}
    client.post("/api/tasks", json={"title": "Done", "status": "DONE"})
    assert client.get("/api/tasks/stats").json()["done"] == 1
    assert client.put("/api/tasks/99999", json={"status": "DONE"}).status_code == 404
    assert client.delete("/api/tasks/99999").status_code == 404


def test_readiness_and_metrics(client):
    assert client.get("/ready").json() == {"status": "READY"}
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text


def test_migration_preserves_existing_assignments(tmp_path):
    import sqlite3
    import subprocess
    import sys

    backend_dir = Path(__file__).resolve().parents[1]
    path = tmp_path / "migration.db"
    env = {**os.environ, "DATABASE_URL": f"sqlite:///{path}"}
    subprocess.run([sys.executable, "-m", "alembic", "upgrade", "0001_create_tasks"], env=env, cwd=backend_dir, check=True)
    with sqlite3.connect(path) as connection:
        connection.execute("INSERT INTO tasks (title, created_at) VALUES ('Existing homework', '2026-10-10 00:00:00')")
    subprocess.run([sys.executable, "-m", "alembic", "upgrade", "head"], env=env, cwd=backend_dir, check=True)
    with sqlite3.connect(path) as connection:
        assert connection.execute("SELECT title, session_number, due_date FROM tasks").fetchone() == ("Existing homework", None, None)
        assert connection.execute("SELECT version_num FROM alembic_version").fetchone()[0] == "0002_assignment_details"
