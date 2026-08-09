"""Estilos ANSI para una interfaz de consola profesional.

Todos los helpers son agnósticos a la plataforma (Windows moderno soporta
secuencias ANSI tras habilitar el terminal virtual).
"""

import os
import sys


def enable_ansi():
    """Habilita secuencias ANSI y salida UTF-8 en consolas Windows modernas."""
    if os.name == "nt":
        try:
            import ctypes

            kernel32 = ctypes.windll.kernel32
            handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
            mode = ctypes.c_uint32()
            if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
                kernel32.SetConsoleMode(handle, mode.value | 0x0004)
        except Exception:
            pass

    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


# --- Paleta (True-Color portable al 16 colores) ---
class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"

    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    GRAY = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"


def paint(text, *codes) -> str:
    """Envuelve un texto con los códigos ANSI dados."""
    if not codes:
        return text
    return "".join(codes) + str(text) + C.RESET


def success(text) -> str:
    return paint("✔ ", C.BRIGHT_GREEN, C.BOLD) + paint(text, C.GREEN)


def error(text) -> str:
    return paint("✘ ", C.BRIGHT_RED, C.BOLD) + paint(text, C.RED)


def warning(text) -> str:
    return paint("⚠ ", C.BRIGHT_YELLOW, C.BOLD) + paint(text, C.YELLOW)


def info(text) -> str:
    return paint("» ", C.BRIGHT_CYAN, C.BOLD) + paint(text, C.CYAN)


def prompt(text) -> str:
    return paint(text, C.BRIGHT_CYAN) + paint(" :: ", C.DIM)