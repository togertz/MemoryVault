def test_get_index_not_logged_in(app_client):
    """
    Tests redirect to get login page when no user is logged in.
    """
    app, client = app_client

    res = client.get("/")
    assert res.status_code == 302
    assert '/login' in res.location


def test_get_index_logged_in(app_client):
    """
    Tests redirect to get memory upload page when user is logged in.
    """
    app, client = app_client

    # Mock login
    with client.session_transaction() as session:
        session["user_id"] = 1

    res = client.get("/")
    assert res.status_code == 302
    assert '/memory' in res.location
