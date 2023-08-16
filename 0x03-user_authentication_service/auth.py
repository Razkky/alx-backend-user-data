#!/usr/bin/env python3
"""Hash a password and return the byte string"""
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hash a password and return a salted hashed_password as bytes"""
    return hashpw(password.encode('utf-8'), gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize Auth class"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a user to the database"""
        if self._db._session.query(User).filter_by(email=email).first():
            raise ValueError(f"User {email} already exists")
        else:
            hashed_psw = _hash_password(password)
            user = User(email=email, hashed_password=hashed_psw)
            self._db._session.add(user)
            self._db._session.commit()
            return user
