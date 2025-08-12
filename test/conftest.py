import pytest

from src.memoryvault.app import create_app


@pytest.fixture
def app_client():
    app = create_app()
    app.config.update({"TESTING": True})

    with app.test_client() as client:
        yield app, client
