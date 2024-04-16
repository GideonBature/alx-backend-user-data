#!/usr/bin/env python3
""" Basic Auth Class
"""
from api.v1.auth.auth import Auth
import base64


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

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """ decode_base64_authorization_header
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) != str:
            return None
        try:
            d_bytes = base64.b64decode(base64_authorization_header)
            decoded_string = d_bytes.decode('utf-8')
            return decoded_string
        except Exception:
            return None
