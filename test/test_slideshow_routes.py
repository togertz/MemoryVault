from datetime import datetime
from unittest.mock import patch

# ------------------- /slideshow/ -------------------


def test_get_index_not_logged_in(app_client):
    """
    Tests redirect to get login page when no user is logged in.
    """
    app, client = app_client

    res = client.get("/slideshow/")
    assert res.status_code == 302
    assert '/login' in res.location


def test_get_index_no_vault_configured(app_client):
    """
    Tests GET on slideshow to retrieve HTML page without a vault configured.
    """
    app, client = app_client

    # Mock login
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_info"] = {"firstname": "Max", "admin": False}

    res = client.get("/slideshow", follow_redirects=True)

    assert res.status_code == 200
    html = res.get_data(as_text=True)
    assert "There is currently no Slideshow for you available." in html


def test_get_index_with_private_vault(app_client):
    """
    Tests GET on slideshow to retrieve HTML page without a vault configured.
    """
    app, client = app_client

    # Mock login
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_info"] = {"firstname": "Max", "admin": False}
        session["vault_info"] = {"vault_id": 1}

    fake_periods = [
        {"period_start": "Tuesday, 1 July 2025",
         "period_end": "Thursday, 31 July 2025"},
        {"period_start": "Friday, 1 August 2025",
         "period_end": "Sunday, 31 August 2025"},
    ]

    with patch("src.memoryvault.routes.slideshow.VaultManagement.get_all_periods", return_value=fake_periods):
        res = client.get("/slideshow", follow_redirects=True)

        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert "Choose the Collection Period:" in html
        assert "Own vault" in html
        assert "Family vault" not in html


def test_get_index_with_private_and_family_vault(app_client):
    """
    Tests GET on slideshow to retrieve HTML page without a vault configured.
    """
    app, client = app_client

    # Mock login
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_info"] = {"firstname": "Max", "admin": False}
        session["vault_info"] = {"vault_id": 1}
        session["family_vault_info"] = {"vault_id": 2}

    fake_periods = [
        {"period_start": "Tuesday, 1 July 2025",
         "period_end": "Thursday, 31 July 2025"},
        {"period_start": "Friday, 1 August 2025",
         "period_end": "Sunday, 31 August 2025"},
    ]

    with patch("src.memoryvault.routes.slideshow.VaultManagement.get_all_periods", return_value=fake_periods):
        res = client.get("/slideshow", follow_redirects=True)

        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert "Choose the Collection Period:" in html
        assert "Own vault" in html
        assert "Family vault" in html


def test_index_exception_handeling(app_client):
    """
    Test exception handeling.
    """
    app, client = app_client

    # Mock login
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_info"] = {"firstname": "Max", "admin": False}
        session["vault_info"] = {"vault_id": 1}

    with patch("src.memoryvault.routes.slideshow.VaultManagement.get_all_periods", side_effect=Exception):
        res = client.get("/slideshow/")

        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert "Please contact an admin to get furhter insights into this error." in html

# ------------------- /slideshow/run -------------------


def test_get_run_not_logged_in(app_client):
    """
    Tests redirect to get login page when no user is logged in.
    """
    app, client = app_client

    res = client.get("/slideshow/run")
    assert res.status_code == 302
    assert '/login' in res.location


def test_run_exception_handeling(app_client):
    """
    Test exception handeling.
    """
    app, client = app_client

    # Mock login
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_info"] = {"firstname": "Max", "admin": False}
        session["vault_info"] = {"vault_id": 1}

    with patch("src.memoryvault.routes.slideshow.MemoryManagement.get_memory_data", side_effect=Exception):
        res = client.get("/slideshow/run?number=3")

        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert "Please contact an admin to get furhter insights into this error." in html


def test_post_run_start_slideshow_no_memories(app_client):
    """
    Test POST to start slideshow of private vault.
    """
    app, client = app_client

    # Mock login
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_info"] = {"firstname": "Max", "admin": False}
        session["vault_info"] = {"vault_id": 1}

    with patch("src.memoryvault.routes.slideshow.MemoryManagement.get_slideshow_order", return_value=[]):
        res = client.post("/slideshow/run",
                          data={
                              "vault": "own_vault",
                              "order": "chronological",
                              "collection-period": "Friday, Aug 1, 2025-Sunday, Aug 31, 2025"
                          },
                          follow_redirects=True)

        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert "No memories were found for this collection period" in html


def test_post_run_start_slideshow(app_client):
    """
    Test POST to start slideshow of private vault.
    """
    app, client = app_client

    # Mock login
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_info"] = {"firstname": "Max", "admin": False}
        session["vault_info"] = {"vault_id": 1}

    fake_memory = {
        "description": "Test description of a memory",
        "date": datetime(year=2025, month=8, day=2).date(),
        "image_uri": None,
        "latitude": None,
        "longitude": None
    }
    with patch("src.memoryvault.routes.slideshow.MemoryManagement.get_slideshow_order", return_value=[1, 2, 3, 4]), \
            patch("src.memoryvault.routes.slideshow.MemoryManagement.get_memory_data", return_value=fake_memory):
        res = client.post("/slideshow/run",
                          data={
                              "vault": "own_vault",
                              "order": "chronological",
                              "collection-period": "Friday, Aug 1, 2025-Sunday, Aug 31, 2025"
                          },
                          follow_redirects=True)

        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert "Saturday, Aug 02, 2025" in html
        assert fake_memory["description"] in html


def test_get_run_next_slide(app_client):
    """
    Test GET on run to access next slide in slideshow.
    """
    app, client = app_client

    # Mock login
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_info"] = {"firstname": "Max", "admin": True}
        session["vault_info"] = {"vault_id": 1}
        session["slideshow_order"] = [1, 2, 3, 4]

    fake_memory = {
        "description": "Test description of a second memory",
        "date": datetime(year=2025, month=8, day=3).date(),
        "image_uri": None,
        "latitude": None,
        "longitude": None
    }

    with patch("src.memoryvault.routes.slideshow.MemoryManagement.get_memory_data", return_value=fake_memory):
        res = client.get("/slideshow/run?number=2")

        assert res.status_code == 200
        html = res.get_data(as_text=True)
        print(html)
        assert "Sunday, Aug 03, 2025" in html
        assert fake_memory["description"] in html
