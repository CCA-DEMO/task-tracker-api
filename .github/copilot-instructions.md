# Task Tracker API — Copilot Instructions

## Project Context

This is a Python Flask REST API for task management. It uses Flask-SQLAlchemy with SQLite and pytest for testing.

## Code Style

- Use the `create_app()` factory pattern in `app.py` for all route definitions
- Return JSON responses using `jsonify` and model `to_dict()` methods
- Use standard HTTP status codes: 200, 201, 204, 400, 404
- Format errors as `{"error": "message"}`

## Adding Endpoints

When adding a new endpoint:
1. Add the route inside `create_app()` in `app.py`
2. Import `request` and `jsonify` from Flask as needed
3. Use `Task.query` for database operations
4. Call `db.session.commit()` after any writes
5. Update the endpoint table in `README.md`

## Adding Tests

- Create one test file per feature: `tests/test_<feature>.py`
- Always use this fixture pattern:
  ```python
  @pytest.fixture
  def client():
      app = create_app()
      app.config["TESTING"] = True
      app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
      with app.test_client() as client:
          yield client
  ```
- Test both happy path and error cases
- Name tests `test_<action>_<scenario>` (e.g., `test_delete_task_not_found`)

## Models

- All models live in `models.py` with a `to_dict()` serialization method
- Use `datetime.now(timezone.utc)` for timestamps
- The `Task` model has: id, title, description, status, created_at

## Do NOT

- Add blueprints — keep routes in `app.py` for now
- Add new dependencies without updating `requirements.txt`
- Modify `conftest.py` or `ci.yml` without being asked
