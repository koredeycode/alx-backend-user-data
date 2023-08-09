#!/usr/bin/env python3
"""
Class to manage the API authentication
"""
from flask import request
from typing import List, TypeVar
import re
from os import getenv


class Auth:
    """
    The Authentication class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        public method
        """
        if path is not None and excluded_paths is not None:
            for exclusion_path in map(lambda x: x.strip(), excluded_paths):
                pattern = ''
                if exclusion_path[-1] == '*':
                    pattern = '{}.*'.format(exclusion_path[0:-1])
                elif exclusion_path[-1] == '/':
                    pattern = '{}/*'.format(exclusion_path[0:-1])
                else:
                    pattern = '{}/*'.format(exclusion_path)
                if re.match(pattern, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        public method
        """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        public method
        """
        return None

    def session_cookie(self, request=None):
        """
        return a cookie from a request
        """
        if request is None:
            return None
        return request.cookies.get(getenv('SESSION_NAME'))
