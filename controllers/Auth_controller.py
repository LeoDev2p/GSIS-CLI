from utils.validation import valitacion_email
from core.logger import get_logger
from core.config import SUPERUSER, MASTER_KEY
from core.Exceptions import AuthError


# Iniciamos la session
@valitacion_email
def login (*args):
    log = get_logger ("AUTH")
    # credential = (user, password)
    if args[0] == SUPERUSER:
        if args[1] == MASTER_KEY:
            log.info ("inicio de session exitoso")
            return True

        log.warning (f"Contraseña incorrecta")
        raise AuthError (2050)
    else:
        log.warning (f"Usuario incorrecto")
        raise AuthError (2040)