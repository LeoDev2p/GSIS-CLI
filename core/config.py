"""Module for managing configuration settings and constants for the application."""

from pathlib import Path
from dotenv import load_dotenv
import os
from argon2 import PasswordHasher

# Raiz base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent


# Cargamos las variables de entorno
load_dotenv(BASE_DIR / ".env")

# Configuracion generales
NAME_BD = os.getenv("NAME_BD")
ROOT_DB = BASE_DIR / "db" / NAME_BD
LOG_FILE = BASE_DIR / "log" / "security.log"

SUPERUSER = os.getenv("SUPERUSER")
MASTER_KEY = os.getenv("MASTER_KEY")

MASTER_PASSWORD_HASH  = os.getenv("MASTER_KEY")
SALT = os.getenv("SALT")

SECRET_KEY_ATTEMPTS = os.getenv("SECRET_KEY_ATTEMPTS")

# config Argon2
ARGON2_SETTING = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=2)

#* Do not configure
app_data = os.getenv('APPDATA') 
secure_folder = os.path.join(app_data, "SystemCacheLogs")
INTEGRETY_PATH = os.path.join(secure_folder, "win_sys_32.dat")

