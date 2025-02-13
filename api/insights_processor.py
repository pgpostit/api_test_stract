import concurrent.futures
from api.services import StractAPIService


class InsightsProcessor:

    def __init__(self, api_service: StractAPIService):
        self.api_service = api_service

    def process_insights(self, platform=None):
        insights_data = []

        platforms = [platform] if platform else [x["value"] for x in self.api_service.fetch_platforms().get("platforms", [])]

        for platform in platforms:
            platform_id = platform
            accounts = self.api_service.fetch_accounts(platform_id)
            field_values = [f["value"]
                            for f in self.api_service.fetch_fields(platform_id)]

            num_workers = min(max(len(accounts) // 2, 5), 20)
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
                futures = {
                    executor.submit(self.api_service.fetch_insights, platform_id, acc["id"], acc["token"], field_values): acc
                    for acc in accounts
                }

                for future in concurrent.futures.as_completed(futures):
                    acc = futures[future]
                    try:
                        response = future.result()
                        insights = response.get("insights", [])

                        for entry in insights:
                            entry["Platform"] = platform_id
                            entry["Account"] = acc["name"]
                            insights_data.append(entry)
                    except Exception as e:
                        print(
                            f"An error occurred while searching insights for {acc['name']}: {e}")

        return insights_data
