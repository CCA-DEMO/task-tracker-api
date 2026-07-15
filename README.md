# Task Tracker API

A lightweight task tracking REST API built with Python and Flask.

## Quick Start

```bash
pip install -r requirements.txt
python app.py
```

The API runs at `http://localhost:5000`.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Web UI (task list + create form) |
| GET | `/health` | Health check |
| GET | `/tasks` | List all tasks |
| POST | `/tasks` | Create a new task |

## Web UI

A minimal browser UI is served at `http://localhost:5000/`. It lists tasks and
lets you create new ones, talking to the JSON API via `fetch`.

## Running Tests

```bash
pytest
```

## Browser Tests (E2E)

Browser-based end-to-end tests for the web UI use Playwright:

```bash
pip install -r requirements-e2e.txt
playwright install chromium
pytest tests/e2e -v
```

These are maintained by the repo-centric `ui-tester` agent. See
[`docs/ui-testing-agent.md`](docs/ui-testing-agent.md) for how the agent, CI, and
project board fit together.
