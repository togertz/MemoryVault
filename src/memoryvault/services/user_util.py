"""
Module containing utility classes for user management.
"""
import random
import hashlib
from abc import ABC
from datetime import datetime

from ..models import db, User, Family
from ..app import bcrypt_app


class UserException(Exception):
    """
    Custom Exception for invalid user registration and management.
    """

    def __init__(self, message: str, *args):
        super().__init__(*args)
        self.message = message

    def get_message(self) -> str:
        """
        Returns error message.
        """
        return self.message


class LoginException(Exception):
    """
    Custom Exception for invalid login input.
    """

    def __init__(self, message: str, *args):
        super().__init__(*args)
        self.message = message

    def get_message(self) -> str:
        """
        Returns error message.
        """
        return self.message


class UserManagement(ABC):
    """
    Utility class for user registration and logins.
    """
    @staticmethod
    def create_user(username: str,
                    password: str,
                    password_repeat: str,
                    firstname: str,
                    lastname: str,
                    birthday: str,
                    admin_token: str = None) -> bool:
        """
        Creates user and stores his information in a database.

        Parameters:
            username: str
            password: str
                The password of the user
            password_repeat: str
                The repitition of the password to avoid typing misstakes of the user.
                Must be the same value as the password.
            firstname: str
            lastname: str
            birthday: str
                The users birthday in "%Y-%m-%d" format.
            admin_token: str
                The hard coded admin token to grant a user admin privileges.
                Must be correct, otherwise no user will be created.

        Returns:
            bool: Is true if user was created sucessfully.
        """
        # -- Check if username is already taken --
        if UserManagement.username_taken(username):
            raise UserException(
                message="No user was created. Username already exists")

        # -- Check if password and password repeat have same values.
        if password != password_repeat:
            raise UserException(
                message="No user was created. Password and repeated password need to be the same")

        # -- Check if admin token is correct and grant admin privilieges --
        is_admin = False
        if admin_token:
            if admin_token == "9264b8a1-2147-4f6c-8401-1d55ac60c644":
                is_admin = True
            else:
                raise UserException(
                    "No user was created. Admin token is not valid.")

        # -- Process and parse login information --
        username = username.lower()
        password_hash = bcrypt_app.generate_password_hash(
            password=password).decode('utf-8')
        birthday = datetime.strptime(birthday, '%Y-%m-%d').date()

        # -- Create user in db --
        new_user = User(username=username,
                        password_hash=password_hash,
                        firstname=firstname,
                        lastname=lastname,
                        birthday=birthday,
                        is_admin=is_admin)
        db.session.add(new_user)
        db.session.commit()

        return True

    @staticmethod
    def username_taken(username: str) -> bool:
        """
        Returns whether a username is already taken by another user.

        Parameters:
            username: str
                The username to check availability

        Returns:
            bool: indicating whether username is taken.
        """
        username = username.lower()

        usernames = db.session.query(User.username).all()
        usernames = [u[0] for u in usernames]

        return username in usernames

    @staticmethod
    def check_login(username: str, password: str) -> str:
        """
        Checks whether login input is valid and the requested user exists.

        Parameters:
            username: str
            password: str

        Returns:
            int: user id if username and password are valid
            None: else
        """
        if not UserManagement.username_taken(username=username):
            return False

        user = User.query.filter_by(username=username).first()

        valid_login = bcrypt_app.check_password_hash(
            user.password_hash, password)

        return user.id if valid_login else None

    @staticmethod
    def get_user_info(user_id: int) -> dict:
        """
        Returns the user information as dict.

        Parameters:
            user_id: int

        Returns:
            dict: the users information
        """
        user = User.query.filter_by(id=user_id).first()

        return user.json_package()

    @staticmethod
    def create_family(user_id: int,
                      family_name: str,
                      ) -> int:
        """
        Creates family and adds the user as member of a family.

        Parameters:
            user_id: int
                The user id of the user creating the family
            family_name: str
                The name of the family

        Returns:
            int: id of the newly created family
        """
        # -- Generating invite code for new family --
        invite_code = f"{random.randint(0, 1000)}_{family_name}"
        invite_code = hashlib.sha256(invite_code.encode("utf-8")).hexdigest()

        # -- Creating family in db --
        new_family = Family(
            family_name=family_name,
            invite_code=invite_code
        )
        db.session.add(new_family)
        db.session.commit()

        # -- Adding user to new family --
        user = User.query.filter_by(id=user_id).first()
        user.family_id = new_family.id
        db.session.commit()

        return new_family.id

    @staticmethod
    def join_family(user_id: int,
                    invite_code: str
                    ):
        """
        Adds user as new member of the family

        Parameters:
            user_id: int
                The user id joining the family
            family_name: str
                The name of the family

        Returns:
            int: id of the joined family
        """
        # -- Searching for family with given invite code --
        family = Family.query.filter_by(invite_code=invite_code).first()
        if family is None:
            raise UserException(
                "No family with this invite code could be found.")

        # -- Adding user to family --
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            raise UserException("User could not be found.")
        user.family_id = family.id
        db.session.commit()
        return family.id

    @staticmethod
    def quit_family(user_id: int) -> None:
        """
        Removes user as member of the family

        Parameters:
            user_id: int
                The user id leaving the family

        Returns:
            None
        """
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            raise UserException("User could not be found.")

        user.family_id = None
        db.session.commit()

    @staticmethod
    def get_family_info(family_id):
        """
        Returns the family information as dict.

        Parameters:
            family_id: int

        Returns:
            dict: the family information
        """
        family = Family.query.filter_by(id=family_id).first()
        if family is None:
            raise UserException("Family could not be found.")

        return family.json_package()
