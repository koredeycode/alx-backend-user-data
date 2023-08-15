#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User

from typing import TypeVar


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
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

    def add_user(self, email: str, hashed_password: str) -> TypeVar("User"):
        """
        add user to the database
        """
        try:
            newuser = User(email=email, hashed_password=hashed_password)
            self._session.add(newuser)
            self._session.commit()
        except Exception:
            self._session.rollback()
            newuser = None
        return newuser

    def find_user_by(self, **kwargs) -> TypeVar("User"):
        """
        find a user from the database
        """
        query = self._session.query(User)
        for k, v in kwargs.items():
            if hasattr(User, k):
                col = getattr(User, k)
                query = query.filter(col == v)
            else:
                raise InvalidRequestError()
        user = query.first()
        if user is None:
            raise NoResultFound()
        return user

    def update_user(self, user_id, **kwargs) -> None:
        """
        update a user in the db
        """
        user = self.find_user_by(id=user_id)
        if user is None:
            return
        for k, v in kwargs.items():
            if hasattr(user, k):
                setattr(user, k, v)
            else:
                raise ValueError()
        self._session.commit()
