from pathlib import Path
from dotenv import load_dotenv
import os

# Raiz base del proyecto
BASE_DIR = Path (__file__).resolve ().parent.parent


# Cargamos las variables de entorno
load_dotenv (BASE_DIR / '.env')

# Configuracion generales
NAME_BD = os.getenv ("NAME_BD")
ROOT_DB = BASE_DIR / 'db' / NAME_BD
LOG_FILE = BASE_DIR / "log" / 'security.log'

SUPERUSER = os.getenv ("SUPERUSER")
MASTER_KEY = os.getenv ("MASTER_KEY")


