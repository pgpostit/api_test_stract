from flask import Flask, jsonify
from api.services import StractAPIService
from api.insights_processor import InsightsProcessor
from api.utils import generate_csv, summarize_data, normalize_data

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
        data = insights_processor.process_insights(platform)

        return generate_csv(data, f"{platform}.csv")

    @app.route("/<platform>/resumo", methods=["GET"])
    def get_platform_summary(platform):
        data = insights_processor.process_insights(platform)
        summarized_data = summarize_data(data)

        return generate_csv(summarized_data, f"{platform}_summary.csv")

    @app.route("/geral", methods=["GET"])
    def get_general_data():
        data = insights_processor.process_insights()
        normalized_data = normalize_data(data)
        return generate_csv(normalized_data, "general.csv")

    @app.route("/geral/resumo", methods=["GET"])
    def get_general_summary():
        data = insights_processor.process_insights()
        normalized_data = normalize_data(data)
        summarized_data = summarize_data(normalized_data)
        return generate_csv(summarized_data, "general_summary.csv")
