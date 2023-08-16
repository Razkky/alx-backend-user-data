#!/usr/bin/env python3
"""Hash a password and return the byte string"""
from bcrypt import hashpw, gensalt, checkpw


def _hash_password(password: str) -> bytes:
    """Hash a password and return a salted hashed_password as bytes"""
    return hashpw(password.encode('utf-8'), gensalt())
