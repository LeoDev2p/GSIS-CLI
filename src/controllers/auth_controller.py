"""Module for handling authentication and session management."""

from src.utils.validation import valitacion_email
from src.core.logger import get_logger
from src.core import config
from src.core.Exceptions import AuthError, SecurityError, PasswordMismatchError, HashCorruptionError
from src.security.hashing import hashVerify, hashCreate
from src.security.integrity import register_failed_attempt, trigger_self_destruct, get_attempts_data, reset_attempts
from pathlib import Path

class Authentication:
    def __init__ (self):
        self.log = get_logger("AUTH")
        self.data = get_attempts_data()
        self.atp = self.data.get("attempts", 0)
        self.atp_mx = self.data.get("max_attempts", 3)

    @valitacion_email
    def login(self, *args):
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
        if self.atp >= self.atp_mx:
            self.log.critical("Maximum login attempts reached. Deleting database for security reasons.")
            trigger_self_destruct ()
            raise SecurityError("System locked. Database deleted.")

        if not config.refresh_credentials():
            self.log.warning("No hay credenciales en el USB")
            raise AuthError(2080, "No credentials found in the USB. Plug the USB with key/key.key.")

        # credential = (user, password)
        if args[0] == config.SUPERUSER:
            try:
                if hashVerify(config.MASTER_KEY, args[1]):
                    self.log.info("Successful session start")
                    reset_attempts()
                    return args[1]
            except (PasswordMismatchError, HashCorruptionError):
                self.log.warning("Incorrect password")

                data = register_failed_attempt() 
                nuevo_atp = data["attempts"]
                
                if nuevo_atp >= self.atp_mx:
                    self.log.critical("Maximum failed attempts reached. Deleting database.")
                    trigger_self_destruct()
                    raise SecurityError("System locked. Data deleted.")

                raise AuthError(2050, nuevo_atp)
        else:
            self.log.warning("Incorrect user")
            data = register_failed_attempt() 
            nuevo_atp = data["attempts"]

            if nuevo_atp >= self.atp_mx:
                self.log.critical("Maximum failed attempts reached. Deleting database.")
                trigger_self_destruct()
                raise SecurityError("System locked. Data deleted.")

            raise AuthError(2060, nuevo_atp)

    @valitacion_email
    def register(self, **kawargs):
        import secrets
        import base64

        unidad = Path(kawargs['unidad']).resolve()
        ruta_carpeta = unidad / 'key'
        ruta_carpeta.mkdir(exist_ok=True)

        password = kawargs.get('password')
        confirm_password = kawargs.get('confirm_password')

        if password != confirm_password:
            raise AuthError(2070, "Las contrasenas no coinciden.")

        # Escribimos las claves maestras en el USB: key/key.key
        hash_psw = hashCreate(password)
        salt = base64.b64encode(secrets.token_bytes(16)).decode('utf-8')

        with open(ruta_carpeta / "key.key", "w", encoding="utf-8") as file:
            file.write(f"MASTER_KEY='{hash_psw}'\n")
            file.write(f"SALT='{salt}'\n")
