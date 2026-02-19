
"""Module for handling password hashing and verification using Argon2."""

from argon2.exceptions import (HashingError, VerificationError, VerifyMismatchError)
from core.Exceptions import HashCorruptionError, PasswordMismatchError
from core.config import ARGON2_SETTING
from core.logger import get_logger

log = get_logger("SECURITY.HASH")


def hashCreate(password: str) -> str | bytes:
    """Hash a password using Argon2 algorithm."""
    ph = ARGON2_SETTING
    try:
        hash = ph.hash(password)
    except HashingError as he:
        log.warning("fails to create hash key")
        raise he

    return hash


def hashVerify(hash: str | bytes, password: str) -> bool:
    """Verify a password against its hash using Argon2 algortihm."""
    ph = ARGON2_SETTING
    try:
        value = ph.verify(hash, password)
    except VerifyMismatchError:
        log.critical("A brute-force attack was detected")
        raise PasswordMismatchError("Incorrect password or possible attack")
    except VerificationError:
        log.critical("The hash is invalid")
        raise HashCorruptionError("The hash is invalid")

    return value

