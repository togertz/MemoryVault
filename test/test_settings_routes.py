import pytest
from unittest.mock import patch

from src.services import UserException

# ------------------- /settings/ -------------------


def test_get_index_not_logged_in(app_client):
    """
    Tests redirect to get login page when no user is logged in.
    """
    app, client = app_client

    res = client.get("/settings/")
    assert res.status_code == 302
    assert '/login' in res.location


def test_get_index_no_vault_configured(app_client):
    """
    Test GET on settings when no vault or family is configured.
    """
    app, client = app_client

    # Mock login
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_info"] = {"firstname": "Max"}

    with patch("src.routes.settings.VaultManagement.get_vault_info", return_value=None):
        res = client.get("/settings/")

        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert "Please create a vault or family to upload memories." in html
        assert "Join a Family" in html
        assert "Create a Family" in html


def test_get_index_private_vault_configured(app_client):
    """
    Test GET on settings when only private vault is configured.
    """
    app, client = app_client

    # Mock login
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_info"] = {"firstname": "Max"}

    fake_vault_info = {"days_left": 10, "period_duration": 6,
                       "curr_period_end": "Friday, 26 March 2025"}

    with patch("src.routes.settings.VaultManagement.get_vault_info", return_value=fake_vault_info), \
            patch("src.routes.settings.VaultManagement.get_number_memories", return_value=10):
        res = client.get("/settings/")

        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert "Number of Memories in current Vault" in html
        assert "Join a Family" in html
        assert "Create a Family" in html


def test_get_index_family_vault_configured(app_client):
    """
    Test GET on settings when only family vault is configured.
    """
    app, client = app_client

    # Mock login
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_info"] = {"firstname": "Max", "family_id": 5}
        session["family_vault_info"] = {
            "family_name": "Doe",
            "invite_code": "abc",
            "number_members": 2,
            "members": ["a", "b"],
            "number_memories": 5,
            "days_left": 10,
            "period_duration": 6,
            "curr_period_end": "Friday, 26 March 2025"
        }

    with patch("src.routes.settings.VaultManagement.get_vault_info", return_value=None):
        res = client.get("/settings/")

        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert "Please create a vault or family to upload memories." in html
        assert "Family Information" in html
        assert "Family Vault Information" in html


def test_index_exception_handeling(app_client):
    """
    Test exception handeling.
    """
    app, client = app_client

    # Mock login
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_info"] = {"firstname": "Max"}

    with patch("src.routes.settings.VaultManagement.get_vault_info", side_effect=RuntimeError):
        res = client.get("/settings/")

        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert "Please contact an admin to get furhter insights into this error." in html


# ------------------- /settings/create_vault -------------------

def test_post_create_vault_not_logged_in(app_client):
    """
    Tests redirect to get settings page when no user is logged in.
    """
    app, client = app_client

    res = client.post("/settings/create_vault")
    assert res.status_code == 302
    assert '/login' in res.location


def test_post_create_vault_missing_data(app_client):
    """
    Tests POST a request with missing data for creating a vault.
    """
    app, client = app_client

    # Mock login
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_info"] = {"firstname": "Max"}

    res = client.post("/settings/create_vault",
                      data={},
                      follow_redirects=True)

    assert res.status_code == 200
    html = res.get_data(as_text=True)
    assert "Please fill out the required form fields." in html


def test_post_create_vault_successful(app_client):
    """
    Tests POST a valid request for creating a vault.
    """
    app, client = app_client

    # Mock login
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_info"] = {"firstname": "Max"}

    with patch("src.services.VaultManagement.create_vault") as mock_vault:
        res = client.post("/settings/create_vault",
                          data={
                              "duration": 10,
                              "start": "2025-07-01"
                          },
                          follow_redirects=True)

        assert res.status_code == 200
        mock_vault.assert_called_once()


def test_create_vault_exception_handeling(app_client):
    """
    Test exception handeling.
    """
    app, client = app_client

    # Mock login
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_info"] = {"firstname": "Max"}

    with patch("src.routes.settings.VaultManagement.create_vault", side_effect=RuntimeError):
        res = client.post("/settings/create_vault",
                          data={
                              "duration": 10,
                              "start": "2025-07-01"
                          })

        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert "Please contact an admin to get furhter insights into this error." in html


# ------------------- /settings/join_family -------------------

def test_post_join_family_not_logged_in(app_client):
    """
    Tests redirect to get settings page when no user is logged in.
    """
    app, client = app_client

    res = client.post("/settings/join_family")
    assert res.status_code == 302
    assert '/login' in res.location


def test_post_join_family_invalid_invite_code(app_client):
    """
    Test POST to join family with invalid invite code.
    """
    app, client = app_client

    # Mock login
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_info"] = {"firstname": "Max"}

    with patch("src.routes.settings.UserManagement.join_family", side_effect=UserException("Testing Error")):
        res = client.post("/settings/join_family",
                          follow_redirects=True)

        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert "Testing Error" in html


def test_post_join_family_successful(app_client):
    """
    Test POST to join family with valid invite code.
    """
    app, client = app_client

    # Mock login
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_info"] = {"firstname": "Max"}

    fake_family_info = {
        "family_name": "Doe",
        "invite_code": "abc",
        "number_members": 2,
        "members": ["a", "b"]
    }
    fake_vault_info = {
        "days_left": 10,
        "period_duration": 6,
        "curr_period_end": "Friday, 26 March 2025"
    }

    with patch("src.routes.settings.UserManagement.join_family", return_value=2), \
        patch("src.routes.settings.UserManagement.get_family_info", return_value=fake_family_info), \
        patch("src.routes.settings.VaultManagement.get_vault_info", return_value=fake_vault_info), \
            patch("src.routes.settings.VaultManagement.get_number_memories", return_value=10):
        res = client.post("/settings/join_family",
                          data={
                              "invite_code": "piaskjdaosikdm"
                          },
                          follow_redirects=True)

        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert "Successfully joined family" in html


def test_join_family_exception_handeling(app_client):
    """
    Test exception handeling.
    """
    app, client = app_client

    # Mock login
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_info"] = {"firstname": "Max"}

    with patch("src.routes.settings.UserManagement.join_family", side_effect=RuntimeError):
        res = client.post("/settings/join_family",
                          data={
                              "invite_code": "piaskjdaosikdm"
                          })

        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert "Please contact an admin to get furhter insights into this error." in html

# ------------------- /settings/create_family -------------------


def test_post_create_family_not_logged_in(app_client):
    """
    Tests redirect to get settings page when no user is logged in.
    """
    app, client = app_client

    res = client.post("/settings/create_family")
    assert res.status_code == 302
    assert '/login' in res.location


def test_post_create_family_already_in_family(app_client):
    """
    Test POST to create family while user is already part of a family.
    """
    app, client = app_client

    # Mock login
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_info"] = {"firstname": "Max"}
        session["family_vault_info"] = {"test": "a"}

    res = client.post("/settings/create_family",
                      follow_redirects=True)

    assert res.status_code == 200
    html = res.get_data(as_text=True)
    assert "You are already part of a family." in html


def test_post_create_family_successful(app_client):
    """
    Test POST to create a family with valid request data.
    """
    app, client = app_client

    fake_user_info = {
        "firstname": "Max",
        "family_id": 5
    }
    fake_family_info = {
        "family_name": "Doe",
        "invite_code": "abc",
        "number_members": 2,
        "members": ["a", "b"]
    }
    fake_vault_info = {
        "days_left": 10,
        "period_duration": 6,
        "curr_period_end": "Friday, 26 March 2025"
    }

    # Mock login
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_info"] = fake_user_info

    with patch("src.routes.settings.UserManagement.get_user_info", return_value=fake_user_info), \
        patch("src.routes.settings.UserManagement.create_family", return_value=2), \
        patch("src.services.VaultManagement.create_vault") as mock_vault, \
        patch("src.routes.settings.UserManagement.get_family_info", return_value=fake_family_info), \
        patch("src.routes.settings.VaultManagement.get_vault_info", return_value=fake_vault_info), \
            patch("src.routes.settings.VaultManagement.get_number_memories", return_value=10):
        res = client.post("/settings/create_family",
                          data={
                              "duration": "6",
                              "start": "2025-07-01"
                          },
                          follow_redirects=True)

        assert res.status_code == 200
        mock_vault.assert_called_once()
        html = res.get_data(as_text=True)
        assert "Family Information" in html
        assert "Family Vault Information" in html


def test_create_family_exception_handeling(app_client):
    """
    Test exception handeling.
    """
    app, client = app_client

    # Mock login
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_info"] = {"firstname": "Max"}

    with patch("src.routes.settings.UserManagement.create_family", side_effect=RuntimeError):
        res = client.post("/settings/create_family")

        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert "Please contact an admin to get furhter insights into this error." in html


# ------------------- /settings/create_family -------------------

def test_post_quit_family_not_logged_in(app_client):
    """
    Tests redirect to get settings page when no user is logged in.
    """
    app, client = app_client

    res = client.post("/settings/quit_family")
    assert res.status_code == 302
    assert '/login' in res.location


def test_post_quit_family_not_in_family(app_client):
    """
    Test POST to quit family while user is no part of a family.
    """
    app, client = app_client

    # Mock login
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_info"] = {"firstname": "Max"}

    res = client.post("/settings/quit_family",
                      follow_redirects=True)

    assert res.status_code == 200
    html = res.get_data(as_text=True)
    assert "You are not part of a family." in html


def test_post_quit_family_successful(app_client):
    """
    Test POST to quit family.
    """
    app, client = app_client

    fake_user_info = {
        "firstname": "Max",
        "family_id": 5
    }

    # Mock login
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_info"] = fake_user_info
        session["family_vault_info"] = {"test": "a"}

    with patch("src.routes.settings.UserManagement.quit_family") as mock_family_quit, \
            patch("src.routes.settings.UserManagement.get_user_info", return_value=fake_user_info):
        res = client.post("/settings/quit_family",
                          follow_redirects=True)

        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert "Successfully quit family." in html
        assert session.get("family_vault_info", False)


def test_create_family_exception_handeling(app_client):
    """
    Test exception handeling.
    """
    app, client = app_client

    # Mock login
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_info"] = {"firstname": "Max"}
        session["family_vault_info"] = {"test": "a"}

    with patch("src.routes.settings.UserManagement.quit_family", side_effect=RuntimeError):
        res = client.post("/settings/quit_family")

        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert "Please contact an admin to get furhter insights into this error." in html
