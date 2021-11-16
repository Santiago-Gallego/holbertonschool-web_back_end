#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from user import Base
from user import User

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


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
    def _session(self):
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Method, which has two required string arguments:
        email and hashed_password, and returns a User object."""
        user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """ Method takes in arbitrary keyword arguments and returns
        the first row found in the users table as filtered by
        the method’s input arguments."""
        data = User.__table__.columns.keys()
        if not all(key in data for key in kwargs) or not kwargs:
            raise InvalidRequestError

        session = self._session
        user = session.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Method that takes as argument a required user_id integer
        and arbitrary keyword arguments."""
        session = self._session
        user = self.find_user_by(id=user_id)
        data = User.__table__.columns.keys()
        if not all(key in data for key in kwargs) or not kwargs:
            raise ValueError

        for k, v in kwargs.items():
            setattr(user, k, v)
        session.commit()
