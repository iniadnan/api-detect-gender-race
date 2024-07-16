from flask import Flask
from config import Config
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize CORS
    CORS(app)

    from app.main.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
