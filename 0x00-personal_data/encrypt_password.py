#!/usr/bin/env python3
"""
the encrypt pasword implementation
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    turn the password string argument to a salted, hashed password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    validate that the provided password matches the hashed password
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
