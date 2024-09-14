from flask import Flask
from .api import api_blueprint
from .scraper import start_scraper

def create_app():
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(api_blueprint)

    # Start background scraping
    start_scraper()

    return app
