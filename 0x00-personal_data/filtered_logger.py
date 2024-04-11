#!/usr/bin/env python3
"""0. Regex-ing -> obfuscate log messages
"""
import re
import logging
from typing import List
import os
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def log_user_data(user_data):
    """Log user data"""
    filtered_keys = ['name', 'email', 'phone', 'ssn', 'password']
    log_format = '[HOLBERTON] user_date INFO {last_login}: {data}'

    data = '; '.join(f'{key}=***' if key in filtered_keys else f'{key}={value}'
                     for key, value in zip(['name', 'email', 'phone', 'ssn',
                                            'password', 'ip', 'last_login',
                                            'user_agent'], user_data))
    print(log_format.format(last_login=user_data[6], data=data))


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns connector to db"""

    return mysql.connector.connect(
        user=os.environ.get("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.environ.get("PERSONAL_DATA_DB_PASSWORD", ""),
        host=os.environ.get("PERSONAL_DATA_DB_HOST", "localhost"),
        database=os.environ.get("PERSONAL_DATA_DB_NAME"),
    )


def get_logger() -> logging.Logger:
    """Get logger"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Obfuscate log messages"""
    for field in fields:
        message = re.sub(f"{field}=.*?{separator}",
                         f"{field}={redaction}{separator}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialization"""
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """formats the log record"""
        Formatter = logging.Formatter(self.FORMAT)
        record = Formatter.format(record)
        return filter_datum(self.fields, self.REDACTION,
                            str(record), self.SEPARATOR)

    def redact(self, message: str) -> str:
        """Redact message"""
        for field in self.fields:
            message = re.sub(f"{field}=[^;]",
                             f"{field}={self.REDACTION}", message)
        return message


def main():
    """Main function"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT name, email, phone, ssn, password, ip, \
                    last_login, user_agent FROM users;")

    for row in cursor:
        log_user_data(row)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
