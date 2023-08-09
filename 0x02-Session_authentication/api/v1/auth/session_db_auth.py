#!/usr/bin/env python3
"""
Class to manage the SessionDB authentication
"""

from typing import TypeVar
from api.v1.auth.session_exp_auth import SessionExpAuth
from os import getenv


class SessionDBAuth(SessionExpAuth):
    """
    The Session Database Authentication class
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
        pass

    def user_id_for_session_id(self, session_id=None):
        """
        overload the user_id_for_session_id method
        """
        pass

    def destroy_session(self, request=None):
        """
        overload the destroy_session method
        """
        pass
