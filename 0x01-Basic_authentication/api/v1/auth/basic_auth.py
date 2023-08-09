#!/usr/bin/env python3
"""This module contains the basic_auth class"""
from api.v1.auth.auth import Auth
from base64 import b64decode


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
