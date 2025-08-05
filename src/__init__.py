"""
MemoryVault package initializer.
Allows external scripts to import and start the Flask app using create_app.
"""
from .app import create_app

__all__ = ['create_app']
