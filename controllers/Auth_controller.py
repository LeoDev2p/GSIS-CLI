from utils.validation import valitacion_email
from core.logger import get_logger
from core.config import SUPERUSER, MASTER_KEY
from core.Exceptions import AuthError
from security.hashing import hashVerify


# Iniciamos la session
@valitacion_email
def login (*args):
    log = get_logger ("AUTH")
    # credential = (user, password)
    if args[0] == SUPERUSER:
        if hashVerify (MASTER_KEY, args[1]):
            log.info ("Successful session start")
            return True

        log.warning (f"Incorrect password")
        raise AuthError (2050)
    else:
        log.warning (f"Incorrect user")
        raise AuthError (2040)