#!/usr/bin/env python3
"""Conatins the SessionAuth class
    that implements its authentication mechanism
"""
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


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

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return user id base on the session_id"""

        if not session_id or not isinstance(session_id, str):
            return None
        else:
            return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Return a user instance based on cookie value"""

        session_id = self.session_cookie(request)
        return User.get(SessionAuth.user_id_by_session_id.get(session_id))
