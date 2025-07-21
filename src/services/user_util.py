from abc import ABC
from datetime import datetime

from ..models import db, User
from ..app import bcrypt_app

class UserException(Exception):
    def __init__(self, message:str, *args):
        super().__init__(*args)
        self.message = message

    def get_message(self) -> str:
        return self.message

class LoginException(Exception):
    def __init__(self, message:str, *args):
        super().__init__(*args)
        self.message = message

    def get_message(self) -> str:
        return self.message

class UserManagement(ABC):

    @staticmethod
    def create_user(username:str,
                    password:str,
                    password_repeat:str,
                    firstname:str,
                    lastname:str,
                    birthday:str) -> bool:

        if UserManagement.username_taken(username):
            raise UserException(message="No user was created. Username already exists")

        if password != password_repeat:
            raise UserException(message="No user was created. Password and repeated password need to be the same")

        username = username.lower()
        password_hash = UserManagement.hash_password(password)
        birthday = datetime.strptime(birthday, '%Y-%m-%d').date()

        new_user = User(username=username,
                        password_hash=password_hash,
                        firstname=firstname,
                        lastname=lastname,
                        birthday=birthday)
        db.session.add(new_user)
        db.session.commit()

        return True

    @staticmethod
    def username_taken(username:str) -> bool:
        username = username.lower()

        usernames = db.session.query(User.username).all()
        usernames = [u[0] for u in usernames]

        return username in usernames

    @staticmethod
    def hash_password(password:str) -> str:
        return bcrypt_app.generate_password_hash(password=password).decode('utf-8')

    @staticmethod
    def check_login(username:str, password:str) -> str:
        if not UserManagement.username_taken(username=username):
            return False

        user = User.query.filter_by(username=username).first()

        validLogin = bcrypt_app.check_password_hash(user.password_hash, password)

        return user.id if validLogin else None

    @staticmethod
    def get_user_json_package(user_id):
        user = User.query.filter_by(id=user_id).first()

        return user.json_package()
