from flask import Flask
from app.main import bp as main_bp
from app.chat import chat_bp
from flask_restx import Api
from .apis.form_handler import form_ns


def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)

    app.register_blueprint(main_bp)
    app.register_blueprint(chat_bp)

    api = Api(app, doc="/docs")

    api.add_namespace(form_ns)

    return app
