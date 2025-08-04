from .base import db
from sqlalchemy.sql import func

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    firstname = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(20), nullable=True)
    birthday = db.Column(db.DateTime(timezone=True))

    is_admin = db.Column(db.Boolean, nullable=False)

    registered_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    family_id = db.Column(db.Integer, db.ForeignKey("family.id"), nullable=True)
    vault = db.relationship("Vault", backref='owner', uselist=False)

    def __repr__(self):
        return f"User {self.username}"

    def json_package(self):
        return {
            "username": self.username,
            "firstname": self.firstname,
            "family_id": self.family_id,
            "admin": self.is_admin
        }