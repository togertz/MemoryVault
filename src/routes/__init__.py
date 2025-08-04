from flask import Flask

from .base import base_bp
from .memory import memory_bp
from .user import user_bp
from .settings import settings_bp
from .slideshow import slideshow_bp


def init_app(app: Flask):

    app.register_blueprint(base_bp)
    app.register_blueprint(memory_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(slideshow_bp)
