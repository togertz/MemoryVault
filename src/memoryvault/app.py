"""
Main application module for MemoryVault.
Loads app configuration, creates Flask app, and configures routes and models.
"""
import os
import logging
from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

if os.getenv("FLASK_ENV") == "production":
    print("Using production mode")
    CONFIG_CLASS = 'src.memoryvault.config.ProductionConfig'
else:
    print("Using development mode")
    CONFIG_CLASS = 'src.memoryvault.config.DevelopmentConfig'

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
