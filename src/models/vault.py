from .base import db
from sqlalchemy.sql import func

class Vault(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    collectionPeriodEnd = db.Column(db.Date, nullable=False)

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True, nullable=True)
    family_id = db.Column(db.Integer, db.ForeignKey("family.id"), unique=True, nullable=True)

    memories = db.relationship('Memory', backref="vault", uselist=True)