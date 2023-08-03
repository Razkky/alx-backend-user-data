#!/usr/bin/env python3
"""Protecting personal data"""
import logging
from typing import List
import re


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'ip')


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
    formatter = RedactingFormatter(pii_fields=PII_FIELDS)
    stream_handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(stream_handler)

    return logger


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
