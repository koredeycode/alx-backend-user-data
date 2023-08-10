#!/usr/bin/env python3
"""
Class to manage the SessionDB authentication
"""

from typing import TypeVar
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
    The Session Database Authentication class
    """

    def create_session(self, user_id=None):
        """
        overload the create_session method
        """
        session_id = super().create_session(user_id)
        session = UserSession(session_id=session_id, user_id=user_id)
        session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        overload the user_id_for_session_id method
        """
        try:
            sessions = UserSession.search({"session_id": session_id})
        except Exception:
            return None
        if sessions is None or len(sessions) <= 0:
            return None
        session = sessions[0]
        if self.session_duration <= 0:
            return session.user_id
        created_at = session.created_at
        difference = timedelta(seconds=self.session_duration)
        if created_at + difference < datetime.now():
            return None
        return session.user_id

    def destroy_session(self, request=None):
        """
        overload the destroy_session method
        """
        cookie = self.session_cookie(request)
        if cookie is None:
            return False
        try:
            sessions = UserSession.search({'session_id': cookie})
        except Exception:
            return False
        if len(sessions) <= 0:
            return False
        session = sessions[0]
        session.remove()
        return True
