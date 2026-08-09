"""Module to encrypt and decrypt sensitive data using Fernet from the cryptography library."""

import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet, InvalidToken
from cryptography.exceptions import InvalidKey
from src.core.logger import get_logger
from src.core import config

log = get_logger("SECURITY.ENCRYPT")

_FALLBACK_SALT = b"gsis-cli-fallback-salt-2026"


class CipherManager:
    """It provides tools for encrypting and decrypting data.

    This class groups utility methods that allow you to secure sensitive information using encryption algorithms, 
    without needing to instantiate the class.
    """

    @staticmethod
    def _generate_key(master_password: str, salt: bytes | str | None = None) -> bytes:
        """Deriva una llave de Fernet a partir de la clave maestra y el SALT."""
        if salt is None:
            salt = config.SALT.encode() if config.SALT else _FALLBACK_SALT
        if isinstance(salt, str):
            salt = salt.encode("utf-8")
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))

    @staticmethod
    def Encypt_data(data: str | int, master_password: str, salt: bytes | str | None = None) -> bytes:
        """Encrypt a simple text string bytes using Fernet symmetric encryption.

        Args:
            data: The text string or integer to be encrypted.
            master_password: The master password used to generate the encryption key.
            salt: Optional explicit salt for the key derivation. Defaults to the config SALT.

        Returns:
            The encrypted data as bytes.

        Raises:
            TypeError: If the input data is not a string or integer.
        """
        try:
            key = CipherManager._generate_key(master_password, salt)
            f = Fernet(key)

            if isinstance(data, int):
                data = str(data)

            return f.encrypt(data.encode("utf-8"))

        except Exception as e:
            log.error(f"Encryption failed: {e}")
            raise e

    @staticmethod
    def Decrypt_data(data: str, master_password: str, salt: bytes | str | None = None) -> str:
        """Decrypt a token to recover the original text.

        Args:
            data: The encrypted data as a string bytes.
            master_password: The master password used to generate the decryption key.
            salt: Optional salt for the key derivation. Defaults to the config SALT.

        Returns:
            The decrypted data as a string or integer.

        Raises:
            InvalidToken/InvalidKey: If the decryption process fails.
        """
        try:
            key = CipherManager._generate_key(master_password, salt)
            f = Fernet(key)

            decrypted = f.decrypt(data).decode("utf-8")
            return int(decrypted) if decrypted.isdigit() else decrypted
        except (InvalidToken, InvalidKey) as e:
            log.error(f"Decryption failed: {e}")
            raise e

    @staticmethod
    def Decrypt_data_tolerant(data: str, master_password: str) -> str | None:
        """Intenta descifrar probando el SALT actual, el fallback y el legacy.

        Útil para datos que fueron cifrados cuando no había USB (fallback) o
        con un SALT previo. Devuelve el texto descifrado o None si ninguno
        coincide.
        """
        candidatos = []
        if getattr(config, "SALT", None):
            candidatos.append(config.SALT.encode("utf-8"))
        candidatos.append(_FALLBACK_SALT)

        for salt in candidatos:
            try:
                key = CipherManager._generate_key(master_password, salt)
                decrypted = Fernet(key).decrypt(data).decode("utf-8")
                return str(decrypted)
            except (InvalidToken, InvalidKey, ValueError):
                continue

        log.error("Decryption failed for all candidate salts.")
        return None
