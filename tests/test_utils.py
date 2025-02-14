
from api.utils import normalize_data, summarize_data, generate_csv
from flask import Response


def test_normalize_data():
    raw_data = [{"adName": "Ad Test", "cost": 100, "clicks": 10}]
    result = normalize_data(raw_data)
    assert result[0]["ad_name"] == "Ad Test"
    assert result[0]["spend"] == 100
    assert result[0]["cpc"] == 10


def test_summarize_data():
    raw_data = [
        {"Platform": "Facebook", "Account": "Test Account", "Clicks": 10},
        {"Platform": "Facebook", "Account": "Test Account", "Clicks": 20}
    ]
    result = summarize_data(raw_data)
    assert len(result) == 1
    assert result[0]["Clicks"] == 30


def test_generate_csv():
    data = [{"Platform": "Facebook", "Account": "Test Account", "Clicks": 10}]
    response = generate_csv(data, "test.csv")
    assert isinstance(response, Response)
    assert response.status_code == 200
    assert "test.csv" in response.headers["Content-Disposition"]
