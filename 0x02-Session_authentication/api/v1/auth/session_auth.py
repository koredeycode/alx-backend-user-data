#!/usr/bin/env python3
"""
Class to manage the Basic authentication
"""

# from flask import request
from typing import TypeVar
from api.v1.auth.auth import Auth
# import base64
from models.user import User
import uuid


class SessionAuth(Auth):
    """
    The Session Authentication class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        creates a session ID for a user_Id
        """
        if user_id is None or type(user_id) is not str:
            return None
        session_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        returns a User Id based on a session id
        """
        if session_id is None or type(session_id) is not str:
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        returns a User based on a cookie value
        """
        cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie)
        return User.get(user_id)
