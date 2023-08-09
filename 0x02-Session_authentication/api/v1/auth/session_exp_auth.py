#!/usr/bin/env python3
"""
Class to manage the Basic authentication
"""

from typing import TypeVar
from api.v1.auth.session_auth import SessionAuth
from models.user import User
import uuid
from datetime import datetime
from os import getenv


class SessionExpAuth(SessionAuth):
    """
    The Session Expiration Authentication class
    """
    def __init__(self):
        """
        overload the init method
        """
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
            print(self.session_duration)
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        overload the create_session method
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {}
        session_dictionary['user_id'] = user_id
        session_dictionary['created_at'] = datetime.now()
        SessionExpAuth.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        overload the user_id_for_session_id method
        """
        if session_id is None:
            return None
        session_dict = SessionExpAuth.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None
        if self.session_duration <= 0:
            return session_dict.get('user_id')
        created_at = session_dict.get('created_at')
        if created_at is None:
            return None
        lapse = datetime.now() - created_at
        if lapse.seconds > self.session_duration:
            return None
        return session_dict.get('user_id')
