"""Module responsible for managing login attempts and implementing security measures such as deleting the database after a certain number of failed attempts."""

import json
import os

from src.core import config as config_module
from src.security.encryption import CipherManager
from cryptography.fernet import InvalidToken

# Sal dedicada y estable para el archivo de integridad. NO depende del SALT
# del vault (que puede cambiar entre sesiones), para que el estado de intentos
# siempre pueda leerse/escribirse aun si el USB cambia.
_ATTEMPTS_SALT = b"gsis-attempts-salt-2026"


def _secure_folder():
    return getattr(config_module, "secure_folder", "")


def _integrity_path():
    return getattr(config_module, "INTEGRETY_PATH", "")


def _secret_key():
    return getattr(config_module, "SECRET_KEY_ATTEMPTS", "")


# Sales probadas al leer para compatibilidad con archivos generados antes de
# esta versión (la derivación usaba config.SALT o el fallback por defecto).
def _legacy_salts():
    salts = [_ATTEMPTS_SALT]
    if getattr(config_module, "SALT", None):
        salts.append(config_module.SALT)
    salts.append(None)
    return salts


def get_attempts_data() -> dict:
    """Read the file or create it with default values if it does not exist."""
    secure_folder = _secure_folder()
    integrity_path = _integrity_path()
    secret = _secret_key()

    if not os.path.exists(secure_folder):
        os.makedirs(secure_folder)

    if not os.path.isfile(integrity_path):
        initial_data = {"attempts": 0, "max_attempts": 3}
        save_attempts_data(initial_data)
        return initial_data

    for salt in _legacy_salts():
        try:
            with open(integrity_path, "r", encoding="utf-8") as f:
                txt_dict = f.read()
                decrypt_data = CipherManager.Decrypt_data(txt_dict, secret, salt=salt)
                d = json.loads(decrypt_data)
                return d
        except (json.JSONDecodeError, FileNotFoundError, InvalidToken, KeyError, ValueError, TypeError):
            continue

    # No pudimos descifrar el archivo: no romper la app, reiniciar estado.
    default_data = {"attempts": 0, "max_attempts": 3}
    save_attempts_data(default_data)
    return default_data


def save_attempts_data(data: dict):
    """Save the data in the .dat file."""
    dict_txt = json.dumps(data)
    encrypted_data = CipherManager.Encypt_data(
        dict_txt, _secret_key(), salt=_ATTEMPTS_SALT
    ).decode("utf-8")

    with open(_integrity_path(), "w", encoding="utf-8") as f:
        f.write(encrypted_data)


def register_failed_attempt():
    """Add one attempt and return the total."""
    data = get_attempts_data()
    data["attempts"] += 1
    save_attempts_data(data)

    return data


def trigger_self_destruct():
    """Physically delete sensitive system files."""
    if os.path.exists(getattr(config_module, "ROOT_DB", "")):
        try:
            os.remove(config_module.ROOT_DB)
        except OSError:
            pass

    if os.path.exists(_integrity_path()):
        try:
            os.remove(_integrity_path())
        except OSError:
            pass


def reset_attempts():
    """Reset the number of failed login attempts."""
    data = get_attempts_data()
    data["attempts"] = 0
    save_attempts_data(data)