from flask import Flask
from flask_cors import CORS
from app.api.forkfiesta import forkfiesta_routes

# Configuration
import app.config

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes

    # Register blueprints
    app.register_blueprint(forkfiesta_routes, url_prefix="/api/forkfiesta")
    return app
