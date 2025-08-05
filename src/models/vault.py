"""
DB module for representing a vault in MemoryVault.
"""
import enum
from datetime import date
from sqlalchemy import Enum
from sqlalchemy.sql import func

from .base import db


class CollectionPeriodDurationEnum(enum.Enum):
    """
    Enumeration for storing all possible durations a collection period can last.
    """
    MONTHLY = 1
    QUARTERLY = 3
    HALF_YEARLY = 6
    YEARLY = 12


class Vault(db.Model):
    """
    Definition of vault table in DB.
    A vault is a bundle of uploaded memories of one user or one family.
    """
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

    def get_number_of_memories_in_timespan(self, timespan_begin: date, timespan_end: date) -> int:
        """
        Returns the number of all memories uploaded in a specified timespan to the vault instance.

        Parameters:
            timespan_begin: date
                start date of the specified timespan
            timespan_end: date
                end date of the specified timespan

        Returns:
            int: number of memories uploaded during the timespan
        """
        number_memories = 0
        for memory in self.memories:
            if timespan_begin < memory.date.date() and memory.date.date() <= timespan_end:
                number_memories += 1

        return number_memories

    def json_package(self) -> dict:
        """
        Returns a dictionary representation of the vault instance,
        including vault id, user id, family id, period duration, and intial start of vault.

        Returns:
            dict: A dictionary containing vault details.
        """
        return {
            "vault_id": self.id,
            "user_id": self.user_id,
            "family_id": self.family_id,
            "period_duration": self.period_duration,
            "period_initial_start": self.period_initial_start
        }
