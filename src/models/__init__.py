from .base import db

from .family import Family
from .memory import Memory
from .user import User
from .vault import Vault, CollectionPeriodDurationEnum

__all__ = ["db", "Family", "Memory", "User", "Vault", "CollectionPeriodDurationEnum"]

from flask import Flask

def init_app(app:Flask):
    db.init_app(app)