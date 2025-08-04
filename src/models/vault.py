import enum
from datetime import date
from sqlalchemy import Enum
from sqlalchemy.sql import func

from .base import db


class CollectionPeriodDurationEnum(enum.Enum):
    MONTHLY = 1
    QUARTERLY = 3
    HALF_YEARLY = 6
    YEARLY = 12


class Vault(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    period_duration = db.Column(Enum(CollectionPeriodDurationEnum,
                                name="collection_period_enum", native_enum=False), nullable=False)
    period_initial_start = db.Column(db.Date, nullable=False)

    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.id"), unique=True, nullable=True)
    family_id = db.Column(db.Integer, db.ForeignKey(
        "family.id"), unique=True, nullable=True)

    memories = db.relationship('Memory', backref="vault", uselist=True)

    def get_number_of_memories_in_timespan(self, timespan_begin: date, timespan_end: date):
        number_memories = 0
        for memory in self.memories:
            if timespan_begin < memory.date.date() and memory.date.date() <= timespan_end:
                number_memories += 1

        return number_memories

    def json_package(self):
        return {
            "vault_id": self.id,
            "user_id": self.user_id,
            "family_id": self.family_id,
            "period_duration": self.period_duration,
            "period_initial_start": self.period_initial_start
        }
