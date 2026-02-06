
from models.database import CreateTable
from models.category_models import QueryCatgory
from core.Exceptions import DataBaseError, CategoryError, UrlError, RowError
from utils.utils import date_today
from utils.validation import valitacion_email, validacion_link, validate_date
from security.encryption import CipherManager
import pdb

def Createtables ():
    CreateTable.createTableSafe ()
    CreateTable.creatTablecategory ()

    return True

def Savecategory (category):
    QueryCatgory._SQL_insert (category)


@valitacion_email
def SaveSafe (db_safe, *args): 
    site_name, category, url, username, email, password, expiry_days, security_level = args
    if not validacion_link (url):
        raise UrlError ("incorrect url")
    
    date = date_today ()
    id_category = QueryCatgory._SQL_select (category)[0][0]
    if not id_category:
        raise CategoryError ("category does not exist")

    encrypt = []
    for k in (username, email, password):
        encrypt.append (CipherManager.Encypt_data (k))
    
    combined = [site_name, id_category, url, encrypt[0], encrypt[1], encrypt[2], date, expiry_days, security_level]

    db_safe._SQL_insert (*combined)
    
    return True

def UpdateDataSafe (db_safe, params):
    username, password, expiry_days, security_level = params
    last_change = date_today ()
    id = GETSitename (db_safe, username)[0][0]

    encrypt = [CipherManager.Decrypt_data (k)  for k in (username, password)]
    db_safe._SQL_update (encrypt[0], encrypt[1], last_change, expiry_days, security_level, id)

def DeleteDataSafe (db_safe, id):
    db_safe._SQL_delete (id)

# validamos si hay datos  o no
def __validatedata (data, identifier, error_msg = None):
    if not data:
        msg = error_msg if error_msg else f"{identifier} does not exist or has no data"
        raise RowError(msg)
    return data

def GetId (db_safe, id):
    # pdb.set_trace ()
    data = db_safe._SQL_filterById (id)
    return __validatedata (data, id)

def GETSitename (db_safe, username):
    data = db_safe._SQL_filterBySitename (username)

    new_data = controlls_decrypt (data)

    return __validatedata (new_data, username)


def GetEverything (db_safe):
    data = db_safe._SQL_select ()
    if not data:
        raise DataBaseError ("Database without registration.", 1070)
    
    new_data = controlls_decrypt (data)
    
    return new_data

def GetdataCategory (db_safe, category):
    id = QueryCatgory._SQL_select (category)
    print (f"[DEBUG] {id}")
    data = db_safe._SQL_filterBycategory (id[0][0])
    new_data = controlls_decrypt (data)
    return __validatedata (new_data, category)

def GetdataLastchange (db_safe, year, month):
    data = db_safe._SQL_filterBylastChange (year, month)
    new_data = controlls_decrypt (data)
    return __validatedata (new_data, month)


def GetdataRange_Lastchange (db_safe, date1, date2):
    if all (filter (validate_date, (date1, date2))):
        normalize = [x.replace ("/", "-") for x in (date1, date2)]

        data = db_safe._SQL_filterRangeLastChange (normalize[0], normalize[1])
        new_data = controlls_decrypt (data)
        return __validatedata (new_data, date1)

# ---
def controlls_decrypt (data):
    new_data = []
    for row in range (len(data)):
        new_data.append ([r for r in data[row][:3]])
        new_data[row].append (CipherManager.Decrypt_data (data[row][3]))

        if len (data[row]) > 4:
            new_data[row].append (data[row][4])
    return new_data