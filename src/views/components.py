"""Módulo responsable de gestionar la interfaz de línea de comandos.

Provee banner, menús enmarcados, tablas con bordes y mensajes estilizados.
"""

from src.utils.utils import lengthText
from src.views.style import C, paint, success, error, info


def Banner():
    """Banner tipográfico grande y legible, con versión y autor."""
    KRYPTA = [
            "██  ██ ██████  ██████ ██████  ████████  ▄████▄", 
            "██ ▄█  ██▄▄██▄   ██   ██▄▄██▄    ██     ██▄▄██",   
            "██▀██  ██   ██ ██████ ██         ██     ██  ██" ,
    ]
    print()
    for line in KRYPTA:
        print(paint(line, C.BRIGHT_CYAN, C.BOLD))
    print(paint("   · · ·  Bóveda segura de credenciales · FERNET + PBKDF2  · · ·", C.DIM))
    print()
    print(paint("   Versión ", C.DIM) + paint("v0.2.0", C.BRIGHT_GREEN, C.BOLD))
    print(paint("   Autor   ", C.DIM) + paint("LeoDev2p", C.BRIGHT_MAGENTA))
    print(paint("   Cifrado  ", C.DIM) + paint("FERNET · PBKDF2 · SHA-256", C.BRIGHT_CYAN))
    print()


def _menu(title: str, items: list[str]) -> None:
    """Menú minimalista estilo interfaz moderna de terminal."""
    print(paint(f"  {title}", C.BRIGHT_CYAN, C.BOLD))
    for i, item in enumerate(items, start=1):
        etiqueta = f"{i:02d}"
        print(paint(f"    {etiqueta}  ", C.BRIGHT_CYAN, C.BOLD) + paint(item, C.WHITE))
    print(paint("  " + "·" * 30, C.DIM))


class Menu:
    """Gestiona la interfaz de menús."""

    @staticmethod
    def Menu():
        _menu(
            "Krypta · Menú principal",
            [
                "Crear base de datos",
                "Agregar categorías",
                "Eliminar categorías",
                "Agregar datos",
                "Consultar datos",
                "Actualizar datos",
                "Eliminar datos",
                "Salir",
            ],
        )

    @staticmethod
    def Menu_select():
        _menu(
            "Seleccionar registro",
            [
                "Ver todos los registros",
                "Buscar por coincidencia (LIKE)",
                "Cancelar",
            ],
        )

    @staticmethod
    def Menu_filter():
        _menu(
            "Krypta · Consultas",
            [
                "Ver todos",
                "Filtrar por nombre del sitio",
                "Filtrar por categoría",
                "Filtrar por año y mes",
                "Filtrar por rango de fechas",
                "Volver al menú principal",
            ],
        )

    @staticmethod
    def menu_config_user():
        _menu("Configuración", ["Registrar credenciales"])


class Table:
    """Tablas con bordes y columnas alineadas."""

    @staticmethod
    def _render(rows, headers, title="RESULTADOS"):
        if not rows:
            print(error("Sin resultados."))
            return

        anchos = []
        for i, header in enumerate(headers):
            ancho = max(len(str(fila[i])) for fila in rows)
            anchos.append(max(ancho, len(header)) + 2)

        interior = "┬".join("─" * w for w in anchos)
        media = "┼".join("─" * w for w in anchos)
        fondo = "┴".join("─" * w for w in anchos)

        print(paint("┌" + interior + "┐", C.DIM))
        if title:
            print(paint("│", C.DIM) + paint(title.center(sum(anchos) + len(anchos) - 1, " "), C.BRIGHT_WHITE, C.BOLD) + paint("│", C.DIM))
            print(paint("├" + media + "┤", C.DIM))

        header_line = paint("│", C.DIM)
        for i, header in enumerate(headers):
            header_line += paint(header.ljust(anchos[i] - 1) + "│", C.BRIGHT_CYAN, C.BOLD)
        print(header_line)
        print(paint("├" + media + "┤", C.DIM))

        for fila in rows:
            linea = paint("│", C.DIM)
            for i, valor in enumerate(fila):
                texto = str(valor)
                linea += paint(texto.ljust(anchos[i] - 1) + "│", C.WHITE)
            print(linea)
        print(paint("└" + fondo + "┘", C.DIM))
        print()


class ShowConsole:
    """Salidas de consola: mensajes, errores y tablas."""

    @staticmethod
    def show_message(message: str):
        print(message)

    @staticmethod
    def show_error(message):
        code = getattr(message, "code", None)
        texto = str(message)
        if code:
            print(error(f"Error {code}: {texto}"))
        else:
            print(error(texto))

    @staticmethod
    def show_data(row_data: list[tuple], title="RESULTS"):
        Table._render(row_data, ["Id", "Categoría", "Sitio", "Email", "Password"], title)

    @staticmethod
    def show_dataFilter(row_data: list[tuple], title="RESULTS"):
        Table._render(
            row_data,
            ["Id", "Categoría", "Sitio", "Email", "Password", "Expira"],
            title,
        )


class Filters:
    """Compatibilidad con el flujo existente de consultas."""

    @staticmethod
    def show_dataFilter(row_data: list[tuple], title="RESULTS"):
        ShowConsole.show_dataFilter(row_data, title)