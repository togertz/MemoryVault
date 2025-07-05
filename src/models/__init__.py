from .base import db
from .memory import Memory

__all__ = ["db", "Memory"]

from flask import Flask

def init_app(app:Flask):
    db.init_app(app)