#!/usr/bin/env python3
"""Auth module
"""
import bcrypt
from db import DB


def _hash_password(password: str) -> bytes:
    """Hash a password
    """
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pw


class Auth:
    """Auth class
    """
    def __init__(self):
        """Initialize a new Auth instance
        """
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """Hash a password
        """
        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_pw

    def register_user(self, email: str, password: str) -> User:
        """Register a new user
        """
        u_query = self._db._session.query(User).\
            filter_by(email=email).first()
        if user_query:
            raise ValueError(f"User {email} already exists")

        hashed_password = self._hash_password(password)
        new_user = self._db.add_user(email, hashed_password)
        return new_user
