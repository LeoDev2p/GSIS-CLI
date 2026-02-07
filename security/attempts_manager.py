"""Module responsible for managing login attempts and implementing security measures such as deleting the database after a certain number of failed attempts."""

import json
import os
from core.config import JSON_PATH, secure_folder

def get_attempts_data():
    """Read the file or create it with default values if it does not exist."""
    if not os.path.exists(secure_folder):
        os.makedirs(secure_folder)

    if not os.path.exists(JSON_PATH):
        # Si no existe, creamos el estado inicial
        initial_data = {"attempts": 0}
        save_attempts_data(initial_data)
        return initial_data

    try:
        with open(JSON_PATH, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {"attempts": 0}

def save_attempts_data(data):
    """Save the data in the .dat file."""
    with open(JSON_PATH, "w") as f:
        json.dump(data, f, separators=(',', ':'))

def register_failed_attempt():
    """Add one attempt and return the total."""
    data = get_attempts_data()
    data["attempts"] += 1
    save_attempts_data(data)
    return data["attempts"]


"""

"""