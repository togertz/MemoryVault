"""
Main application module for MemoryVault.
Loads app configuration, creates Flask app, and configures routes and models.
"""
import os
from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt

load_dotenv()

if os.getenv("FLASK_ENV") == "production":
    CONFIG_CLASS = 'src.config.ProductionConfig'
else:
    CONFIG_CLASS = 'src.config.DevelopmentConfig'

bcrypt_app = Bcrypt()


def create_app(config_class=CONFIG_CLASS):
    app = Flask(__name__)
    bcrypt_app.init_app(app)
    app.config.from_object(config_class)

    from . import models, routes

    models.init_app(app)
    routes.init_app(app)

    with app.app_context():
        models.db.create_all()

    return app
