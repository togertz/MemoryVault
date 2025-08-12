import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime

from src.memoryvault.services import VaultManagement
from src.memoryvault.models import CollectionPeriodDurationEnum


@pytest.fixture
def vault_mock():
    vault = MagicMock()
    vault.id = 1
    vault.period_duration = CollectionPeriodDurationEnum.YEARLY
    vault.period_initial_start = "2025-01-01"
    vault.user_id = 1
    vault.family_id = None
    return vault


@patch("src.memoryvault.services.vault_util.db")
@patch("src.memoryvault.services.vault_util.Vault")
def test_create_vault_successful(mock_vault_cls, mock_db, vault_mock):
    mock_vault_cls.return_value = vault_mock

    result = VaultManagement.create_vault(
        user_id=1,
        family_id=None,
        period_duration=12,
        first_period_start="01-2025"
    )

    assert result is True
    mock_db.session.add.assert_called_once_with(vault_mock)
    mock_db.session.commit.assert_called()


def test_create_vault_no_user_and_family_id():

    with pytest.raises(ValueError) as exc:
        result = VaultManagement.create_vault(
            user_id=None,
            family_id=None,
            period_duration=12,
            first_period_start=datetime(2025, 1, 1).date()
        )

    assert isinstance(exc.value, ValueError)
    assert "Either user_id or family_id have to be filled" in str(
        exc.value)


@patch("src.memoryvault.services.vault_util.Vault")
def test_get_vault_successful(mock_vault_cls, vault_mock):
    mock_vault_cls.query.filter_by.return_value.first.return_value = vault_mock

    vault = VaultManagement._get_vault(vault_id=1)
    assert vault.id == vault_mock.id
    assert vault.period_duration == vault_mock.period_duration


def test_get_vault_successful_no_id_provided():

    with pytest.raises(ValueError) as exc:
        vault = VaultManagement._get_vault(
            user_id=None, family_id=None, vault_id=None)

    assert isinstance(exc.value, ValueError)
    assert "Either user_id, family_id, or vault_id have to be filled" in str(
        exc.value)


@patch("src.memoryvault.services.vault_util.datetime")
def test_get_start_end_curr_period_no_shifts(mock_datetime):
    mock_datetime.today.return_value = datetime(2025, 8, 12)
    # Keep other functionality of datetime:
    mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

    start_date = datetime(2025, 8, 1).date()
    duration = CollectionPeriodDurationEnum(1)

    result = VaultManagement._get_start_end_curr_period(
        start_date=start_date, duration=duration)

    assert result["start_date"] == datetime(2025, 8, 1).date()
    assert result["end_date"] == datetime(2025, 8, 31).date()
