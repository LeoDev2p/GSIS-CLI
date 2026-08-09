"""Module responsible for handling database operations related to the safe and category management."""

from typing import Any
from src.core.Exceptions import DataBaseError, CategoryError, UrlError, RowError
from src.utils.utils import date_today
from src.utils.validation import valitacion_email, validacion_link
from src.security.encryption import CipherManager

class Safe:
    def __init__ (self, table, safe, category):
        self.table = table
        self.safe = safe
        self.category = category

    def Createtables(self):
        """Create the necessary tables for the application if they do not exist."""
        self.table.createTableSafe()
        self.table.creatTablecategory()

        return True


    def Savecategory(self, category):
        """Save a new category to the database."""
        self.category._SQL_insert(category)

    def GetCategories(self) -> list[tuple]:
        """Return all existing categories from the database."""
        try:
            return self.category._SQL_getAll()
        except Exception:
            return []

    def delete_category(self, category):
        """Delete a category from the database based on the provided name."""
        result = self.category._SQL_select(category)
        if not result:
            raise CategoryError("category does not exist")

        id_category = result[0][0]
        self.category._SQL_delete(id_category)


    @valitacion_email
    def SaveSafe(self, *args: Any, master_password: str = ""):
        """Save sensitive data to the database after validating the email and URL and encrypting the username, email, and password.

        Args:
            db_safe: An instance of the database handler for the safe.
            master_password: The master password used for encryption.
            *args: A variable number of arguments containing the data to be saved.
        
        Returns:
            bool: True if the data was successfully saved, False otherwise.
        
        Raises:
            UrlError: If the provided URL is not valid.
            CategoryError: If the specified category does not exist in the database.

        """
        site_name, category, url, username, email, password, expiry_days, security_level = args
        if not validacion_link(url):
            raise UrlError("incorrect url")

        date = date_today()
        id_category = self.category._SQL_select(category)
        if not id_category:
            raise CategoryError("category does not exist")

        encrypt = []
        for k in (username, email, password):
            encrypt.append(CipherManager.Encypt_data(k, master_password))

        combined = [site_name, id_category[0][0], url, encrypt[0], encrypt[1], encrypt[2],date, expiry_days, security_level,
        ]

        self.safe._SQL_insert(*combined)

        return True


    def UpdateDataSafe(self, params: tuple, id: int | None = None, master_password: str = "") -> None:
        """Update existing data in the safe.

        Args:
            params: A tuple containing the data to be updated.
            id: Optional explicit id of the record to update. If not provided,
                it is resolved from the site name stored in params[0].
            master_password: The master password used for encryption.
        """
        username, password, expiry_days, security_level = params
        last_change = date_today()

        if id is None:
            id = self.GETSitename(username, master_password)[0][0]

        encrypt = [CipherManager.Encypt_data (k, master_password) for k in (username, password)]
        self.safe._SQL_update(
            encrypt[0], encrypt[1], last_change, expiry_days, security_level, id
        )

    def DeleteDataSafe(self, id: int) -> None:
        """Delete data from the safe based on the provided ID."""
        self.safe._SQL_delete(id)



    def __validatedata(self, data: list[tuple], identifier: str | int, error_msg: str | None = None) ->list[tuple]:
        """Validate if data has data; if not, raise a RowError."""
        if not data:
            msg = error_msg if error_msg else f"{identifier} does not exist or has no data"
            raise RowError(msg)
        return data


    def GetId(self, id: int, master_password: str = "") -> list[tuple]:
        """Get data from the safe based on the provided ID."""
        data = self.safe._SQL_filterById(id)
        new_data = self.controlls_decrypt(data, master_password)
        return self.__validatedata(new_data, id)


    def GETSitename(self, username: str, master_password: str = "") -> list[tuple]:
        """Get data from the safe based on the provided site name."""
        data = self.safe._SQL_filterBySitename(username)

        new_data = self.controlls_decrypt(data, master_password)
        return self.__validatedata(new_data, username)


    def SearchSitename(self, termino: str, master_password: str = "") -> list[tuple]:
        """Busca registros por coincidencia parcial (LIKE) en nombre de sitio o categoría."""
        data = self.safe._SQL_filterByLike(termino)
        if not data:
            raise RowError(f"sin coincidencias para '{termino}'")
        return self.controlls_decrypt(data, master_password)


    def GetEverything(self, master_password: str = "") -> list[tuple]:
        """Retrieve all data from the safe."""
        data = self.safe._SQL_select()
        if not data:
            raise DataBaseError("Database without registration.", 1070)

        new_data = self.controlls_decrypt(data, master_password)

        return new_data

    def GetdataCategory(self, category: str, master_password: str = "") -> list[tuple]:
        """Get data from the safe based on the provided category."""
        id = self.category._SQL_select(category)
        data = self.category._SQL_filterBycategory(id[0][0])
        new_data = self.controlls_decrypt(data, master_password)

        return self.__validatedata(new_data, category)


    def GetdataLastchange(self, year: int, month: int, master_password: str = "") -> list[tuple]:
        """Get data from the safe based on the provided year and month of last change."""
        data = self.safe._SQL_filterBylastChange(year, month)
        new_data = self.controlls_decrypt(data, master_password)

        return self.__validatedata(new_data, month)



    # ---
    def controlls_decrypt(self, data: list[tuple], master_password: str = "") -> list[list]:
        """Decrypts the data in the provided list of tuples.
        
        Args:
            data: A list of tuples containing the data to be decrypted.
            master_password: The master password used for decryption.
        
        Returns:
            A list of list with the decrypted data.
        """
        new_data = []
        for row in data:
            current_row = list(row[:3])

            # DESENCRIPTAMOS usando la password REAL, tolerando cambios de SALT
            for i in [3, 4]:
                decrypted_pass = CipherManager.Decrypt_data_tolerant(row[i], master_password)
                current_row.append(decrypted_pass if decrypted_pass is not None else "[no descifrado]")

            if len(row) > 5:
                current_row.append(row[5])

            new_data.append(current_row)
        return new_data
