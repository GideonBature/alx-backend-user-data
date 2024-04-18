#!/usr/bin/env python3
""" Session DB Auth
"""
from datetime import datetime, timedelta
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ Session DB Auth
    """
    def create_session(self, user_id: str = None) -> str:
        """ create_session
        """
        session_id = super().create_session(user_id)
        if session_id:
            n_session = UserSession(user_id=user_id, session_id=session_id)
            n_session.save()
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ user_id_for_session_id
        """
        user_sessions = UserSession.search({'session_id': session_id})
        if user_sessions:
            user_session = user_sessions[0]
            if self.session_duration > 0:
                time_elapsed = datetime.now() - user_session.created_at
                if time_elapsed > timedelta(seconds=self.session_duration):
                    return None
            return user_session.user_id
        return None

    def destroy_session(self, request=None) -> bool:
        """ destroy_session, deletes the user session/logout
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        UserSession.destroy({'session_id': session_id})
        return True
