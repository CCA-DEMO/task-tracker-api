"""Shared fixtures for browser-based end-to-end tests.

These tests exercise the real web UI in a browser via Playwright, so they need a
running instance of the Flask app. We boot the app in a background thread on a
free port using a temporary SQLite database, then point Playwright at it through
the ``base_url`` fixture (consumed automatically by pytest-playwright).
"""

import socket
import threading

import pytest
from werkzeug.serving import make_server

from app import create_app
from models import Task, db

# When the optional browser-test dependencies (pytest-playwright) are not
# installed -- e.g. in the lightweight unit-test CI job that runs plain `pytest`
# -- skip collecting the E2E specs instead of failing on the missing import.
try:
    import playwright  # noqa: F401
except ImportError:  # pragma: no cover
    collect_ignore_glob = ["*"]


def _free_port():
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


@pytest.fixture(scope="session")
def live_app(tmp_path_factory):
    db_path = tmp_path_factory.mktemp("e2e") / "e2e.db"
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
        }
    )
    port = _free_port()
    server = make_server("127.0.0.1", port, app, threaded=True)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield app, f"http://127.0.0.1:{port}"
    finally:
        server.shutdown()
        thread.join()


@pytest.fixture(scope="session")
def base_url(live_app):
    return live_app[1]


@pytest.fixture(autouse=True)
def _reset_db(live_app):
    """Start every test from an empty task list."""
    app = live_app[0]
    with app.app_context():
        Task.query.delete()
        db.session.commit()
    yield
