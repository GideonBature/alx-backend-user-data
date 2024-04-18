#!/usr/bin/env python3
""" Session DB Auth
"""
from datetime import datetime, timedelta
from models.user_session import UserSession
from api.v1.auth.session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """ Session DB Auth
    """
    def create_session(self, user_id=None):
        """Create a session and store it in the
        file-based database.
        """
        session_id = super().create_session(user_id)
        if session_id:
            new_user_session = UserSession(user_id=user_id,
                                           session_id=session_id)
            new_user_session.save()  # Assumes save method writes to file
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve user ID based on session ID
        from the file database.
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

    def destroy_session(self, request=None):
        """Destroy the session based on the
        session ID in the request cookie.
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id and self.user_id_for_session_id(session_id):
            UserSession.destroy({'session_id': session_id})
            return True
        return False
