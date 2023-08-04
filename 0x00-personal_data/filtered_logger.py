#!/usr/bin/env python3
"""
the filter_logger module containing the filter_datum function
"""
import re
from typing import List
import logging
import mysql.connector
import os

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


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """return the log message obfuscated with the readacted string"""
    extract_pattern = r'(?P<field>{})=[^{}]*'.format('|'.join(fields),
                                                     re.escape(separator))
    replace_pattern = r'\g<field>={}'.format(redaction)
    return re.sub(extract_pattern, replace_pattern, message)


def get_logger() -> logging.Logger:
    """
    return a Logger object fro user data
    """
    logger = logging.getLogger("user_data")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    returns a connector to the database
    """
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db = os.getenv("PERSONAL_DATA_DB_NAME", "")
    user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    connection = mysql.connector.connect(host=host, user=user, port=3306,
                                         password=pwd, database=db)
    return connection


def main() -> None:
    """
    obtain a database connection and retriev all rows in users table and
    display each row in filter format
    """
    fields = ["name", "email", "phone", "ssn", "password", "ip",
              "last_login", "user_agent"]
    fields_str = ",".join(fields)
    query = "SELECT {} FROM users;".format(fields_str)
    logger = get_logger()
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            record = map(
                    lambda x: '{}={}'.format(x[0], x[1]),
                    zip(fields, row),
                    )
            msg = "{};".format("; ".join(list(record)))
            args = ("user_data", logging.INFO, None, None, msg, None, None)
            log_record = logging.LogRecord(*args)
            logger.handle(log_record)


if __name__ == "__main__":
    main()
