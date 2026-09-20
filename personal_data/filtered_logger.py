#!/usr/bin/env python3
"""Filtered logger module.

This module provides a function and a logging Formatter for
obfuscating personally identifiable information (PII) fields
within log messages.
"""
import logging
import os
import re
from typing import List

import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Obfuscate the values of specified fields within a log message.

    Args:
        fields: the list of field names whose values to obfuscate.
        redaction: the string to replace each field's value with.
        message: the log line containing the fields.
        separator: the character separating fields in the message.

    Returns:
        The log message with each listed field's value replaced by
        redaction.
    """
    pattern = r'(' + '|'.join(fields) + r')=[^' + separator + r']*'
    return re.sub(pattern, lambda m: m.group(1) + '=' + redaction, message)


class RedactingFormatter(logging.Formatter):
    """Logging Formatter that redacts specified PII fields."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize the formatter with the fields to redact.

        Args:
            fields: the list of field names whose values should be
                redacted in every formatted log record.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record, redacting the configured PII fields.

        Args:
            record: the log record to format.

        Returns:
            The formatted log message with values of self.fields
            replaced by REDACTION.
        """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Create and configure a logger for handling user data.

    Returns:
        A logging.Logger named "user_data" that logs up to INFO
        level, does not propagate to other loggers, and uses a
        StreamHandler with RedactingFormatter (parameterized with
        PII_FIELDS) to obfuscate sensitive fields in log messages.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Connect to the secure holberton database using env credentials.

    Reads PERSONAL_DATA_DB_USERNAME (default "root"),
    PERSONAL_DATA_DB_PASSWORD (default ""), PERSONAL_DATA_DB_HOST
    (default "localhost"), and PERSONAL_DATA_DB_NAME from the
    environment to avoid hardcoding credentials in the codebase.

    Returns:
        A MySQLConnection object connected to the configured
        database.
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name,
    )
