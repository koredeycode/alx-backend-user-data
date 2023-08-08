#!/usr/bin/env python3
"""
Class to manage the Basic authentication
"""
from flask import request
from typing import List, TypeVar
from .auth import Auth
import base64


class BasicAuth(Auth):
    """
    The Basic Authentication class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        return ths base64 part of the Authorization header
        """
        header = authorization_header
        if header is None or type(header) is not str:
            return None
        start = header[:6]
        basic = header[6:]
        if start != "Basic ":
            return None
        return basic

    def decode_base64_authorization_header(self, base64_header: str) -> str:
        """
        return the decoded value of a Base64 string
        """
        header = base64_header
        if header is None or type(header) is not str:
            return None
        try:
            return base64.b64decode(header).decode()
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_header: str) -> (str, str):
        """
        returns the user email and password from the decoded value
        """
        header = decoded_base64_header
        if header is None or type(header) is not str or ":" not in header:
            return None, None
        return tuple(header.split(":"))

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        return the User instance based on his email and password
        """
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None