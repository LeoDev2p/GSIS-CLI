"""Module for handling authentication and session management."""

from utils.validation import valitacion_email
from core.logger import get_logger
from core.config import SUPERUSER, MASTER_KEY
from core.Exceptions import AuthError
from security.hashing import hashVerify


# Iniciamos la session
@valitacion_email
def login(*args):
    """Login function that validates the user credentials against the master key.
    
    Args:
        *args: A variable number of arguments containing the user credentials (username and passoword).

    Returns:
        bool: True if the credentials are valid, False otherwise.
    
    Raises:
        AuthError: If the username is incorrect (code 2040) or if the password is incorrect (code 2050).
        code 2040: Incorrect user
        code 2050: Incorrect password
    """
    log = get_logger("AUTH")
    # credential = (user, password)
    if args[0] == SUPERUSER:
        if hashVerify(MASTER_KEY, args[1]):
            log.info("Successful session start")
            return True, args[1]

        log.warning("Incorrect password")
        raise AuthError(2050)
    else:
        log.warning("Incorrect user")
        raise AuthError(2040)
