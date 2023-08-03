#!/usr/bin/env python3
"""Encryping password with bcrypt"""


import bcrypt


def hash_password(password: str) -> bytes:
    """return a hashed password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if a user password is correct"""
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        return True
    else:
        return False
