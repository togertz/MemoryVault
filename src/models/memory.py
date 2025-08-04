from sqlalchemy.sql import func

from .base import db


class Memory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.DateTime(timezone=True))
    latitude = db.Column(db.Numeric, nullable=True)
    longitude = db.Column(db.Numeric, nullable=True)
    image_uri = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    vault_id = db.Column(db.Integer, db.ForeignKey("vault.id"), nullable=False)

    def __repr__(self):
        return f"User {self.id}"

    def to_json(self):
        return {
            "id": self.id,
            "description": self.description,
            "date": self.date,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "image_uri": self.image_uri
        }
