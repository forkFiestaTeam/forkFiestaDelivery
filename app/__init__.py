from flask import Flask
from app.api.forkfiesta import forkfiesta_routes

# Configuration
import app.config

def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(forkfiesta_routes, url_prefix="/api/forkfiesta")
    return app
