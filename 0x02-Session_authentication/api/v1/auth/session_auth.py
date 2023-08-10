#!/usr/bin/env python3
"""Conatins the SessionAuth class
    that implements its authentication mechanism
"""
from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """Implements the session authentication mechanism"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session id for a user"""
        if not user_id or not isinstance(user_id, str):
            return None
        else:
            id = str(uuid4())
            SessionAuth.user_id_by_session_id[id] = user_id
            return id
