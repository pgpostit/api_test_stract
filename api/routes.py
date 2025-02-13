from flask import Flask, jsonify
from api.services import StractAPIService
from api.insights_processor import InsightsProcessor
from api.utils import generate_csv

api_service = StractAPIService()
insights_processor = InsightsProcessor(api_service)


def register_routes(app: Flask):

    @app.route("/", methods=["GET"])
    def home():
        return jsonify({
            "name": "Paulo S. Garcia",
            "email": "pgarcia2022@gmail.com",
            "linkedin": "https://linkedin.com/in/paulogarcia01"
        })

    @app.route("/<platform>", methods=["GET"])
    def get_platform_data(platform):
        data = insights_processor.process_insights()
        platform_data = [row for row in data if row["Platform"] == platform]

        return generate_csv(platform_data, f"{platform}.csv")
