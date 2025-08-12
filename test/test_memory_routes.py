import pytest
from unittest.mock import patch


def test_get_not_logged_in(app_client):
    """
    Tests redirect to login page when no user is logged in.
    """
    app, client = app_client

    res = client.get("/memory/")
    assert res.status_code == 302
    assert '/login' in res.location


def test_get_no_vault_configured(app_client):
    """
    Tests redirect to settings page when no vault is configured.
    """
    app, client = app_client

    # Mock login
    with client.session_transaction() as session:
        session["user_id"] = 1

    res = client.get("/memory/")
    assert res.status_code == 302
    assert '/settings' in res.location


def test_get_upload_page(app_client):
    """
    Tests requesting the upload HTML website.
    """
    app, client = app_client

    # Mock login and vault
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_info"] = {"firstname": "Max"}
        # Only days left will be used in ninja render
        session["vault_info"] = {"days_left": 10}

    res = client.get("/memory/")
    assert res.status_code == 200
    html = res.get_data(as_text=True)
    assert "Upload a new Memory to your Vault" in html


def test_post_own_vault_not_configured(app_client):
    """
    Test POST on upload_memory to own vault without having vault configured.
    """
    app, client = app_client

    # Mock login and vault
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_info"] = {"firstname": "Max"}
        # Only days left will be used in ninja render
        session["family_vault_info"] = {"days_left": 10}

    res = client.post("/memory/", data={
        "vault": "own_vault",
        "date": "2025-01-01",
        "description": "test"
    })

    assert res.status_code == 200
    html = res.get_data(as_text=True)
    assert "You cannot upload memories to your own vault when it is not configured." in html


def test_post_family_vault_not_configured(app_client):
    """
    Test POST on upload_memory to family vault without having vault configured.
    """
    app, client = app_client

    # Mock login and vault
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_info"] = {"firstname": "Max"}
        # Only days left will be used in ninja render
        session["vault_info"] = {"days_left": 10}

    res = client.post("/memory/", data={
        "vault": "family_vault",
        "date": "2025-01-01",
        "description": "test"
    })

    assert res.status_code == 200
    html = res.get_data(as_text=True)
    assert "You cannot upload memories to your family vault when it is not configured." in html


def test_post_date_outside_period(app_client):
    """
    Test POST memory that is not in the current Collection Period.
    """
    app, client = app_client

    # Mock login and vault
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_info"] = {"firstname": "Max"}
        # Only days left will be used in ninja render
        session["vault_info"] = {
            "vault_id": 1,
            "days_left": 10,
            "curr_period_start": "Friday, Aug 01, 2025",
            "curr_period_end": "Sunday, Aug 31, 2025"
        }

    res = client.post("/memory/", data={
        "vault": "own_vault",
        "date": "2025-07-01",
        "description": "test"
    })

    assert res.status_code == 200
    html = res.get_data(as_text=True)
    assert "You cannot upload a memory that is not part of the current Collection Period" in html


def test_post_valid_upload(app_client):
    """
    Test POST a valid memory upload.
    """
    app, client = app_client

    # Mock login and vault
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_info"] = {"firstname": "Max"}
        # Only days left will be used in ninja render
        session["vault_info"] = {
            "vault_id": 1,
            "days_left": 10,
            "curr_period_start": "Friday, Aug 01, 2025",
            "curr_period_end": "Sunday, Aug 31, 2025"
        }

    with patch("src.memoryvault.services.MemoryManagement.upload_memory") as mock_upload:
        res = client.post("/memory/", data={
            "vault": "own_vault",
            "date": "2025-08-05",
            "description": "test"
        })

        assert res.status_code == 200
        mock_upload.assert_called_once()


def test_exception_handeling(app_client):
    """
    Test exception handeling.
    """
    app, client = app_client

    # Mock login and vault
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_info"] = {"firstname": "Max"}
        # Only days left will be used in ninja render
        session["vault_info"] = {
            "vault_id": 1,
            "days_left": 10,
            "curr_period_start": "Friday, Aug 01, 2025",
            "curr_period_end": "Sunday, Aug 31, 2025"
        }

    with patch("src.memoryvault.services.MemoryManagement.upload_memory", side_effect=Exception):
        res = client.post("/memory/", data={
            "vault": "own_vault",
            "date": "2025-08-05",
            "description": "test"
        })

        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert "Please contact an admin to get furhter insights into this error." in html
