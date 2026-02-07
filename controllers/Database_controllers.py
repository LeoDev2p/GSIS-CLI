"""Module responsible for handling database operations related to the safe and category management."""

from typing import Any

from models.database import CreateTable
from models.category_models import QueryCatgory
from core.Exceptions import DataBaseError, CategoryError, UrlError, RowError
from utils.utils import date_today
from utils.validation import valitacion_email, validacion_link, validate_date
from security.encryption import CipherManager


def Createtables():
    """Create the necessary tables for the application if they do not exist."""
    CreateTable.createTableSafe()
    CreateTable.creatTablecategory()

    return True


def Savecategory(category):
    """Save a new category to the database."""
    QueryCatgory._SQL_insert(category)

def delete_category(category):
    """Delete a category from the database based on the provided name."""
    id_category = QueryCatgory._SQL_select(category)[0][0]

    if id_category:
        QueryCatgory._SQL_delete(id_category)
    else:
        raise CategoryError("category does not exist")


@valitacion_email
def SaveSafe(db_safe: object, *args: Any, master_password: str = ""):
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
    site_name, category, url, username, email, password, expiry_days, security_level = (args)
    if not validacion_link(url):
        raise UrlError("incorrect url")

    date = date_today()
    id_category = QueryCatgory._SQL_select(category)
    if not id_category:
        raise CategoryError("category does not exist")

    encrypt = []
    for k in (username, email, password):
        encrypt.append(CipherManager.Encypt_data(k, master_password))

    combined = [site_name, id_category[0][0], url, encrypt[0], encrypt[1], encrypt[2],
        date, expiry_days, security_level,
    ]

    db_safe._SQL_insert(*combined)

    return True


def UpdateDataSafe(db_safe: object, params: tuple, master_password: str = "") -> None:
    """Update existing data in the safe after validating the email and URL and encrypting the username and password.
    
    Args:
        db_safe: An instance of the database handler for the safe.
        master_password: The master password used for encryption.
        params: A tuple containing the data to be updated.

    Returns:
        bool: True if the data was successfully updated, False otherwise.
    """
    username, password, expiry_days, security_level = params
    last_change = date_today()
    id = GETSitename(db_safe, username, master_password)[0][0]

    encrypt = [CipherManager.Encypt_data (k, master_password) for k in (username, password)]
    db_safe._SQL_update(
        encrypt[0], encrypt[1], last_change, expiry_days, security_level, id
    )


def DeleteDataSafe(db_safe: object, id: int) -> None:
    """Delete data from the safe based on the provided ID."""
    db_safe._SQL_delete(id)


# validamos si hay datos  o no
def __validatedata(data: list[tuple], identifier: str | int, error_msg: str | None = None) ->list[tuple]:
    """Validate if data has data; if not, raise a RowError."""
    if not data:
        msg = error_msg if error_msg else f"{identifier} does not exist or has no data"
        raise RowError(msg)
    return data


def GetId(db_safe: object, id: int, master_password: str = "") -> list[tuple]:
    """Get data from the safe based on the provided ID."""
    data = db_safe._SQL_filterById(id)
    new_data = controlls_decrypt(data, master_password)
    return __validatedata(new_data, id)


def GETSitename(db_safe: object, username: str, master_password: str = "") -> list[tuple]:
    """Get data from the safe based on the provided site name."""
    data = db_safe._SQL_filterBySitename(username)

    new_data = controlls_decrypt(data, master_password)
    return __validatedata(new_data, username)


def GetEverything(db_safe: object, master_password: str = "") -> list[tuple]:
    """Retrieve all data from the safe."""
    data = db_safe._SQL_select()
    if not data:
        raise DataBaseError("Database without registration.", 1070)

    new_data = controlls_decrypt(data, master_password)

    return new_data

def GetdataCategory(db_safe: object, category: str, master_password: str = "") -> list[tuple]:
    """Get data from the safe based on the provided category."""
    id = QueryCatgory._SQL_select(category)
    data = db_safe._SQL_filterBycategory(id[0][0])
    new_data = controlls_decrypt(data, master_password)

    return __validatedata(new_data, category)


def GetdataLastchange(db_safe: object, year: int, month: int, master_password: str = "") -> list[tuple]:
    """Get data from the safe based on the provided year and month of last change."""
    data = db_safe._SQL_filterBylastChange(year, month)
    new_data = controlls_decrypt(data, master_password)

    return __validatedata(new_data, month)


def GetdataRange_Lastchange(db_safe: object, date1: int, date2: int, master_password: str = "") -> list[tuple]:
    """Get data from the safe based on the provided date range of last change."""
    if all(filter(validate_date, (date1, date2))):
        normalize = [x.replace("/", "-") for x in (date1, date2)]

        data = db_safe._SQL_filterRangeLastChange(normalize[0], normalize[1])
        new_data = controlls_decrypt(data, master_password)

        return __validatedata(new_data, date1)


# ---
def controlls_decrypt(data: list[tuple], master_password: str = "") -> list[list]:
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
        
        # DESENCRIPTAMOS usando la password REAL
        for i in [3,4]:
            decrypted_pass = CipherManager.Decrypt_data(row[i], master_password)
            current_row.append(decrypted_pass)

        if len(row) > 5:
            current_row.append(row[5])
            
        new_data.append(current_row)
    return new_data
