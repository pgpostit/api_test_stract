from unittest.mock import MagicMock
from api.insights_processor import InsightsProcessor
from api.services import StractAPIService


def test_process_insights():
    mock_service = MagicMock(spec=StractAPIService)
    processor = InsightsProcessor(mock_service)

    mock_service.fetch_platforms.return_value = {
        "platforms": [{"value": "Facebook"}]}
    mock_service.fetch_accounts.return_value = [
        {"id": "123", "name": "Test Account", "token": "test_token"}]
    mock_service.fetch_fields.return_value = [
        {"value": "clicks"}, {"value": "spend"}]
    mock_service.fetch_insights.return_value = {
        "insights": [{"clicks": 10, "spend": 100}]}

    insights = processor.process_insights("Facebook")
    assert len(insights) == 1
    assert insights[0]["Platform"] == "Facebook"
    assert insights[0]["Account"] == "Test Account"
    assert insights[0]["clicks"] == 10
    assert insights[0]["spend"] == 100
