#!/usr/bin/env python3
"""
the filter_logger module containing the filter_datum function
"""
import re
from typing import List


def filter_datum(fields: List, redaction: str,
                 message: str, separator: str) -> str:
    """return the log message obfuscated with the readacted string"""
    pattern = r'({}=)[^{}]+'.format('=|'.join(fields), separator)
    return re.sub(pattern, r'\1{}'.format(redaction), message)
