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
