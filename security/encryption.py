from cryptography.exceptions import InvalidKey
from cryptography.fernet import Fernet, InvalidToken
from core.config import SECRET_KEY_FERNET
from core.logger import get_logger

log = get_logger("SECURITY.ENCRYPT")


class CipherManager:

    @staticmethod
    def Encypt_data(data):
        try:
            f = Fernet(SECRET_KEY_FERNET)
            if isinstance(data, int):
                data = f"{data}"

            encode_data = data.encode("utf-8")
            token = f.encrypt(encode_data)
        except (TypeError, InvalidToken) as Error:
            log.error("The data is not in bytes")
            raise Error

        return token

    @staticmethod
    def Decrypt_data(data):
        try:
            f = Fernet(SECRET_KEY_FERNET)
            decrypt_data = f.decrypt(data)
        except (InvalidToken, InvalidKey) as Error:
            raise Error

        decode_data = decrypt_data.decode("utf-8")
        return decode_data if not decode_data.isdigit() else int(decode_data)
