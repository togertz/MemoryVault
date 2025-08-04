from .base import db
from sqlalchemy.sql import func


class Family(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    family_name = db.Column(db.String(30), nullable=False)
    invite_code = db.Column(db.String(100), nullable=False, unique=True)

    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    members = db.relationship('User', backref="member", uselist=True)
    vault = db.relationship("Vault", backref='family', uselist=False)

    def json_package(self):
        return {
            "family_name": self.family_name,
            "invite_code": self.invite_code,
            "members": [user.username for user in self.members],
            "number_members": len(self.members)
        }
