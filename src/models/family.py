from .base import db
from sqlalchemy.sql import func

class Family(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    members = db.relationship('User', backref="member", uselist=True)
    vault = db.relationship("Vault", backref='family', uselist=False)