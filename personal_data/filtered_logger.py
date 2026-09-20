#!/usr/bin/env python3
"""Filtered logger module.

This module provides a function for obfuscating personally
identifiable information (PII) fields within log messages.
"""
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
