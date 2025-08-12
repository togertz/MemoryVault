"""
Module containing utility classes for vault management.
"""
from abc import ABC
import calendar
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from ..models import db, User, Vault, CollectionPeriodDurationEnum, Family


class VaultManagement(ABC):
    """
    Utility class for vault creation and management.
    """
    @staticmethod
    def create_vault(user_id: int,
                     family_id: int,
                     period_duration: int,
                     first_period_start: datetime.date) -> bool:
        """
        Creates vault and stores information in a database.

        Parameters:
            user_id: int
                id of the user owning this vault.
            family_id: int
                id of the family owning this vault
            period_duration: int
                Number of months one collection period for this vault is going to last.
            first_period_start: datetime.datetime.date
                Start date of the first collection period

        Returns:
            bool: Is true if vault was created sucessfully.
        """
        if (user_id is None) and (family_id is None):
            raise ValueError("Either user_id or family_id have to be filled")
        # -- Parse input --
        period_duration = CollectionPeriodDurationEnum(int(period_duration))
        [period_start_month, period_start_year] = first_period_start.split("-")
        period_start_month = int(period_start_month) + 1
        first_period_start = datetime(
            year=int(period_start_year), month=period_start_month, day=1).date()

        # -- Create vault instance --
        if user_id:
            vault = Vault(
                user_id=user_id,
                period_duration=period_duration,
                period_initial_start=first_period_start
            )
        else:
            vault = Vault(
                family_id=family_id,
                period_duration=period_duration,
                period_initial_start=first_period_start
            )
        db.session.add(vault)
        db.session.commit()

        return True

    @staticmethod
    def _get_vault(user_id: int = None,
                   family_id: int = None,
                   vault_id: int = None) -> Vault:
        """
        Returns a vault instance based on user_id, family_id or vault_id.

        Parameters:
            user_id: int
                id of the user owning this vault.
            family_id: int
                id of the family owning this vault
            vault_id: int
                unique identifier of vault instance

        Returns:
            Vault
        """
        if (user_id is None) and (vault_id is None) and (family_id is None):
            raise ValueError(
                "Either user_id, family_id, or vault_id have to be filled")

        vault = None
        if user_id:
            user = User.query.filter_by(id=user_id).first()
            vault = user.vault
        elif vault_id:
            vault = Vault.query.filter_by(id=vault_id).first()
        elif family_id:
            family = Family.query.filter_by(id=family_id).first()
            vault = family.vault

        return vault

    @staticmethod
    def _get_start_end_curr_period(start_date: datetime.date,
                                   duration: CollectionPeriodDurationEnum) -> dict:
        """
        Returns the start and end date of the current collection period based on the initial
        start of the first collection period and the duration.

        Parameters:
            user_id: int
                id of the user owning this vault.
            family_id: int
                id of the family owning this vault
            vault_id: int
                unique identifier of vault instance

        Returns:
            Vault
        """
        interval_months = duration.value

        today = datetime.today().date()

        while start_date + relativedelta(months=interval_months) <= today:
            start_date += relativedelta(months=interval_months)

        end_period_date = start_date + \
            relativedelta(months=interval_months) - timedelta(days=1)
        last_day = calendar.monthrange(
            end_period_date.year, end_period_date.month)[1]

        return {
            "start_date": start_date,
            "end_date": end_period_date.replace(day=last_day)
        }

    @staticmethod
    def _get_vault_info(vault: Vault) -> dict:
        """
        Returns the vault information as dict. Additional information such as start, end of and
        days left in Collection Period are returned in dict.

        Parameters:
            vault: Vault
                The vault instance to retrieve information about.

        Returns:
            dict: the vault information
        """
        vault_info = vault.json_package()

        period_duration = vault_info["period_duration"]
        period_initial_start = vault_info["period_initial_start"]
        period_start_end = VaultManagement._get_start_end_curr_period(
            period_initial_start, period_duration)

        today = datetime.today().date()

        vault_info["period_duration"] = period_duration.value
        vault_info["period_initial_start"] = period_initial_start
        vault_info["curr_period_start"] = period_start_end["start_date"].strftime(
            "%A, %b %d, %Y")
        vault_info["curr_period_end"] = period_start_end["end_date"].strftime(
            "%A, %b %d, %Y")
        vault_info["days_left"] = (period_start_end["end_date"] - today).days
        vault_info["slideshow_available"] = True

        return vault_info

    @staticmethod
    def get_all_periods(user_id: int = None,
                        vault_id: int = None,
                        family_id: int = None) -> list:
        """
        Returns list containing the start and end dates of all Collection Periods since
        the initial Collection Period.

        Parameters:
            user_id: int
                id of the user owning this vault.
            family_id: int
                id of the family owning this vault
            vault_id: int
                unique identifier of vault instance

        Returns:
            list: containing dicts with keys "period_start" and "period_end"
        """
        vault = VaultManagement._get_vault(
            user_id=user_id, vault_id=vault_id, family_id=family_id)
        vault_info = vault.json_package()

        interval_monts = vault_info["period_duration"].value
        periods = []

        today = datetime.today().date()

        current_start = vault_info["period_initial_start"]

        while current_start <= today:
            current_end = current_start + \
                relativedelta(months=interval_monts) - timedelta(days=1)
            last_day = calendar.monthrange(
                current_end.year, current_end.month)[1]
            current_end = current_end.replace(day=last_day)
            periods.append({
                "period_start": current_start.strftime("%A, %b %d, %Y"),
                "period_end": current_end.strftime("%A, %b %d, %Y")
            })
            current_start = current_start + \
                relativedelta(months=interval_monts)

        return periods

    @staticmethod
    def get_vault_info(user_id: int = None,
                       vault_id: int = None,
                       family_id: int = None) -> dict:
        """
        Returns the vault information as dict.

        Parameters:
            user_id: int
                id of the user owning this vault.
            family_id: int
                id of the family owning this vault
            vault_id: int
                unique identifier of vault instance

        Returns:
            dict: the vaults information
        """
        vault = VaultManagement._get_vault(
            user_id=user_id, vault_id=vault_id, family_id=family_id)

        if vault is None:
            return None

        return VaultManagement._get_vault_info(vault=vault)

    @staticmethod
    def get_number_memories(user_id: int = None,
                            vault_id: int = None,
                            family_id: int = None) -> int:
        """
        Returns the number of memories in the vault during the ongoing Collection Period.

        Parameters:
            user_id: int
                id of the user owning this vault.
            family_id: int
                id of the family owning this vault
            vault_id: int
                unique identifier of vault instance

        Returns:
            int: Number of memories
        """
        vault = VaultManagement._get_vault(
            user_id=user_id, vault_id=vault_id, family_id=family_id)
        vault_info = VaultManagement._get_vault_info(vault=vault)

        timespan_begin = datetime.strptime(
            vault_info["curr_period_start"], "%A, %b %d, %Y").date()
        timespan_end = datetime.strptime(
            vault_info["curr_period_end"], "%A, %b %d, %Y").date()

        return vault.get_number_of_memories_in_timespan(timespan_begin=timespan_begin,
                                                        timespan_end=timespan_end)
