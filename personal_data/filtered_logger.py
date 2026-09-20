#!/usr/bin/env python3
"""Filtered logger module.

This module provides a function and a logging Formatter for
obfuscating personally identifiable information (PII) fields
within log messages.
"""
import logging
import re
from typing import List


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
