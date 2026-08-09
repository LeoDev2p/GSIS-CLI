"""Module with utility functions for the application, including console management, date handling, text length calculation, and a progress bar display."""

import os
import platform
import re
import time
from datetime import date
from pathlib import Path


def Clearconsole():
    """Clear the console screen based on the operating system."""
    if os.name == "nt":
        _ = os.system("cls")
    else:
        _ = os.system("clear")


def date_today():
    """Fetch the current date and return it as a string in 'YYYY-MM-DD' format."""
    d = date.today().strftime("%Y-%m-%d")
    return d


def lengthText(lista, index):
    """Longitud máxima de una columna, tolerando None/int/NoneType."""
    longitudes = []
    for fila in lista:
        try:
            valor = fila[index]
        except (IndexError, TypeError):
            continue
        if valor is None:
            longitudes.append(0)
        else:
            longitudes.append(len(str(valor)))
    return max(longitudes, default=0)


def progress_bar(total=40):
    """Barra de progreso compacta y limpia."""
    from src.views.style import C, paint

    print()
    for i in range(total + 1):
        filled = i / total
        completado = int(filled * 40)
        barra = "█" * completado + "░" * (40 - completado)
        color = C.BRIGHT_GREEN if filled < 1 else C.BRIGHT_CYAN
        print(f"\r{paint(f'  [{barra}] {filled*100:5.0f}%' , color)}", end="", flush=True)
        time.sleep(0.04)
    print("\n")


def search_usb():
    sistema = platform.system()
    usbs_encontrados = []

    # --- 1. DETECCIÓN EN WINDOWS ---
    if sistema == "Windows":
        import string

        for letra in string.ascii_uppercase:
            ruta = f"{letra}:\\"
            if not os.path.exists(ruta):
                continue
            if letra == "C":
                continue
            try:
                import ctypes

                # 1=NO_ROOT_DIR 2=REMOVABLE 3=FIXED 4=NETWORK 5=CDROM 6=RAMDISK
                tipo_disco = ctypes.windll.kernel32.GetDriveTypeW(ruta)
                # Se incluyen USB removibles (2) y USB que Windows monta como
                # disco fijo (3, p.ej. NTFS/exFAT, modo "HDD"), verificando que
                # en el ISO exista la carpeta de llaves que corresponde.
                if tipo_disco in (2, 3):
                    usbs_encontrados.append(ruta)
            except Exception:
                usbs_encontrados.append(ruta)

    # --- 2. DETECCIÓN EN LINUX ---
    elif sistema == "Linux":
        ruta_media = "/media"
        if os.path.exists(ruta_media):
            for usuario in os.listdir(ruta_media):
                ruta_usuario = os.path.join(ruta_media, usuario)
                if os.path.isdir(ruta_usuario):
                    for dispositivo in os.listdir(ruta_usuario):
                        usbs_encontrados.append(os.path.join(ruta_usuario, dispositivo))

    # --- 3. DETECCIÓN EN MACOS (DARWIN) ---
    elif sistema == "Darwin":
        ruta_volumes = "/Volumes"
        if os.path.exists(ruta_volumes):
            for dispositivo in os.listdir(ruta_volumes):
                if dispositivo != "Macintosh HD":
                    usbs_encontrados.append(os.path.join(ruta_volumes, dispositivo))

    else:
        print("Sistema operativo no soportado para detección automática.")

    return usbs_encontrados

def is_key_file(nombre_archivo: str) -> bool:
    """Devuelve True si el archivo parece una llave (termina en .key o contiene 'clave')."""
    nombre = str(nombre_archivo).lower()
    return nombre.endswith(".key") or "clave" in nombre


def find_key_file(nombre_carpeta_objetivo="key") -> Path | None:
    """Busca la carpeta 'key' (o un .key suelto) en los USB conectados y devuelve el archivo de llaves, o None.

    Busca tanto en la raíz del USB (USB/key.key o USB/clave.txt) como dentro
    de subcarpetas (USB/Secure/key) y recursivamente hasta 3 niveles de profundidad.
    """
    unidades = search_usb()
    if not unidades:
        print("[Krypta] No se detectó ningún USB conectado.")
        return None

    target = nombre_carpeta_objetivo.strip().lower()

    # --- búsqueda recursiva de la carpeta objetivo y de keys sueltos ---
    def _es_carpeta_objetivo(p: Path | None) -> bool:
        return p is not None and p.is_dir() and p.name.lower() == target

    def _buscar_recursivo(path: Path, profundidad: int):
        if profundidad <= 0:
            return None
        try:
            for elemento in path.iterdir():
                try:
                    if not elemento.is_dir():
                        # archivo suelto de llave en la raíz/subcarpeta
                        if is_key_file(elemento.name):
                            return elemento
                        continue

                    if _es_carpeta_objetivo(elemento):
                        for archivo in elemento.iterdir():
                            if archivo.is_file() and is_key_file(archivo.name):
                                return archivo

                    resultado = _buscar_recursivo(elemento, profundidad - 1)
                    if resultado:
                        return resultado
                except PermissionError:
                    continue
                except OSError:
                    continue
        except PermissionError:
            return None
        except OSError:
            return None
        return None

    for ruta_usb in unidades:
        # verificar cualquier .key suelto en la raíz del USB
        hay_key_suelto = None
        try:
            for archivo in Path(ruta_usb).iterdir():
                if archivo.is_file() and is_key_file(archivo.name):
                    hay_key_suelto = archivo
                    break
        except OSError:
            pass
        if hay_key_suelto:
            return hay_key_suelto

        resultado = _buscar_recursivo(Path(ruta_usb), 3)
        if resultado:
            return resultado

    return None


def search_key(nombre_carpeta_objetivo="key") -> str | None:
    """Busca el archivo de llave en los USB conectados y devuelve su contenido de texto, o None."""
    archivo = find_key_file(nombre_carpeta_objetivo)
    if archivo is None:
        return None
    try:
        return archivo.read_text(encoding="utf-8").strip()
    except OSError as e:
        print(f"Error al leer el archivo de clave: {e}")
        return None


def parse_key_credentials(content: str | None) -> dict | None:
    """Parsea MASTER_KEY y SALT desde el contenido del archivo de llaves del USB.

    Soporta dos formatos:
      - Moderno:  MASTER_KEY='aldo...'\\nSALT='base64...' (con o sin comillas)
      - Legacy:   "MASTER_KEY=<hash>SALT=<SALT=base64>" (una sola linea)
    """
    if not content:
        return None

    texto = content.strip()

    def _buscar(patrones: list) -> str | None:
        for patron in patrones:
            m = re.search(patron, texto)
            if m:
                return m.group(1)
        return None

    patrones_master = [
        r"MASTER_KEY\s*=\s*['\"]([^'\"]+)['\"]",
        r"MASTER_KEY\s*=\s*<([^>]+)>",
        r"MASTER_KEY\s*=\s*([^\s>'\"}]+)",
    ]

    patrones_salt = [
        r"SALT\s*=\s*['\"]([^'\"]+)['\"]",
        r"SALT\s*=\s*<SALT=([^>]+)>",
        r"SALT\s*=\s*<([^>]+)>",
        r"SALT\s*=\s*([^\s>'\"}]+)",
    ]

    master = _buscar(patrones_master)
    salt = _buscar(patrones_salt)

    if not master or not salt:
        return None

    return {"MASTER_KEY": master, "SALT": salt}


def load_key_credentials(nombre_carpeta_objetivo="key") -> dict | None:
    """Busca y parseta las credenciales maestras (MASTER_KEY y SALT) desde el USB."""
    return parse_key_credentials(search_key(nombre_carpeta_objetivo))

