#!/usr/bin/env python3
"""5. Encrypting passwords
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hash a password
    """
    return bcrypt.hashpw(password.encode('utf-8'),
                         bcrypt.gensalt())
