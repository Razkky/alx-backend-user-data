#!/usr/bin/env python3
"""This module contains the basic_auth class"""
from api.v1.auth.auth import Auth


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
