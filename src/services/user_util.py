import random
import hashlib
from abc import ABC
from datetime import datetime

from ..models import db, User, Family
from ..app import bcrypt_app


class UserException(Exception):
    def __init__(self, message: str, *args):
        super().__init__(*args)
        self.message = message

    def get_message(self) -> str:
        return self.message


class LoginException(Exception):
    def __init__(self, message: str, *args):
        super().__init__(*args)
        self.message = message

    def get_message(self) -> str:
        return self.message


class UserManagement(ABC):

    @staticmethod
    def create_user(username: str,
                    password: str,
                    password_repeat: str,
                    firstname: str,
                    lastname: str,
                    birthday: str,
                    admin_token: str = None) -> bool:

        if UserManagement.username_taken(username):
            raise UserException(
                message="No user was created. Username already exists")

        if password != password_repeat:
            raise UserException(
                message="No user was created. Password and repeated password need to be the same")

        is_admin = False
        if admin_token:
            if admin_token == "9264b8a1-2147-4f6c-8401-1d55ac60c644":
                is_admin = True
            else:
                raise UserException(
                    "No user was created. Admin token is not valid.")

        username = username.lower()
        password_hash = UserManagement.hash_password(password)
        birthday = datetime.strptime(birthday, '%Y-%m-%d').date()

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
        username = username.lower()

        usernames = db.session.query(User.username).all()
        usernames = [u[0] for u in usernames]

        return username in usernames

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt_app.generate_password_hash(password=password).decode('utf-8')

    @staticmethod
    def check_login(username: str, password: str) -> str:
        if not UserManagement.username_taken(username=username):
            return False

        user = User.query.filter_by(username=username).first()

        valid_login = bcrypt_app.check_password_hash(
            user.password_hash, password)

        return user.id if valid_login else None

    @staticmethod
    def get_user_json_package(user_id):
        user = User.query.filter_by(id=user_id).first()

        return user.json_package()

    @staticmethod
    def create_family(user_id,
                      family_name,
                      ):
        invite_code = f"{random.randint(0, 1000)}_{family_name}"
        invite_code = hashlib.sha256(invite_code.encode("utf-8")).hexdigest()

        new_family = Family(
            family_name=family_name,
            invite_code=invite_code
        )
        db.session.add(new_family)
        db.session.commit()

        user = User.query.filter_by(id=user_id).first()
        user.family_id = new_family.id
        db.session.commit()

        return new_family.id

    @staticmethod
    def join_family(user_id,
                    invite_code: str
                    ):
        family = Family.query.filter_by(invite_code=invite_code).first()
        if family is None:
            raise UserException(
                "No family with this invite code could be found.")

        user = User.query.filter_by(id=user_id).first()
        if user is None:
            raise UserException("User could not be found.")
        user.family_id = family.id
        db.session.commit()
        return family.id

    @staticmethod
    def quit_family(user_id):
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            raise UserException("User could not be found.")

        user.family_id = None
        db.session.commit()
        return True

    @staticmethod
    def get_family_info(family_id):
        family = Family.query.filter_by(id=family_id).first()
        if family is None:
            raise UserException("Family could not be found.")

        return family.json_package()
