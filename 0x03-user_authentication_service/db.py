#!/usr/bin/env python3
"""DB module
"""
from flask import Flask, jsonify, request, abort, Response
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """adds a user to the database
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Implement the find_user_by method, which has one required
        argument: kwargs, a dictionary.
        The method should return the first
        row found in the users table as filtered by the methods
        input arguments.
        """
        if not kwargs:
            raise InvalidRequestError
        if not all(key in User.__table__.columns.keys() for key in kwargs):
            raise InvalidRequestError
        row = self._session.query(User).filter_by(**kwargs).first()
        if not row:
            raise NoResultFound
        return row

    def update_user(self, user_id: int, **kwargs) -> None:
        """Implement the update_user method, which has two required arguments:
        user_id and kwargs, a dictionary.
        The method should update the corresponding user with the
        attributes.
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if key not in User.__table__.columns.keys():
                raise ValueError
            setattr(user, key, value)
        self._session.commit()
