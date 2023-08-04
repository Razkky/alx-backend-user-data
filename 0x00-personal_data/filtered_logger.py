#!/usr/bin/env python3
"""Protecting personal data"""
import logging
from typing import List
import re
import os
import mysql.connector


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """return log message obfuscated"""
    tmp = message
    for field in fields:
        tmp = re.sub(field + "=.*?" + separator,
                     field + "=" + redaction + separator, tmp)
    return tmp


def get_logger() -> logging.Logger:
    """Returns a logging.Logger object"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    formatter = RedactingFormatter(pii_fields=PII_FIELDS)
    stream_handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Connects to mysql database"""
    user = os.environ.get('PERSONAL_DATA_DB_USERNAME', None)
    password = os.environ.get('PERSONAL_DATA_DB_PASSWORD', None)
    db_host = os.environ.get('PERSONAL_DATA_DB_HOST', None)
    db_name = os.environ.get('PERSONAL_DATA_DB_NAME', None)

    return mysql.connector.connect(user=user,
                                   password=password,
                                   host=db_host,
                                   database=db_name)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format log output"""
        return filter_datum(self.fields,
                            self.REDACTION, super(
                                RedactingFormatter, self).format(record),
                            self.SEPARATOR)
