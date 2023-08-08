#!/usr/bin/env python3
"""
Class to manage the Basic authentication
"""
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth
import base64
from models.user import User


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
        creds = header.split(":")
        email, pwd = creds[0], ":".join(creds[1:])
        return email, pwd

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        return the User instance based on his email and password
        """
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        if len(users) <= 0:
            return None
        user = users[0]
        if user is None or not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """
        retrieves the user instance for a request
        """
        header = self.authorization_header(request)
        extract = self.extract_base64_authorization_header(header)
        decoded_extract = self.decode_base64_authorization_header(extract)
        email, pwd = self.extract_user_credentials(decoded_extract)
        user = self.user_object_from_credentials(email, pwd)
        return user
