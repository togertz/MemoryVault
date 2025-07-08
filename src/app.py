from flask import Flask
from flask_bcrypt import Bcrypt

bcrypt_app = Bcrypt()

def create_app(config_class='src.config.Config'):
    app = Flask(__name__)
    bcrypt_app.init_app(app)
    app.config.from_object(config_class)

    from . import models, routes

    models.init_app(app)
    routes.init_app(app)

    with app.app_context():
        models.db.create_all()

    return app