"""
Model package initializer.
Loads all db model classes and enables easier imports.
"""
from flask import Flask

from .base import db
from .family import Family
from .memory import Memory
from .user import User
from .vault import Vault, CollectionPeriodDurationEnum

__all__ = ["db", "Family", "Memory", "User",
           "Vault", "CollectionPeriodDurationEnum"]


def init_app(app: Flask) -> None:
    """
    Initializes database connection using SQL Alchemy.

    Returns:
        None
    """
    db.init_app(app)
