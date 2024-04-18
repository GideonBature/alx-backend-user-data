#!/usr/bin/env python3
""" Session Exp Auth
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """ Session Exp Auth
    """
    def __init__(self):
        """ __init__
        """
        session_duration = os.getenv('SESSION_DURATION', 0)
        try:
            self.session_duration = int(session_duration)
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """ create_session
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_dictionary = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ user_id_for_session_id
        """
        if session_id is None or session_id not in \
                self.user_id_by_session_id:
            return None

        session_data = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_data['user_id']

        created_at = session_data.get('created_at')
        if created_at is None:
            return None

        if created_at + timedelta(seconds=self.session_duration) < \
                datetime.now():
            return None

        return session_data['user_id']
