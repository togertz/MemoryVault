from .base import db
from sqlalchemy.sql import func

class Memory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.DateTime(timezone=True))
    location = db.Column(db.String(50), nullable=True)
    image_uri = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"User {self.id}"