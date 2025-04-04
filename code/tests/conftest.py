# conftest.py
import os
import pytest

GUNICORN_PORT = os.environ.get("GUNICORN_PORT", 5000)
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN', None)


@pytest.fixture(scope="module")
def validate_environment():
    assert ACCESS_TOKEN, "ACCESS_TOKEN environment variable is not set."
    assert GUNICORN_PORT, "GUNICORN_PORT environment variable is not set."


@pytest.fixture(scope="module")
def api_url():
    return f'http://127.0.0.1:{GUNICORN_PORT}'


@pytest.fixture(scope="function")
def headers():
    return {"Authorization": f"Bearer {ACCESS_TOKEN}"}
