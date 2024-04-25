#!/usr/bin/env python3
""" Module that handles all authentication
"""
from db import DB
import bcrypt
from uuid import uuid4
from user import User
from typing import ByteString
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound


def _generate_uuid() -> str:
    """Generate uuid
    """
    UUID = str(uuid4())
    return UUID


def _hash_password(password: str) -> str:
    """Hash a password for storing.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """initisation"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError('User {} already exists'.format(email))
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """checks password for valid login"""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Creates new session"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> str:
        """gets user from session id"""
        if not session_id:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """destroys the current session"""
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """generates a password reset token using uuid"""
        try:
            user = self._db.find_user_by(email=email)
            password_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=password_token)
            return password_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """checks the reset token with the database then
        sets the new password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            NPwd = _hash_password(password)
            self._db.update_user(user.id, hashed_password=NPwd,
                                 reset_token=None)
        except NoResultFound:
            raise ValueError
