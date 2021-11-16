#!/usr/bin/env python3
"""
Hash password
"""
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> str:
    """ Returned bytes is a salted hash of the input password."""
    return hashpw(password.encode('utf-8'), gensalt())


def _generate_uuid() -> str:
    """  function should return a string representation of a new UUID
    Use the uuid module."""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """ __init__"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """hash the password with _hash_password, save the use to
        the database using self._db and return the User object."""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)

            return user

        raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """It should expect email and password required
        arguments and return a boolean."""
        try:
            user = self._db.find_user_by(email=email)
            return checkpw(password.encode('utf-8'), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """ It takes an email string argument and
        returns the session ID as a string."""
        try:
            user_data = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user_data.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> str:
        """Takes a single session_id string argument and
        returns the corresponding User or None"""
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Method updates the corresponding user’s session ID to None."""
        if not user_id:
            return None
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
            return None
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """ Generate a UUID and update the user."""
        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, reset_token=_generate_uuid())
            return user.reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """ Update password """
        if not reset_token:
            return None
            
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            pwd = _hash_password(password)
            self._db.update_user(user.id, hashed_password=pwd,
                                 reset_token=None)
        except NoResultFound:
            raise ValueError
