#!/usr/bin/env python3
"""
the filter_logger module containing the filter_datum function
"""
import re
from typing import List
import logging

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """format a log recordd with filter_daturm"""
        msg = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)


#def filter_datum(fields: List[str], redaction: str,
 #                message: str, separator: str) -> str:
  #  """return the log message obfuscated with the readacted string"""
   # pattern = r'({}=)[^{}]+'.format('=|'.join(fields), separator)
    #return re.sub(pattern, r'\1{}'.format(redaction), message)
def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """return the log message obfuscated with the readacted string"""
    extract_pattern = r'(?P<field>{})=[^{}]*'.format('|'.join(fields), re.escape(separator))
    replace_pattern = r'\g<field>={}'.format(redaction)
    return re.sub(extract_pattern, replace_pattern, message)
