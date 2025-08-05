"""
DB module for representing a Memory in MemoryVault.
"""
from sqlalchemy.sql import func

from .base import db


class Memory(db.Model):
    """
    Definition of memory table in DB.
    A memory is a collection consisting of text, image,
    date and coordinates that describes a particular memory.
    """
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.DateTime(timezone=True))
    latitude = db.Column(db.Numeric, nullable=True)
    longitude = db.Column(db.Numeric, nullable=True)
    image_uri = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    vault_id = db.Column(db.Integer, db.ForeignKey("vault.id"), nullable=False)

    def to_json(self) -> dict:
        """
        Returns a dictionary representation of the Memory instance,
        including memory id, description, date, coordinates and image_uri.

        Returns:
            dict: A dictionary containing memory details.
        """
        return {
            "id": self.id,
            "description": self.description,
            "date": self.date,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "image_uri": self.image_uri
        }
