#!/usr/bin/env python3
"""
Class to manage the SessionDB authentication
"""

from typing import TypeVar
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
import uuid
from datetime import datetime


class SessionDBAuth(SessionExpAuth):
    """
    The Session Database Authentication class
    """

    def create_session(self, user_id=None):
        """
        overload the create_session method
        """
        session_id = str(uuid.uuid4())
        session = UserSession(session_id=session_id, user_id=user_id)
        session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        overload the user_id_for_session_id method
        """
        sessions = UserSession.search({"session_id": session_id})
        if sessions is None or len(sessions) <= 0:
            return None
        session = sessions[0]
        created_at = session.created_at
        lapse = datetime.now() - created_at
        if lapse.seconds > self.session_duration:
            return None
        return session.user_id

    def destroy_session(self, request=None):
        """
        overload the destroy_session method
        """
        if request is None:
            return False
        cookie = self.session_cookie(request)
        if cookie is None:
            return False
        sessions = UserSession.search({'session_id': cookie})
        if len(sessions) <= 0:
            return False
        session = sessions[0]
        session.remove()
        return True
