"""
DB module for representing a user in MemoryVault.
"""
from sqlalchemy.sql import func

from .base import db


class User(db.Model):
    """
    Definition of user table in DB.
    A user is a person able to create and upload memories as well as
    accessing the slideshow after the predefined collection period.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    firstname = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(20), nullable=True)
    birthday = db.Column(db.DateTime(timezone=True))

    is_admin = db.Column(db.Boolean, nullable=False)

    registered_at = db.Column(db.DateTime(
        timezone=True), server_default=func.now())

    family_id = db.Column(
        db.Integer, db.ForeignKey("family.id"), nullable=True)
    vault = db.relationship("Vault", backref='owner', uselist=False)

    def json_package(self) -> dict:
        """
        Returns a dictionary representation of the user instance,
        including username, firstname, family_id and admin flag.

        Returns:
            dict: A dictionary containing user details.
        """
        return {
            "username": self.username,
            "firstname": self.firstname,
            "family_id": self.family_id,
            "admin": self.is_admin
        }
