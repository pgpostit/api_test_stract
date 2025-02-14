from unittest.mock import patch
from api.services import StractAPIService


def test_fetch_platforms():
    mock_service = StractAPIService()
    with patch.object(mock_service, "_make_request", return_value={"platforms": [{"value": "Facebook"}]}):
        platforms = mock_service.fetch_platforms()
        assert "platforms" in platforms
        assert platforms["platforms"][0]["value"] == "Facebook"


def test_fetch_accounts():
    mock_service = StractAPIService()
    with patch.object(mock_service, "_paginate", return_value=[{"id": "123", "name": "Test Account"}]) as mock_paginate:
        accounts = mock_service.fetch_accounts("Facebook")
        assert len(accounts) == 1
        assert accounts[0]["name"] == "Test Account"
        mock_paginate.assert_called_once_with(
            "accounts", {"platform": "Facebook"})


def test_fetch_fields():
    mock_service = StractAPIService()
    with patch.object(mock_service, "_paginate", return_value=[{"value": "clicks"}, {"value": "spend"}]) as mock_paginate:
        fields = mock_service.fetch_fields("Facebook")
        assert len(fields) == 2
        assert fields[0]["value"] == "clicks"
        assert fields[1]["value"] == "spend"
        mock_paginate.assert_called_once_with(
            "fields", {"platform": "Facebook"})


def test_fetch_insights():
    mock_service = StractAPIService()
    with patch.object(mock_service, "_make_request", return_value={"insights": [{"clicks": 100, "spend": 200}]}) as mock_request:
        insights = mock_service.fetch_insights(
            "Facebook", "123", "test_token", ["clicks", "spend"])
        assert "insights" in insights
        assert insights["insights"][0]["clicks"] == 100
        assert insights["insights"][0]["spend"] == 200
        mock_request.assert_called_once_with(
            "insights", {
                "platform": "Facebook",
                "account": "123",
                "token": "test_token",
                "fields": "clicks,spend"
            }
        )
