from views.app import Views, Filters
from controllers.Database_controllers import *
from controllers.Auth_controller import login
from core.Exceptions import (
    AuthError,
    DataBaseError,
    CategoryError,
    InvalidParameterCountError,
    UrlError,
    RestrictionError,
    PasswordMismatchError,
    HashCorruptionError,
)
from utils.utils import Clearconsole, progress_bar
from models.safe_models import QuerySafe
from cryptography.fernet import InvalidToken
import time

import pdb


class orquestador:
    def __init__(self, view, db_safe):
        self.status = False
        self.view = view
        self.db_safe = db_safe
        self.result_query = None

        self.view_login()

    def view_login(self):
        while True:
            Clearconsole()
            self.view.Banner()
            credentials = self.view.inputCredentials()
            try:
                if login(credentials[0], credentials[1]):
                    progress_bar()
                    self.view.show_message("Successful login")
                    self.status = True
                    break
            except (AuthError, PasswordMismatchError, HashCorruptionError) as a:
                self.view.show_error(a)
                if self.view.ask("Do you want to go out? Y/N") == "N":
                    break

    def run(self):
        # Limpiamos la consola
        while True:
            Clearconsole()
            self.view.Banner()
            self.view.Menu()
            option = self.view.inputOption()

            match option:
                case 1:
                    # pdb.set_trace ()
                    try:
                        if Createtables():
                            self.view.show_message("Tables created successfully")
                            progress_bar()
                    except DataBaseError as db:
                        self.view.show_error(db)

                    finally:
                        time.sleep(1)
                case 2:
                    # pdb.set_trace ()
                    while True:
                        name_category = self.view.formcategoryInsert()
                        try:
                            Savecategory(name_category)
                        except DataBaseError as db:
                            self.view.show_error(db)
                        else:
                            progress_bar()
                            self.view.show_message(
                                f"{name_category} added successfully"
                            )
                            if self.view.ask() == "N":
                                break
                        finally:
                            time.sleep(1)

                case 3:
                    while True:
                        data = self.view.formInsert()
                        try:
                            SaveSafe(
                                self.db_safe,
                                data[0],
                                data[1],
                                data[2],
                                data[3],
                                data[4],
                                data[5],
                                data[6],
                                data[7],
                            )
                            progress_bar()
                            self.view.show_message("Data successfully insert")
                        except (
                            CategoryError,
                            InvalidParameterCountError,
                            DataBaseError,
                            UrlError,
                            AuthError,
                        ) as e:
                            self.view.show_error(e)

                        if self.view.ask() == "N":
                            break

                        time.sleep(1)

                case 4:
                    self.filters()

                case 5:
                    data = self.view.formUpdate()
                    try:
                        results = GETSitename(self.db_safe, data[0])
                        if results:
                            # mostrar datos antes de actualiza
                            self.view.show_data(results)
                            if self.view.ask() == "S":
                                UpdateDataSafe(self.db_safe, data)
                                progress_bar()
                                self.view.show_message(
                                    f"{results[0][2]} successfully update"
                                )
                            else:
                                self.view.show_message("Action successfully cancelled")
                    except DataBaseError as db:
                        self.view.show_error(db)
                    finally:
                        time.sleep(2)

                case 6:
                    id = self.view.formID()
                    try:
                        results = GetId(self.db_safe, id)
                        if results:
                            self.view.show_data(results)
                            if self.view.ask() == "S":
                                DeleteDataSafe(self.db_safe, id)
                                progress_bar()
                                self.view.show_message(
                                    f"{results[0][2]} successfully removed"
                                )
                            else:
                                self.view.show_message("Action successfully cancelled")
                    except (RowError, RestrictionError, DataBaseError) as db:
                        self.view.show_error(db)
                    finally:
                        time.sleep(2)

                case 7:
                    self.view.show_message("leaving  .....")
                    time.sleep(0.5)
                    break
                case _:
                    self.view.show_message("Option not available")

    def filters(self):
        while True:
            Clearconsole()
            self.view.Banner()
            Filters.Menu_filter()

            option = self.view.inputOption()
            match option:
                case 1:
                    try:
                        results = GetEverything(self.db_safe)
                        self.view.show_message("consulting data")
                        progress_bar()
                        Filters.show_dataFilter(results, title="CATEGORY SEARCH")
                    except (DataBaseError, InvalidToken) as dbError:
                        self.view.show_error(dbError)

                    if self.view.ask() == "S":
                        continue
                case 2:
                    username = self.view.formSitename()
                    try:
                        results = GETSitename(self.db_safe, username)
                        self.view.show_message("consulting data")
                        progress_bar()
                        self.view.show_data(results, title="WEBSITE SEARCH")
                    except RowError as re:
                        self.view.show_error(re)

                    if self.view.ask() == "N":
                        continue

                case 3:
                    category = self.view.formcategoryInsert()
                    try:
                        results = GetdataCategory(self.db_safe, category)
                        self.view.show_message("consulting data")
                        progress_bar()
                        Filters.show_dataFilter(results, title="CATEGORY SEARCH")
                    except (RowError, InvalidParameterCountError) as re:
                        self.view.show_error(re)

                    if self.view.ask() == "N":
                        continue

                case 4:
                    data = Filters.form_yearmonth()
                    try:
                        results = GetdataLastchange(self.db_safe, data[0], data[1])
                        self.view.show_message("consulting data")
                        progress_bar()
                        Filters.show_dataFilter(results, title="LAST CHANGE SEARCH")
                    except RowError as re:
                        self.view.show_error(re)

                    if self.view.ask() == "N":
                        continue

                case 5:
                    data = Filters.form_yearyear()
                    try:
                        results = GetdataRange_Lastchange(
                            self.db_safe, data[0], data[1]
                        )
                        self.view.show_message("consulting data")
                        progress_bar()
                        Filters.show_dataFilter(results, title="LAST CHANGE SEARCH")
                    except RowError as re:
                        self.view.show_error(re)

                    if self.view.ask() == "N":
                        continue

                case 6:
                    self.view.show_message("leaving  .....")
                    time.sleep(0.5)
                    break
                case _:
                    self.view.show_message("Option not available")


if __name__ == "__main__":
    view = Views()
    db_safe = QuerySafe()
    data = orquestador(view, db_safe)
    if data.status:
        data.run()
