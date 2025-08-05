"""
DB module for representing a family in MemoryVault.
"""
from sqlalchemy.sql import func

from .base import db


class Family(db.Model):
    """
    Definition of family table in DB.
    A family is a bundle of multiple users whose
    memories will be stored together in one shared vault.
    """
    id = db.Column(db.Integer, primary_key=True)
    family_name = db.Column(db.String(30), nullable=False)
    invite_code = db.Column(db.String(100), nullable=False, unique=True)

    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    members = db.relationship('User', backref="member", uselist=True)
    vault = db.relationship("Vault", backref='family', uselist=False)

    def json_package(self) -> dict:
        """
        Returns a dictionary representation of the Family instance,
        including family name, invite code, member usernames, and member count.

        Returns:
            dict: A dictionary containing family details.
        """
        return {
            "family_name": self.family_name,
            "invite_code": self.invite_code,
            "members": [user.username for user in self.members],
            "number_members": len(self.members)
        }
