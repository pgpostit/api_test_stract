import csv
import io
from flask import Response


def normalize_data(data):
    FIELD_MAPPINGS = {
        "adName": "ad_name",       # GA4 → Meta Ads/TikTok
        "cost": "spend",           # GA4/TikTok → Meta Ads
        "region": "country",       # GA4 → Meta Ads/TikTok
        "cost_per_click": "cpc",   # TikTok → Meta Ads
        "status": "effective_status"  # GA4 → Meta Ads
    }

    normalized_data = []

    for entry in data:
        normalized_entry = {}

        for key, value in entry.items():
            new_key = FIELD_MAPPINGS.get(key, key)
            normalized_entry[new_key] = value

        if "cpc" not in normalized_entry:
            spend = normalized_entry.get("spend", 0)
            clicks = normalized_entry.get("clicks", 0)
            normalized_entry["cpc"] = (spend / clicks) if clicks > 0 else 0

        normalized_data.append(normalized_entry)

    translated_fields = set(FIELD_MAPPINGS.keys())
    final_data = [{k: v for k, v in entry.items() if k not in translated_fields}
                  for entry in normalized_data]

    return final_data


def summarize_data(data):
    summary = {}

    for entry in data:
        account_key = entry.get("Account")

        if account_key not in summary:
            summary[account_key] = {
                k: (0 if isinstance(v, (int, float)) else "") for k, v in entry.items()}
            summary[account_key]["Platform"] = entry["Platform"]
            summary[account_key]["Account"] = entry["Account"]

        for key, value in entry.items():
            if isinstance(value, (int, float)):
                summary[account_key][key] += value
            elif isinstance(value, str):
                if summary[account_key][key]:
                    summary[account_key][key] = f"{summary[account_key][key]}, {value}"
                else:
                    summary[account_key][key] = value

    return list(summary.values())


def generate_csv(data, filename):
    if not data:
        return Response("No data available", status=400)

    fieldnames = list(data[0].keys())

    output = io.StringIO()
    csv_writer = csv.DictWriter(
        output, fieldnames=fieldnames, delimiter=";", extrasaction="ignore")

    csv_writer.writeheader()
    csv_writer.writerows(data)

    response = Response(output.getvalue(),
                        mimetype="text/csv; charset=utf-8-sig")
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"

    return response
