#!/usr/bin/env python3
"""This module contains the user authentication mechanism"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """Authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """This methods return False"""
        if not path or not excluded_paths:
            return True
        if path[-1] != '/':
            path += '/'
        if path not in excluded_paths:
            return True
        else:
            return False

    def authorization_header(self, request=None) -> str:
        """Returns None"""
        if not request or 'Authorization' not in request.headers:
            return None
        else:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """This methods return None"""
        return None

    def session_cookie(self, request=None):
        """Returns a cookie value from a request"""

        if not request:
            return None
        name = os.getenv('SESSION_NAME')
        return request.cookies.get(name)
