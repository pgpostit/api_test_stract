from flask import Flask
from api.routes import register_routes
from api.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_routes(app)
    return app
