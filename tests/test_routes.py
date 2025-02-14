import pytest
from unittest.mock import patch
from api import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_route(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert "name" in data
    assert "email" in data
    assert "linkedin" in data


def test_get_platform_data(client):
    with patch("api.insights_processor.InsightsProcessor.process_insights", return_value=[{"Platform": "Facebook", "Account": "Test Account", "Clicks": 10}]):
        response = client.get("/Facebook")
        assert response.status_code == 200
        assert "Facebook.csv" in response.headers["Content-Disposition"]


def test_get_platform_summary(client):
    with patch("api.insights_processor.InsightsProcessor.process_insights", return_value=[{"Platform": "Facebook", "Account": "Test Account", "Clicks": 10}]):
        response = client.get("/Facebook/resumo")
        assert response.status_code == 200
        assert "Facebook_summary.csv" in response.headers["Content-Disposition"]


def test_get_general_data(client):
    with patch("api.insights_processor.InsightsProcessor.process_insights", return_value=[{"Platform": "Facebook", "Account": "Test Account", "Clicks": 10}]):
        response = client.get("/geral")
        assert response.status_code == 200
        assert "general.csv" in response.headers["Content-Disposition"]


def test_get_general_summary(client):
    with patch("api.insights_processor.InsightsProcessor.process_insights", return_value=[{"Platform": "Facebook", "Account": "Test Account", "Clicks": 10}]):
        response = client.get("/geral/resumo")
        assert response.status_code == 200
        assert "general_summary.csv" in response.headers["Content-Disposition"]
