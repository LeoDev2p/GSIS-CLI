# from src.core.config import ROOT_DB
# import os
from src.views.forms import Forms
from src.views.components import ShowConsole
from src.views.style import enable_ansi, success, info, warning, error as style_error
from src.utils.utils import search_usb
from src.utils.utils import Clearconsole

enable_ansi()

class ConfigApp:
    def __init__(self, controller, banner):
        self.controller = controller
        self.banner = banner

    def run(self):
        while True:
            Clearconsole()
            self.banner()
            unidad = search_usb()
            if not unidad:
                ShowConsole.show_message(warning("Inserte una unidad extraíble."))
                if Forms.ask(message="Reintentar análisis [Y/N]") != "Y":
                    return False
                continue

            ShowConsole.show_message(info("Selecciona una unidad:"))
            for c, u in enumerate(unidad):
                ShowConsole.show_message(f"   {c} : {u}")

            ShowConsole.show_message("\n")
            option = Forms.inputOption()
            try:
                usb = unidad[option]
            except (IndexError, TypeError):
                ShowConsole.show_error("Unidad no disponible")
                continue

            data = Forms.form_login()
            data['unidad'] = usb

            try:
                self.controller.auth.register(**data)
                ShowConsole.show_message(success("Credenciales escritas en el USB"))
            except Exception as e:
                ShowConsole.show_error(e)
                continue

            return True