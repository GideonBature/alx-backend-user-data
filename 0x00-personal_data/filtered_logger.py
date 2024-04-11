#!/usr/bin/env python3
"""0. Regex-ing -> obfuscate log messages
"""
import re


def filter_datum(fields: list, redaction: str, message: str, separator: str) -> str:
    """Obfuscate log messages"""
    for field in fields:
        message = re.sub(f"{field}=.*?{separator}", f"{field}={redaction}{separator}", message)
    return message
