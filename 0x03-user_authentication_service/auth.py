#!/usr/bin/env python3
"""
the auth module
"""
import bcrypt
from db import DB
from user import User
from typing import TypeVar
import uuid
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    return the bytes of the salted hash of the password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> TypeVar("User"):
        """
        register a user to the database
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            user = self._db.add_user(email, hashed_pwd)
            return user
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """
        check if it is valid login
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return False
        return bcrypt.checkpw(password.encode(), user.hashed_password)

    def _generate_uuid(self) -> str:
        """
        generate a new uuid
        """
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """
        create a session with id
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return
        session_id = self._generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> TypeVar('User'):
        """
        find a user with the session_id
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        destroy the user with the user_id session
        """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        return a user reset token
        """
        try:
            user = self._db.find_user_by(email=email)
            if user is None:
                raise ValueError
            token = self._generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        except Exception:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        update the password of the user with the reset token
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            if user is None:
                raise ValueError
            pwd = _hash_password(password)
            self._db.update_user(user.id, hashed_password=pwd,
                                 reset_token=None)
        except Exception:
            raise ValueError
