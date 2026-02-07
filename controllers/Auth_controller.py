"""Module for handling authentication and session management."""

from utils.validation import valitacion_email
from core.logger import get_logger
from core.config import SUPERUSER, MASTER_KEY
from core.Exceptions import AuthError, SecurityError, PasswordMismatchError, HashCorruptionError
from security.hashing import hashVerify
from security.integrity import register_failed_attempt, trigger_self_destruct, get_attempts_data, reset_attempts

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
    data = get_attempts_data()
    atp = data.get("attempts", 0)
    mx = data.get("max_attempts", 3)

    if atp >= mx:
        log.critical("Maximum login attempts reached. Deleting database for security reasons.")
        trigger_self_destruct ()
        raise SecurityError("System locked. Data deleted.")
    
    # credential = (user, password)
    if args[0] == SUPERUSER:
        try:
            if hashVerify(MASTER_KEY, args[1]):
                log.info("Successful session start")
                reset_attempts()
                return args[1]
        except (PasswordMismatchError, HashCorruptionError):
            log.warning("Incorrect password")

            data = register_failed_attempt() 
            nuevo_atp = data["attempts"]
            
            if nuevo_atp >= mx:
                log.critical("Maximum failed attempts reached. Deleting database.")
                trigger_self_destruct()
                raise SecurityError("System locked. Data deleted.")

            raise AuthError(2050, nuevo_atp)
    else:
        log.warning("Incorrect user")
        data = register_failed_attempt() 
        nuevo_atp = data["attempts"]

        if nuevo_atp >= mx:
            log.critical("Maximum failed attempts reached. Deleting database.")
            trigger_self_destruct()
            raise SecurityError("System locked. Data deleted.")

        raise AuthError(2060, nuevo_atp)
