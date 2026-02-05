
from models.database import CreateTable
from models.category_models import QueryCatgory
from core.Exceptions import DataBaseError, CategoryError, UrlError, RowError
from utils.view_utils import date_today
from utils.validation import valitacion_email, validacion_link, validate_date
import pdb

def Createtables ():
    CreateTable.createTableSafe ()
    CreateTable.creatTablecategory ()

    return True

def Savecategory (category):
    QueryCatgory._SQL_insert (category)


@valitacion_email
def SaveSafe (db_safe, *args): # posible errror por *args en decorador
    site_name, category, url, username, email, password, expiry_days, security_level = args
    if not validacion_link (url):
        raise UrlError ("incorrect url")
    
    id_category = QueryCatgory._SQL_select (category)
    if not id_category:
        raise CategoryError ("category does not exist")
    
    date = date_today ()

    db_safe._SQL_insert (site_name, id_category, url, username, email, password, date, expiry_days, security_level)
    
    return True

def UpdateDataSafe (db_safe, params):
    username, password, expiry_days, security_level = params
    last_change = date_today ()
    id = GETSitename (db_safe, username)[0][0]

    db_safe._SQL_update (username, password, last_change, expiry_days, security_level, id)

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

    return __validatedata (data, username)


def GetEverything (db_safe):
    data = db_safe._SQL_select ()
    if not data:
        raise DataBaseError ("Base de datos sin registro.", 1070)
    
    return data

def GetdataCategory (db_safe, category):
    id = QueryCatgory._SQL_select (category)
    data = db_safe._SQL_filterBycategory (id)
    return __validatedata (data, category)

def GetdataLastchange (db_safe, year, month):
    data = db_safe._SQL_filterBylastChange (year, month)
    return __validatedata (data, month)


def GetdataRange_Lastchange (db_safe, date1, date2):
    if all (filter (validate_date, (date1, date2))):
        normalize = [x.replace ("/", "-") for x in (date1, date2)]

        data = db_safe._SQL_filterRangeLastChange (normalize[0], normalize[1])
        return __validatedata (data, date1)


