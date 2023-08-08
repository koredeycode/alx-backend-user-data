#!/usr/bin/env python3
"""
Class to manage the API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    The Authentication class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        public method
        """
        if (path is None or excluded_paths is None or excluded_paths == []):
            return True
        return all([path not in p for p in excluded_paths])

    def authorization_header(self, request=None) -> str:
        """
        public method
        """
        if request is None:
            return None
        print(request.headers)
        if 'Authorization' not in request.headers:
            return None
        print(request.headers.get('Authorization'))
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        public method
        """
        return None
