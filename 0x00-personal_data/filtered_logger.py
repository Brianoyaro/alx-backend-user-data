#!/usr/bin/env python3
'''Regex-ing  module
'''
import mysql.connector
from mysql.connector.connection import MySQLConnection
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
        '''return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)'''
        formatter = logging.Formatter(self.FORMAT)
        value = formatter.format(record)
        return filter_datum(self.fields, self.REDACTION,
                            value, self.SEPARATOR)


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


def get_db() -> MySQLConnection:
    '''returns a connector to the database
    '''
    db_user_name = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_passwd = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')
    # how to return a connector?
    # how to use _mysql_connector to connect to mysl
    mydb = mysql.connector.connect(
            host=db_host,
            user=db_user_name,
            password=db_passwd,
            database=db_name)
    return mydb


def main():
    '''main function
    '''
    formatter = RedactingFormatter(fields=["phone",
                                           "name",
                                           "email",
                                           "ssn",
                                           "password"])
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    for row in cursor:
        logger.info(row)
    cursor.close()
    db.close()


main()
