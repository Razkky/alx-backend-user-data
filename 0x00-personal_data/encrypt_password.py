#!/usr/bin/env python3
"""Encryping password with bcrypt"""


import bcrypt


def hash_password(password: str) -> str:
    """return a hashed password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
