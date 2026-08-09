"""Module for managing configuration settings and constants for the application."""

import os
from pathlib import Path

from argon2 import PasswordHasher
from dotenv import load_dotenv

from src.utils.utils import load_key_credentials


# Raiz base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Cargamos las variables de entorno
load_dotenv(BASE_DIR / ".env")

# Configuracion generales
NAME_BD = os.getenv("NAME_BD")
ROOT_DB = BASE_DIR / "storage" / "db" / NAME_BD
LOG_FILE = BASE_DIR / "storage" / "log" / "security.log"

SUPERUSER = os.getenv("SUPERUSER")

# MASTER_KEY (hash Argon2) y SALT (para PBKDF2/Fernet) salen del USB via key/key.key.
def refresh_credentials():
    """Recarga las credenciales maestras (MASTER_KEY y SALT) desde el USB."""
    global MASTER_KEY, SALT
    credenciales = load_key_credentials() or {}
    MASTER_KEY = credenciales.get("MASTER_KEY")
    SALT = credenciales.get("SALT")
    return bool(MASTER_KEY and SALT)

refresh_credentials()

SECRET_KEY_ATTEMPTS = os.getenv("SECRET_KEY_ATTEMPTS")

# config Argon2
ARGON2_SETTING = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=2)

# * Do not configure
app_data = os.getenv("APPDATA")
secure_folder = os.path.join(app_data, "SystemCacheLogs")
INTEGRETY_PATH = os.path.join(secure_folder, "win_sys_32.dat")
