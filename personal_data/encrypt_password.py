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


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check whether a password matches a previously hashed password.

    Args:
        hashed_password: the bcrypt-hashed password to check against.
        password: the plain-text password to validate.

    Returns:
        True if password, once hashed, matches hashed_password,
        False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
