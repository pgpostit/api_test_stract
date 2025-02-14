import pytest


@pytest.fixture(scope="session")
def client():
    from api import create_app
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
