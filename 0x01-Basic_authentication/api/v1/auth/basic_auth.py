#!/usr/bin/env python3
""" Basic Auth Class
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ Basic Auth Class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str
                                            ) -> str:
        """ extract_base64_authorization_header
        """
        if authorization_header is None:
            return None
        if type(authorization_header) != str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]
