import requests


class StractAPIService:
    BASE_URL = "https://sidebar.stract.to/api"

    def __init__(self):
        self.headers = {"Authorization": "ProcessoSeletivoStract2025"}

    def _fetch_paginated_data(self, endpoint, params):
        data = []
        page = 1
        total_pages = 1

        while page <= total_pages:
            params["page"] = page
            response = requests.get(
                f"{self.BASE_URL}/{endpoint}", params=params, headers=self.headers).json()

            if "pagination" in response:
                total_pages = response["pagination"]["total"]

            data.extend(response.get(endpoint, []))

            page += 1

        return data

    def fetch_platforms(self):
        response = requests.get(
            f"{self.BASE_URL}/platforms", headers=self.headers)
        return response.json()

    def fetch_accounts(self, platform, page=1):
        return self._fetch_paginated_data("accounts", {"platform": platform})

    def fetch_fields(self, platform, page=1):
        return self._fetch_paginated_data("fields", {"platform": platform})

    def fetch_insights(self, platform, account_id, token, field_values):
        response = requests.get(
            f"{self.BASE_URL}/insights",
            params={
                "platform": platform,
                "account": account_id,
                "token": token,
                "fields": ",".join(field_values)
            },
            headers=self.headers
        )
        return response.json()
