#!/usr/bin/env python3
'''Regex-ing  module
'''
import os
import logging
import re
from typing import List


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    '''obsfuscates fields in message using redaction
    '''
    value = message
    for field in fields:
        sub = field + '=' + redaction
        # value = re.sub(r'{}[=\w\d/-@\.]*'.format(field), sub, value)
        value = re.sub(r'{}[=\w\d@\.-]*'.format(field), sub, value)
    return value


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''takes a logRecord and formats it to uman readable format
        '''
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def get_logger() -> logging.Logger:
    ''' returns a logging.Logger object.
    '''
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.setHandler(stream_handler)
    return logger


def get_db():
    '''returns a connector to the database
    '''
    db_user_name = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_passwd = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db.host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')
    # how to return a connector?
    # how to use _mysql_connector to connect to mysl
