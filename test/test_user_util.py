import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime

from src.memoryvault.services import UserManagement, UserException


@pytest.fixture
def user_mock():
    user = MagicMock()
    user.id = 1
    user.username = "testuser"
    user.password_hash = "abcd"
    user.firstname = "John"
    user.lastname = "Doe"
    user.birthday = datetime(2010, 7, 1).date()
    user.is_admin = False
    user.family_id = None
    user.json_package.return_value = {"id": 1, "username": "testuser"}
    return user


@pytest.fixture
def family_mock():
    family = MagicMock()
    family.id = 1
    family.name = "Doe"
    family.invite_code = "ABCD"
    family.json_package.return_value = {"id": 1, "family_name": "Doe"}
    return family


@patch("src.memoryvault.services.user_util.db")
@patch("src.memoryvault.services.user_util.User")
@patch("src.memoryvault.services.user_util.bcrypt_app")
@patch("src.memoryvault.services.user_util.UserManagement.username_taken", return_value=False)
def test_create_user_successful(mock_taken, mock_bcrypt, mock_user_cls, mock_db, user_mock):
    """
    Tests to create a user.
    """
    mock_user_cls.return_value = user_mock
    mock_bcrypt.generate_password_hash.return_value = b"abcd"

    result = UserManagement.create_user(
        username="alice",
        password="defg",
        password_repeat="defg",
        firstname="Alice",
        lastname="Doe",
        birthday="2011-04-12",
    )

    assert result is True
    mock_db.session.add.assert_called_once_with(user_mock)
    mock_db.session.commit.assert_called()


@patch("src.memoryvault.services.user_util.UserManagement.username_taken", return_value=True)
def test_create_user_username_taken(mock_taken):
    """
    Tests to create a user with a taken username. Expects UserException.
    """
    with pytest.raises(UserException) as exc:
        UserManagement.create_user(
            username="alice",
            password="defg",
            password_repeat="defg",
            firstname="Alice",
            lastname="Doe",
            birthday="2011-04-12",
        )
    assert "Username already exists" in exc.value.get_message()


@patch("src.memoryvault.services.user_util.UserManagement.username_taken", return_value=False)
def test_create_user_different_passwords(mock_taken):
    """
    Tests to create a user with mismatching passwords. Expects UserException.
    """
    with pytest.raises(UserException) as exc:
        UserManagement.create_user(
            username="alice",
            password="defg",
            password_repeat="hjik",
            firstname="Alice",
            lastname="Doe",
            birthday="2011-04-12",
        )
    assert "No user was created. Password and repeated password need to be the same" in exc.value.get_message()


@patch("src.memoryvault.services.user_util.User")
@patch("src.memoryvault.services.user_util.bcrypt_app")
@patch("src.memoryvault.services.user_util.UserManagement.username_taken", return_value=True)
def test_check_login_successful(mock_taken, mock_bcrypt, mock_user_cls, user_mock):
    """
    Tests a successful login attempt.
    """
    mock_user_cls.query.filter_by.return_value.first.return_value = user_mock
    mock_bcrypt.check_password_hash.return_value = True

    assert UserManagement.check_login("John", "abc") == user_mock.id


@patch("src.memoryvault.services.user_util.db")
@patch("src.memoryvault.services.user_util.User")
@patch("src.memoryvault.services.user_util.Family")
def test_create_family_successful(mock_family_cls, mock_user_cls, mock_db, family_mock, user_mock):
    """
    Tests creating a family.
    """
    mock_family_cls.return_value = family_mock
    mock_user_cls.query.filter_by.return_value.first.return_value = user_mock

    result = UserManagement.create_family(
        user_id=user_mock.id,
        family_name="Doe"
    )

    assert isinstance(result, int)
    mock_db.session.add.assert_called_once_with(family_mock)
    mock_db.session.commit.assert_called()


@patch("src.memoryvault.services.user_util.db")
@patch("src.memoryvault.services.user_util.User")
@patch("src.memoryvault.services.user_util.Family")
def test_join_family_successful(mock_family_cls, mock_user_cls, mock_db, family_mock, user_mock):
    """
    Tests to join a family.
    """
    mock_family_cls.query.filter_by.return_value.first.return_value = family_mock
    mock_user_cls.query.filter_by.return_value.first.return_value = user_mock

    UserManagement.join_family(
        user_id=1,
        invite_code="something"
    )

    mock_db.session.commit.assert_called()
    assert user_mock.family_id == family_mock.id


@patch("src.memoryvault.services.user_util.Family")
def test_join_family_invalid_invite_code(mock_family_cls):
    """
    Tests to join a family with an invalid invite code.
    """
    mock_family_cls.query.filter_by.return_value.first.return_value = None

    with pytest.raises(UserException) as exc:
        UserManagement.join_family(
            user_id=1,
            invite_code="something"
        )
    assert "No family with this invite code could be found." in exc.value.get_message()


@patch("src.memoryvault.services.user_util.User")
@patch("src.memoryvault.services.user_util.Family")
def test_join_family_invalid_user_id(mock_family_cls, mock_user_cls, family_mock):
    """
    Tests to join a family by using an invalid user_id.
    """
    mock_family_cls.query.filter_by.return_value.first.return_value = family_mock
    mock_user_cls.query.filter_by.return_value.first.return_value = None

    with pytest.raises(UserException) as exc:
        UserManagement.join_family(
            user_id=1,
            invite_code="something"
        )
    assert "User could not be found." in exc.value.get_message()


@patch("src.memoryvault.services.user_util.db")
@patch("src.memoryvault.services.user_util.User")
def test_quit_family_successful(mock_user_cls, mock_db, family_mock, user_mock):
    """
    Tests to quit a family.
    """
    mock_user_cls.query.filter_by.return_value.first.return_value = user_mock

    UserManagement.quit_family(user_id=1)

    mock_db.session.commit.assert_called()
    assert user_mock.family_id == None


@patch("src.memoryvault.services.user_util.User")
def test_quit_family_invalid_user_id(mock_user_cls):
    """
    Tests to quit a family with an invalid user id.
    """
    mock_user_cls.query.filter_by.return_value.first.return_value = None

    with pytest.raises(UserException) as exc:
        UserManagement.quit_family(user_id=1)

    assert "User could not be found." in exc.value.get_message()


@patch("src.memoryvault.services.user_util.Family")
def test_get_family_info_successful(mock_family_cls, family_mock):
    """
    Tests retrieving family information.
    """
    mock_family_cls.query.filter_by.return_value.first.return_value = family_mock

    result = UserManagement.get_family_info(family_id=1)

    assert isinstance(result, dict)
    assert result["id"] == 1
    assert result["family_name"] == "Doe"


@patch("src.memoryvault.services.user_util.Family")
def test_get_family_info_no_family_found(mock_family_cls):
    """
    Tests retrieving family information with an invalid family id.
    """
    mock_family_cls.query.filter_by.return_value.first.return_value = None

    with pytest.raises(UserException) as exc:
        UserManagement.get_family_info(family_id=1)
    assert "Family could not be found." in exc.value.get_message()
