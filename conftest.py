"""Configure Test"""
import pytest
from flask.testing import FlaskClient

from api import app

@pytest.fixture()
def api_client() -> FlaskClient:
    """Returns a version of the API for testing."""
    return app.test_client()
