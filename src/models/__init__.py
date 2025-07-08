from .base import db
from .memory import Memory
from .user import User

__all__ = ["db", "Memory", "User"]

from flask import Flask

def init_app(app:Flask):
    db.init_app(app)