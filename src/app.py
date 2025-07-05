from flask import Flask

def create_app(config_class='src.config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from . import models, routes

    models.init_app(app)
    routes.init_app(app)

    with app.app_context():
        models.db.create_all()

    return app