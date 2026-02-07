"""Module responsible for managing login attempts and implementing security measures such as deleting the database after a certain number of failed attempts."""

import json
import os

from core.config import INTEGRETY_PATH, secure_folder, SECRET_KEY_ATTEMPTS, ROOT_DB
from security.encryption import CipherManager

def get_attempts_data() -> dict:
    """Read the file or create it with default values if it does not exist."""
    if not os.path.exists(secure_folder):
        os.makedirs(secure_folder)

    if not os.path.isfile(INTEGRETY_PATH):
        # Si no existe, creamos el estado inicial
        initial_data = {
            "attempts": 0,
            "max_attempts": 3
            }
        
        save_attempts_data(initial_data)
        return initial_data

    try:
        with open(INTEGRETY_PATH, "r", encoding='utf-8') as f:
            txt_dict = f.read ()
            decrypt_data = CipherManager.Decrypt_data (txt_dict, SECRET_KEY_ATTEMPTS)
            d = json.loads (decrypt_data)

            return d
        
    except (json.JSONDecodeError, FileNotFoundError):
        return {"attempts": 0, "max_attempts": 3}


def save_attempts_data(data: dict):
    """Save the data in the .dat file."""
    dict_txt = json.dumps (data)
        
    encrypted_data = CipherManager.Encypt_data (dict_txt, SECRET_KEY_ATTEMPTS).decode ('utf-8')

    with open(INTEGRETY_PATH, "w", encoding='utf-8') as f:
        f.write (encrypted_data)


def register_failed_attempt():
    """Add one attempt and return the total."""
    data = get_attempts_data()
    data["attempts"] += 1
    save_attempts_data(data)

    return data

def trigger_self_destruct ():
    """Physically delete sensitive system files."""
    try:
        if os.path.exists(ROOT_DB):
            os.remove(ROOT_DB)
        
        if os.path.exists(INTEGRETY_PATH):
            os.remove(INTEGRETY_PATH)
    except OSError as e:
        raise e

def reset_attempts():
    """Reset the number of failed login attempts."""
    data = get_attempts_data()
    data["attempts"] = 0
    save_attempts_data(data)    