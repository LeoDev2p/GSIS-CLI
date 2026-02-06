from argon2.exceptions import HashingError, VerificationError, VerifyMismatchError
from core.Exceptions import HashCorruptionError, PasswordMismatchError
from core.config import ARGON2_SETTING
from core.logger import get_logger

log = get_logger("SECURITY.HASH")


# creamos el hash de contraseña
def hashCreate(data):

    ph = ARGON2_SETTING
    try:
        hash = ph.hash(data)
    except HashingError as he:
        log.warning("fails to create hash key")
        return f"Error {he}"

    return hash


def hashVerify(hash, data):
    ph = ARGON2_SETTING
    try:
        value = ph.verify(hash, data)
    except VerifyMismatchError as vfError:
        log.critical("A brute-force attack was detected")
        raise PasswordMismatchError("Incorrect password or possible attack")
    except VerificationError as VError:
        log.critical("The hash is invalid")
        raise HashCorruptionError("The hash is invalid")

    return value
