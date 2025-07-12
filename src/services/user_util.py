from abc import ABC
from datetime import datetime
from flask_bcrypt import Bcrypt

from ..models import db, User
from ..app import bcrypt_app

class UserException(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class LoginException(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class UserManagement(ABC):

    @staticmethod
    def create_user(username:str,
                    password:str,
                    firstname:str,
                    lastname:str,
                    birthday:str) -> bool:

        if UserManagement.username_taken(username):
            raise UserException("Username already exists")

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

    def username_taken(username:str) -> bool:
        username = username.lower()

        usernames = db.session.query(User.username).all()
        usernames = [u[0] for u in usernames]

        return username in usernames

    def hash_password(password:str) -> str:
        return bcrypt_app.generate_password_hash(password=password).decode('utf-8')

    def check_login(username:str, password:str) -> str:
        if not UserManagement.username_taken(username=username):
            return False

        user = User.query.filter_by(username=username).first()

        return bcrypt_app.check_password_hash(user.password_hash, password)