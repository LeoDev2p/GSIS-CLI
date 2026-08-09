"""Main module for the GSIS-CLI application."""

import time
import os

from src.core.config import ROOT_DB, refresh_credentials
from src.views.components import Menu, ShowConsole, Filters, Banner
from src.views.forms import Forms
from src.views.config import ConfigApp

from src.core.Exceptions import (
    AuthError,
    DataBaseError,
    CategoryError,
    InvalidParameterCountError,
    UrlError,
    RestrictionError,
    PasswordMismatchError,
    HashCorruptionError,
    SecurityError,
    RowError
)
from src.utils.utils import Clearconsole, progress_bar, search_usb
from src.views.style import enable_ansi, C, paint, success, info, warning, error as style_error
from cryptography.fernet import InvalidToken

enable_ansi()

class App:
    """Coordinates the main flow of the GSIS-CLI application."""

    def __init__(self, controller):
        self.config_app = ConfigApp(controller, Banner) 
        self.status = False
        self.session_password = None

        self.controller = controller

        if not os.path.exists(ROOT_DB):
            self.config_app.run()

        self.view_login()

    def verify_usb_credentials(self) -> bool:
        """Verifica la conexión del USB y la validez de las credenciales maestras antes de solicitar el login."""
        ShowConsole.show_message(paint("[1/2] Verificando USB conectado...", C.BRIGHT_CYAN))
        time.sleep(0.9)
        usbs = search_usb()
        if not usbs:
            ShowConsole.show_message(warning("No se detectó ningún USB conectado."))
            return False

        ShowConsole.show_message(paint("[2/2] Revisando credenciales...", C.BRIGHT_CYAN))
        time.sleep(0.9)
        if not refresh_credentials():
            ShowConsole.show_message(warning("Credenciales no encontradas en el USB."))
            return False

        if not os.path.exists(ROOT_DB):
            ShowConsole.show_message(info("Base de datos no encontrada. Se creará al iniciar el menú."))
        else:
            time.sleep(0.6)
            ShowConsole.show_message(success("Base de datos encontrada."))

        return True

    def view_login(self):
        """Function responsible for handling the user login process, including credential validation and error handling."""
        while True:
            Clearconsole()
            Banner()

            if not self.verify_usb_credentials():
                if Forms.ask("Reintentar verificacion [S/N]") != "S":
                    break
                continue

            credentials = Forms.inputCredentials()
            try:
                self.session_password = self.controller.auth.login(credentials[0], credentials[1])
                if self.session_password:
                    progress_bar()
                    ShowConsole.show_message(success("Sesión iniciada correctamente."))
                    self.status = True
                    break
            except (
                SecurityError,
                PasswordMismatchError,
                HashCorruptionError,
                AuthError,
                InvalidToken,
            ) as a:
                ShowConsole.show_error(a)

            if Forms.ask("Do you want to retry loging [Y/N]") != "Y":
                break

    def list_categories(self):
        """Lista las categorías existentes antes de agregar o eliminar."""
        categorias = self.controller.safe.GetCategories()
        if not categorias:
            ShowConsole.show_message("[:] No hay categorías registradas.")
            return
        ShowConsole.show_message("[:] Categorías existentes:")
        for id, name in categorias:
            ShowConsole.show_message(f"   - {name}")

    def _select_record(self) -> list[list] | None:
        """Muestra una tabla para que el usuario elija un registro sin adivinar el id.

        Permite ver todos los registros o buscar por coincidencia (LIKE) en el
        nombre del sitio o categoría. Devuelve las filas que coinciden para que el
        flujo de update/delete muestre la fila elegida, o None si se cancela.
        """
        while True:
            Clearconsole()
            Banner()
            Menu.Menu_select()
            option = Forms.inputOption()

            if option == 3:
                return None

            try:
                if option == 1:
                    results = self.controller.safe.GetEverything(
                        master_password=self.session_password
                    )
                    Filters.show_dataFilter(results, title="REGISTROS DISPONIBLES")
                elif option == 2:
                    termino = Forms.formSitename()
                    results = self.controller.safe.SearchSitename(
                        termino, master_password=self.session_password
                    )
                    Filters.show_dataFilter(results, title="COINCIDENCIAS")
                else:
                    ShowConsole.show_message(warning("Opción no disponible"))
                    continue
            except (DataBaseError, RowError, InvalidToken) as e:
                ShowConsole.show_error(e)
                if Forms.ask("Reintentar [S/N]") != "S":
                    return None
                continue

            if not results:
                ShowConsole.show_message(warning("No hay registros."))
            return results

    def run(self):
        """Function responsible for running the main loop of the application, handling user interactions, and coordinating database operations based on user input."""
        # Limpiamos la consola
        while True:
            Clearconsole()
            Banner()
            Menu.Menu()
            option = Forms.inputOption()

            match option:
                case 1:
                    # created tables
                    try:
                        if os.path.exists(ROOT_DB):
                            ShowConsole.show_message(info("La base de datos ya existe"))
                        elif self.controller.safe.Createtables():
                            progress_bar()
                            ShowConsole.show_message(success("Tables created successfully"))
                    except DataBaseError as db:
                        ShowConsole.show_error(db)

                    finally:
                        time.sleep(3)
                case 2:
                    # add category
                    self.list_categories()
                    while True:
                        name_category = Forms.formcategoryInsert()
                        try:
                            self.controller.safe.Savecategory(name_category)
                        except DataBaseError as db:
                            ShowConsole.show_error(db)
                        else:
                            progress_bar()
                            ShowConsole.show_message(success(f"{name_category} added successfully"))
                            if Forms.ask() == "N":
                                break
                        finally:
                            time.sleep(1)
                case 3:
                    self.list_categories()
                    category = Forms.formcategoryInsert()
                    try:
                        self.controller.safe.delete_category(category)
                        progress_bar()
                        ShowConsole.show_message(success(f"{category} removed successfully"))
                    except (CategoryError, InvalidParameterCountError) as ce:
                        ShowConsole.show_error(ce)

                    time.sleep(5)

                case 4:
                    # add data to safe
                    while True:
                        data = Forms.formInsert()
                        try:
                            self.controller.safe.SaveSafe(
                                data[0],data[1],
                                data[2],data[3],data[4],data[5],
                                data[6],data[7],master_password=self.session_password,
                            )
                            progress_bar()
                            ShowConsole.show_message(success("Data successfully insert"))
                        except (
                            CategoryError,
                            InvalidParameterCountError,
                            DataBaseError,
                            UrlError,
                            AuthError,
                        ) as e:
                            ShowConsole.show_error(e)

                        if Forms.ask() == "N":
                            break

                        time.sleep(1)

                case 5:
                    # filter data
                    self.filters()

                case 6:
                    # update data
                    results = self._select_record()
                    if not results:
                        time.sleep(2)
                        continue

                    id = Forms.formID()
                    fila = next((r for r in results if r[0] == id), None)
                    if fila is None:
                        ShowConsole.show_message("El ID no está en la tabla mostrada.")
                        time.sleep(2)
                        continue

                    data = Forms.formUpdate()
                    try:
                        ShowConsole.show_data([fila], title="DATA TO UPDATE")
                        if Forms.ask() == "S":
                            self.controller.safe.UpdateDataSafe(
                                data,
                                id=id,
                                master_password=self.session_password,
                            )
                            progress_bar()
                            ShowConsole.show_message(
                                success(f"{fila[2]} successfully updated")
                            )
                        else:
                            ShowConsole.show_message(info("Action successfully cancelled"))
                    except DataBaseError as db:
                        ShowConsole.show_error(db)
                    finally:
                        time.sleep(3)

                case 7:
                    # delete data
                    results = self._select_record()
                    if not results:
                        time.sleep(2)
                        continue

                    id = Forms.formID()
                    if next((r for r in results if r[0] == id), None) is None:
                        ShowConsole.show_message("El ID no está en la tabla mostrada.")
                        time.sleep(2)
                        continue
                    try:
                        results = self.controller.safe.GetId(id, master_password=self.session_password)
                        if results:
                            ShowConsole.show_data(results, title="DATA TO DELETE")
                            if Forms.ask() == "S":
                                self.controller.safe.DeleteDataSafe(id)
                                progress_bar()
                                ShowConsole.show_message(
                                    success(f"{results[0][2]} successfully removed")
                                )
                            else:
                                ShowConsole.show_message(info("Action successfully cancelled"))
                    except (RowError, RestrictionError, DataBaseError) as db:
                        ShowConsole.show_error(db)
                    finally:
                        time.sleep(2)

                case 8:
                    # exit
                    ShowConsole.show_message(info("Saliendo..."))
                    time.sleep(0.5)
                    break
                case _:
                    ShowConsole.show_message(warning("Opción no disponible"))

    def filters(self):
        """Function responsible for handling the filter data."""
        while True:
            Clearconsole()
            Banner()
            Menu.Menu_filter()

            option = Forms.inputOption()
            match option:
                case 1:
                    try:
                        results = self.controller.safe.GetEverything(
                            master_password=self.session_password
                        )
                        ShowConsole.show_message(info("Consultando datos..."))
                        progress_bar()
                        Filters.show_dataFilter(results, title="CATEGORY SEARCH")
                    except (DataBaseError, InvalidToken) as dbError:
                        ShowConsole.show_error(dbError)

                    if Forms.ask() == "S":
                        continue
                case 2:
                    username = Forms.formSitename()
                    try:
                        results = self.controller.safe.GETSitename(
                            username,
                            master_password=self.session_password,
                        )
                        ShowConsole.show_message(info("Consultando datos..."))
                        progress_bar()
                        ShowConsole.show_data(results, title="WEBSITE SEARCH")
                    except RowError as re:
                        ShowConsole.show_error(re)

                    if Forms.ask() == "N":
                        continue

                case 3:
                    category = Forms.formcategoryInsert()
                    try:
                        results = self.controller.safe.GetdataCategory(
                            category,
                            master_password=self.session_password,
                        )
                        ShowConsole.show_message(info("Consultando datos..."))
                        progress_bar()
                        Filters.show_dataFilter(results, title="CATEGORY SEARCH")
                    except (RowError, InvalidParameterCountError) as re:
                        ShowConsole.show_error(re)

                    if Forms.ask() == "N":
                        continue

                case 4:
                    data = Forms.form_yearmonth()
                    try:
                        results = self.controller.safe.GetdataLastchange(
                            data[0],
                            data[1],
                            master_password=self.session_password,
                        )
                        ShowConsole.show_message(info("Consultando datos..."))
                        progress_bar()
                        Filters.show_dataFilter(results, title="LAST CHANGE SEARCH")
                    except RowError as re:
                        ShowConsole.show_error(re)

                    if Forms.ask() == "N":
                        continue

                case 5:
                    data = Forms.form_yearyear()
                    try:
                        results = self.controller.safe.GetdataRange_Lastchange(
                            data[0],
                            data[1],
                            master_password=self.session_password,
                        )
                        ShowConsole.show_message(info("Consultando datos..."))
                        progress_bar()
                        Filters.show_dataFilter(results, title="LAST CHANGE SEARCH")
                    except RowError as re:
                        ShowConsole.show_error(re)

                    if Forms.ask() == "N":
                        continue

                case 6:
                    ShowConsole.show_message(info("Volviendo al menú principal..."))
                    time.sleep(0.5)
                    break
                case _:
                    ShowConsole.show_message(warning("Opción no disponible"))



