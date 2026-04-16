import pytest
from app import create_app
from models import db, Task


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as client:
        yield client


def test_get_tasks_empty(client):
    resp = client.get("/tasks")
    assert resp.status_code == 200
    assert resp.json == []


def test_get_tasks_returns_all(client):
    # Create tasks via the database directly
    app = client.application
    with app.app_context():
        task1 = Task(title="Task 1", description="First task")
        task2 = Task(title="Task 2", description="Second task")
        db.session.add(task1)
        db.session.add(task2)
        db.session.commit()

    resp = client.get("/tasks")
    assert resp.status_code == 200
    data = resp.json
    assert len(data) == 2
    assert data[0]["title"] == "Task 1"
    assert data[1]["title"] == "Task 2"
    for task in data:
        assert "id" in task
        assert "title" in task
        assert "description" in task
        assert "status" in task
        assert "created_at" in task
