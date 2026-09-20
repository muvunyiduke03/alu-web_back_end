#!/usr/bin/env python3
"""Encrypt password module.

This module provides a function for securely hashing passwords so
that plain-text passwords are never stored in a database.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hash a password with a randomly generated salt.

    Args:
        password: the plain-text password to hash.

    Returns:
        A salted, hashed version of password as a byte string,
        suitable for storing in place of the plain-text password.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
