#!/usr/bin/env python3
"""Protecting personal data"""
import logging
from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """return log message obfuscated"""
    tmp = message
    for field in fields:
        tmp = re.sub(field + "=.*?" + separator,
                     field + "=" + redaction + separator, tmp)
    return tmp


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
