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
