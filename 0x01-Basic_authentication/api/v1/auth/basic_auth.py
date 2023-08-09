#!/usr/bin/env python3
"""This module contains the basic_auth class"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """BasicAucth class that holds all methods for basic authentication"""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Returns the base64 part of the authorizationheader for
            basic authentication
        """
        if not authorization_header:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        else:
            return authorization_header.split('Basic ')[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Return decoded value of base64 authorization_header"""
        if not base64_authorization_header:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = b64decode(base64_authorization_header).decode('utf-8')
            return decoded
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Return user email and password from the b64 decoded value"""
        if not decoded_base64_authorization_header:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:

            return None, None
        else:
            email, password = decoded_base64_authorization_header.split(':')
            return email, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Return User instance based on user email and password"""
        if not user_email and not isinstance(user_email, str):
            return None
        if not user_pwd and not isinstance(user_pwd, str):
            return None
        users = User.search({'email': user_email})
        if not users:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        else:
            return None
