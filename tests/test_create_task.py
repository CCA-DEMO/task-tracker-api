import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    with app.test_client() as client:
        yield client


def test_create_task_success(client):
    resp = client.post("/tasks", json={"title": "New Task", "description": "A description"})
    assert resp.status_code == 201
    data = resp.json
    assert data["title"] == "New Task"
    assert data["description"] == "A description"
    assert data["status"] == "todo"
    assert "id" in data
    assert "created_at" in data


def test_create_task_missing_title(client):
    resp = client.post("/tasks", json={"description": "No title"})
    assert resp.status_code == 400
    assert "error" in resp.json


def test_create_task_description_defaults_to_empty(client):
    resp = client.post("/tasks", json={"title": "Only Title"})
    assert resp.status_code == 201
    assert resp.json["description"] == ""
