"""Module to encrypt and decrypt sensitive data using Fernet from the cryptography library."""

import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet, InvalidToken
from cryptography.exceptions import InvalidKey
from core.logger import get_logger
from core.config import SALT

log = get_logger("SECURITY.ENCRYPT")


class CipherManager:
    """It provides tools for encrypting and decrypting data.

    This class groups utility methods that allow you to secure sensitive information using encryption algorithms, 
    without needing to instantiate the class.
    """
    @staticmethod
    def _generate_key(master_password: str) -> bytes:
        """Deriva una llave de Fernet a partir de la clave maestra y el SALT."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=SALT.encode(),
            iterations=480000,
        )
        return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    
    @staticmethod
    def Encypt_data(data: str | int, master_password: str) -> bytes:
        """Encrypt a simple text string bytes using Fernet symmetric encryption.
        
        Args:
            data: The text string or integer to be encrypted.
            master_password: The master password used to generate the encryption key.
        
        Returns:
            The encrypted data as bytes.
        
        Raises:
            TypeError: If the input data is not a string or integer.
            InvalidToken: If the encryption process fails due to an invalid token.
        """
        try:
            # La llave NO vive en el .env, se crea aquí y muere al terminar la función
            key = CipherManager._generate_key(master_password)
            f = Fernet(key)
            
            if isinstance(data, int):
                data = str(data)

            return f.encrypt(data.encode("utf-8"))

        except Exception as e:
            log.error(f"Encryption failed: {e}")
            raise e

    @staticmethod
    def Decrypt_data(data: str, master_password: str) -> str:
        """Decrypt a token to recover the original text.
        
        Args:
            data: The encrypted data as a string bytes.
            master_password: The master password used to generate the decryption key.
        
        Returns:
            The decrypted data as a string or integer.
        
        Raises:
            InvalidToken: if the decryption process fails due to an invalid.
            InvalidKey: if the decryption process fails due to an invalid key.
        """
        try:
            key = CipherManager._generate_key(master_password)
            f = Fernet(key)
            
            decrypted = f.decrypt(data).decode("utf-8")
            return int(decrypted) if decrypted.isdigit() else decrypted
        except (InvalidToken, InvalidKey) as e:
            log.error(f"Decryption failed: {e}")
            raise e
