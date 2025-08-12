"""
Base module for database connection.
Initializes connection to SQL database using SQLAlchemy.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
