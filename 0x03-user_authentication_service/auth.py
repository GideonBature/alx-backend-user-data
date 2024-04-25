#!/usr/bin/env python3
"""Auth module
"""
import bcrypt


def __hash_password(password: str) -> bytes:
    """Hash a password
    """
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pw
