import requests
from typing import List, Dict, Any


class StractAPIService:
    BASE_URL = "https://sidebar.stract.to/api"

    def __init__(self):
        self.headers = {"Authorization": "ProcessoSeletivoStract2025"}

    def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        response = requests.get(
            f"{self.BASE_URL}/{endpoint}",
            params=params,
            headers=self.headers
        )
        return response.json()

    def _paginate(self, endpoint: str, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        data = []
        page = 1
        total_pages = 1

        while page <= total_pages:
            params["page"] = page
            response = self._make_request(endpoint, params)

            if "pagination" in response:
                total_pages = response["pagination"]["total"]

            data.extend(response.get(endpoint, []))
            page += 1

        return data

    def fetch_platforms(self) -> Dict[str, Any]:
        return self._make_request("platforms")

    def fetch_accounts(self, platform: str) -> List[Dict[str, Any]]:
        return self._paginate("accounts", {"platform": platform})

    def fetch_fields(self, platform: str) -> List[Dict[str, Any]]:
        return self._paginate("fields", {"platform": platform})

    def fetch_insights(self, platform: str, account_id: str, token: str, field_values: List[str]) -> Dict[str, Any]:
        return self._make_request(
            "insights",
            {
                "platform": platform,
                "account": account_id,
                "token": token,
                "fields": ",".join(field_values),
            }
        )
