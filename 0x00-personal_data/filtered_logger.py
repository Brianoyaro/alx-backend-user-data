#!/usr/bin/env python3
'''Regex-ing  module
'''
import logging
import re
from typing import List


PII_FIELDS = (1,2,3,4,44)
def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    value = message
    for field in fields:
        sub = field + '=' + redaction
        value = re.sub(r'{}[=\w\d/-]*'.format(field), sub, value)
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
        return filter_datum(self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR)

def get_logger() -> logging.Logger:
    ''' returns a logging.Logger object.
    '''
    user_data = logging.getLogger(__name__)
    user_data.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter([]))
    user_data.setHandler(stream_handler)
