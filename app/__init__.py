from flask import Flask
from app.main import bp as main_bp


def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)

    app.register_blueprint(main_bp)

    return app
