"""Main module for the GSIS-CLI application."""

import time

from views.app import Views, Filters
from controllers.Database_controllers import (
    Createtables, SaveSafe, DeleteDataSafe, GetdataCategory, 
    GetdataLastchange, GetdataRange_Lastchange, GetEverything, 
    GetId, GETSitename, UpdateDataSafe, Savecategory, delete_category
)
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

from core.Exceptions import RowError



class Orchestrator:
    """Coordinates the main flow of the GSIS-CLI application."""
    def __init__(self, view, db_safe):
        self.status = False
        self.session_password = None
        self.view = view
        self.db_safe = db_safe

        self.view_login()

    def view_login(self):
        """Function responsible for handling the user login process, including credential validation and error handling."""
        while True:
            Clearconsole()
            self.view.Banner()
            credentials = self.view.inputCredentials()
            try:
                success, self.session_password = login(credentials[0], credentials[1])
                if success:
                    progress_bar()
                    self.view.show_message("Successful login")
                    self.status = True
                    break
            except (AuthError, PasswordMismatchError, HashCorruptionError) as a:
                self.view.show_error(a)
                if self.view.ask("Do you want to go out? Y/N") == "N":
                    break

    def run(self):
        """Function responsible for running the main loop of the application, handling user interactions, and coordinating database operations based on user input."""
        # Limpiamos la consola
        while True:
            Clearconsole()
            self.view.Banner()
            self.view.Menu()
            option = self.view.inputOption()

            match option:
                case 1:
                    # created tables
                    try:
                        if Createtables():
                            progress_bar()
                            self.view.show_message("Tables created successfully")
                    except DataBaseError as db:
                        self.view.show_error(db)

                    finally:
                        time.sleep(3)
                case 2:
                    # add category
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
                    category = self.view.formcategoryInsert ()
                    try:
                        delete_category (category)
                        progress_bar()
                        self.view.show_message(f"{category} removed successfully")  
                    except (CategoryError, InvalidParameterCountError) as ce:
                        self.view.show_error(ce)
                    
                    time.sleep (5)
                        
                case 4:
                    # add data to safe
                    while True:
                        data = self.view.formInsert()
                        try:
                            SaveSafe(
                                self.db_safe, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], master_password=self.session_password
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

                case 5:
                    # filter data
                    self.filters()

                case 6:
                    # update data
                    data = self.view.formUpdate()
                    try:
                        results = GETSitename(self.db_safe, data[0], master_password=self.session_password)
                        if results:
                            # mostrar datos antes de actualiza
                            self.view.show_data(results)
                            if self.view.ask() == "S":
                                UpdateDataSafe(self.db_safe, data, master_password=self.session_password)
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

                case 7:
                    # delete data
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

                case 8:
                    # exit
                    self.view.show_message("leaving  .....")
                    time.sleep(0.5)
                    break
                case _:
                    self.view.show_message("Option not available")

    def filters(self):
        """Function responsible for handling the filter data."""
        while True:
            Clearconsole()
            self.view.Banner()
            Filters.Menu_filter()

            option = self.view.inputOption()
            match option:
                case 1:
                    try:
                        results = GetEverything(self.db_safe, master_password=self.session_password)
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
                        results = GETSitename(self.db_safe, username, master_password=self.session_password)
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
                        results = GetdataCategory(self.db_safe, category, master_password=self.session_password)
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
                        results = GetdataLastchange(self.db_safe, data[0], data[1], master_password=self.session_password)
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
                            self.db_safe, data[0], data[1], master_password=self.session_password
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
    try:
        view = Views()
        db_safe = QuerySafe()
        data = Orchestrator(view, db_safe)
        if data.status:
            data.run()
    except KeyboardInterrupt:
        view.show_message("leaving  .....")
        time.sleep(0.5)
