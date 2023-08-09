#!/usr/bin/env python3
"""
Class to manage the Basic authentication
"""

from typing import TypeVar
from api.v1.auth.session_auth import SessionAuth
from models.user import User
import uuid


class SessionExpAuth(SessionAuth):
    """
    The Session Expiration Authentication class
    """
    pass
