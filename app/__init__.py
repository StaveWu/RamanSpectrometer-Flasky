from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import config
from .io import SpectrumIO, ComponentIO, ModelIO

db = SQLAlchemy()
spectrum_io = SpectrumIO()
component_io = ComponentIO()
model_io = ModelIO()


def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    spectrum_io.init_app(app)
    component_io.init_app(app)
    model_io.init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app

