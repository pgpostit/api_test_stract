import csv
import io
from flask import Response


def normalize_data(data):
    ...


def summarize_data(data):
    summary = {}

    for entry in data:
        account_key = entry.get("Account")

        if account_key not in summary:
            summary[account_key] = {k: 0 if isinstance(
                v, (int, float)) else "" for k, v in entry.items()}
            summary[account_key]["Platform"] = entry["Platform"]
            summary[account_key]["Account"] = entry["Account"]

        for key, value in entry.items():
            if isinstance(value, (int, float)):
                summary[account_key][key] += value
            elif key == "ad_name":
                if summary[account_key][key]:
                    summary[account_key][key] += f", {value}"
                else:
                    summary[account_key][key] = value

    return list(summary.values())


def generate_csv(data, filename):
    if not data:
        return Response("No data available", status=400)

    output = io.StringIO()
    csv_writer = csv.DictWriter(
        output, fieldnames=data[0].keys(), delimiter=";")
    csv_writer.writeheader()
    csv_writer.writerows(data)

    response = Response(output.getvalue().encode(
        "utf-8-sig"), mimetype="text/csv")
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Content-Type"] = "text/csv; charset=utf-8"

    return response
