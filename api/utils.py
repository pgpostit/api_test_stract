import csv
import io
from flask import Response


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
