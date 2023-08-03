#!/usr/bin/env python3
"""Encryping password with bcrypt"""


import bcrypt


def hash_password(password: str) -> bytes:
    """return a hashed password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hash_password: bytes, password: str) -> bool:
    """Checks if a user password is correct"""
    if bcrypt.checkpw(password.encode('utf-8'), hash_password):
        return True
    else:
        return False
