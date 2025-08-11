import pytest
from unittest.mock import patch

# ------------------- /u/login/ -------------------


def test_get_login_already_logged_in(app_client):
    """
    Tests redirect to upload page when user is already logged in.
    """
    app, client = app_client

    # Mock login
    with client.session_transaction() as session:
        session["user_id"] = 1

    res = client.get("/u/login")
    assert res.status_code == 302
    assert '/memory' in res.location


def test_get_login_page(app_client):
    """
    Tests GET login html page.
    """
    app, client = app_client

    res = client.get("/u/login")
    assert res.status_code == 200
    html = res.get_data(as_text=True)
    assert "No account yet?" in html


def test_post_login_wrong_password(app_client):
    """
    Tests POST login with valid wrong password.
    """
    app, client = app_client

    with patch("src.routes.user.UserManagement.check_login", return_value=None), \
            patch("src.routes.user.UserManagement.username_taken", return_value=True):
        res = client.post("/u/login",
                          data={"username": "admin", "password": "admin"},
                          follow_redirects=True)

        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert "Wrong password" in html


def test_post_login_user_not_exists(app_client):
    """
    Tests POST login with not existing user.
    """
    app, client = app_client

    with patch("src.routes.user.UserManagement.check_login", return_value=None), \
            patch("src.routes.user.UserManagement.username_taken", return_value=False):
        res = client.post("/u/login",
                          data={"username": "admin", "password": "admin"},
                          follow_redirects=True)

        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert "User does not exist" in html


def test_post_login_successful(app_client):
    """
    Tests POST login with valid credentials.
    """
    app, client = app_client

    fake_user_info = {"firstname": "Max"}
    fake_vault_info = {"days_left": 10, "period_duration": 6,
                       "curr_period_end": "Friday, 26 March 2025"}

    with patch("src.routes.user.UserManagement.check_login", return_value=1), \
            patch("src.routes.user.UserManagement.get_user_info", return_value=fake_user_info), \
            patch("src.routes.user.VaultManagement.get_vault_info", return_value=fake_vault_info):
        res = client.post("/u/login",
                          data={"username": "admin", "password": "admin"},
                          follow_redirects=True)

        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert "Successfully logged in" in html


def test_login_exception_handeling(app_client):
    """
    Test exception handeling.
    """
    app, client = app_client

    with patch("src.routes.settings.UserManagement.check_login", side_effect=RuntimeError):
        res = client.post("/u/login",
                          data={"username": "admin", "password": "admin"})

        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert "Please contact an admin to get furhter insights into this error." in html

# ------------------- /u/logout/ -------------------


def test_get_logout_not_logged_in(app_client):
    """
    Tests redirect to login page when user is not logged in.
    """
    app, client = app_client

    res = client.get("/u/logout")
    assert res.status_code == 302
    assert '/login' in res.location


def test_get_logout_successful(app_client):
    """
    Tests GET for successful logout.
    """
    app, client = app_client

    # Mock login
    with client.session_transaction() as session:
        session["user_id"] = 1

    res = client.get("/u/logout",
                     follow_redirects=True)

    assert res.status_code == 200
    html = res.get_data(as_text=True)
    assert "Successfully logged out" in html

# ------------------- /u/logout/ -------------------


def test_get_register_already_logged_in(app_client):
    """
    Tests redirect to upload page when user is already logged in.
    """
    app, client = app_client

    # Mock login
    with client.session_transaction() as session:
        session["user_id"] = 1

    res = client.get("/u/register")
    assert res.status_code == 302
    assert '/memory' in res.location


def test_get_register_page(app_client):
    """
    Tests GET register html page.
    """
    app, client = app_client

    res = client.get("/u/register")
    assert res.status_code == 200
    html = res.get_data(as_text=True)
    assert "Create a new user" in html


def test_post_register_successful(app_client):
    """
    Tests POST register with valid user information.
    """
    app, client = app_client

    with patch("src.routes.user.UserManagement.create_user") as mock_register:
        res = client.post("/u/register",
                          data={
                              "username": "admin",
                              "password": "1234",
                              "password-repeat": "1234",
                              "firstname": "John",
                              "lastname": "Doe",
                              "birthday": "2025-01-01"
                          })

        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert "User was created. Please login:" in html


def test_register_exception_handeling(app_client):
    """
    Test exception handeling.
    """
    app, client = app_client

    with patch("src.routes.settings.UserManagement.create_user", side_effect=RuntimeError):
        res = client.post("/u/register",
                          data={
                              "username": "admin",
                              "password": "1234",
                              "password-repeat": "1234",
                              "firstname": "John",
                              "lastname": "Doe",
                              "birthday": "2025-01-01"
                          })

        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert "Please contact an admin to get furhter insights into this error." in html

# ------------------- /u/username-taken/ -------------------


def test_get_username_taken(app_client):
    """
    Test GET on username taken endpoint.
    """
    app, client = app_client

    with patch("src.routes.user.UserManagement.username_taken", return_value=False):
        res = client.get("/u/username-taken?username=admin")

        assert res.status_code == 200
        assert res.json == {"exists": False}
