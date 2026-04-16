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
| GET | `/health` | Health check |
| GET | `/tasks` | List all tasks |

## Running Tests

```bash
pytest
```
