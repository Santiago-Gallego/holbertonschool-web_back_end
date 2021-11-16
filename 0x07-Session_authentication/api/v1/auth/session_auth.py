#!/usr/bin/env python3
""" API authentication
"""

from api.v1.auth.auth import Auth
from flask import request
from typing import List, TypeVar
import uuid
from models.user import User


class SessionAuth(Auth):
    """ Session Auth class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create Session ID For User_id"""
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a User ID based on a Session ID"""
        if not session_id or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Returns a User instance based on a cookie value."""
        session_id = self.session_cookie(request)
        if session_id is None:
            return None

        idd = self.user_id_for_session_id(session_id)
        return User.get(idd)

    def destroy_session(self, request=None):
        """deletes the user session / logout"""
        if not request:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        u_id = self.user_id_for_session_id(session_id)
        if not u_id:
            return False

        del self.user_id_by_session_id[session_id]
        return True
