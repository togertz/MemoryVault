from abc import ABC
import calendar
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from ..models import db, User, Vault, CollectionPeriodDurationEnum

class VaultManagement(ABC):

    @staticmethod
    def create_vault(user_id, period_duration, first_period_start):
        period_duration = CollectionPeriodDurationEnum(int(period_duration))
        [period_start_month, period_start_year] = first_period_start.split("-")
        period_start_month = int(period_start_month) + 1
        first_period_start = datetime(year=int(period_start_year), month=period_start_month, day=1).date()

        vault = Vault(
            user_id=user_id,
            period_duration=period_duration,
            period_initial_start=first_period_start
        )
        db.session.add(vault)
        db.session.commit()

        return True

    @staticmethod
    def _get_vault(user_id=None, vault_id=None):
        if (user_id is None) and (vault_id is None):
            raise ValueError("Either user_id or vault_id have to be filled")

        if user_id:
            user = User.query.filter_by(id=user_id).first()
            vault = user.vault
        else:
            vault = Vault.query.filter_by(id=vault_id).first()

        return vault

    @staticmethod
    def _get_start_end_curr_period(start_date, duration:CollectionPeriodDurationEnum):
        interval_months = duration.value
        today = datetime.today().date()

        while start_date + relativedelta(months=interval_months) <= today:
            start_date += relativedelta(months=interval_months)

        end_period_date = start_date + relativedelta(months=interval_months) - timedelta(days=1)
        last_day = calendar.monthrange(end_period_date.year, end_period_date.month)[1]

        return {
            "start_date": start_date,
            "end_date": end_period_date.replace(day=last_day)
        }

    @staticmethod
    def _get_vault_info(vault:Vault):
        vault_info = vault.json_package()

        period_duration = vault_info["period_duration"]
        period_initial_start = vault_info["period_initial_start"]
        period_start_end = VaultManagement._get_start_end_curr_period(period_initial_start, period_duration)

        today = datetime.today().date()

        vault_info["period_duration"] = period_duration.value
        vault_info["period_initial_start"] = period_initial_start
        vault_info["curr_period_start"] = period_start_end["start_date"].strftime("%A, %b %d, %Y")
        vault_info["curr_period_end"] = period_start_end["end_date"].strftime("%A, %b %d, %Y")
        vault_info["days_left"] = (period_start_end["end_date"] - today).days

        return vault_info


    @staticmethod
    def get_vault_info(user_id=None, vault_id=None):
        vault = VaultManagement._get_vault(user_id=user_id, vault_id=vault_id)

        if vault is None:
            return None

        return VaultManagement._get_vault_info(vault=vault)

    @staticmethod
    def get_number_memories(user_id=None, vault_id=None):
        vault = VaultManagement._get_vault(user_id=user_id, vault_id=vault_id)
        vault_info = VaultManagement._get_vault_info(vault=vault)

        if type(vault_info["curr_period_start"]) == str:
            timespan_begin = datetime.strptime(vault_info["curr_period_start"], "%A, %b %d, %Y").date()
            timespan_end = datetime.strptime(vault_info["curr_period_end"], "%A, %b %d, %Y").date()

        return vault.get_number_of_memories_in_timespan(timespan_begin=timespan_begin,
                                                        timespan_end=timespan_end)
