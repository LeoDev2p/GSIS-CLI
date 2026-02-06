from core import config, Exceptions
from core.logger import get_logger
import sqlite3

log = get_logger("DATABASE")


def conectionDB(query, *args, select=False):
    """Ejecuta query SQL con prevención de SQL injection.
    
    Args:
        query: Query SQL con placeholders (?).
        *args: Parámetros de la query.
        select: True para SELECT, False para INSERT/UPDATE/DELETE.
    
    Returns:
        list si select=True, bool si exitoso.
    
    Raises:
        DataBaseError: Error de SQLite.
        InvalidParameterCountError: Parámetros incorrectos.
        RestrictionError: Violación de constraint.
    """
    try:
        with sqlite3.connect(config.ROOT_DB) as conn:
            conn.execute("PRAGMA foreign_keys = ON;")
            cursor = conn.cursor()

            cursor.execute(query, args)
            if select:
                return cursor.fetchall()

            conn.commit()

    except sqlite3.OperationalError as sql_O:
        log.error(f"Error en la base de datos {sql_O}")
        raise Exceptions.DataBaseError(str(sql_O))
    except sqlite3.ProgrammingError as sql_P:
        log.error(f"incorrect number of bindings supplied {sql_P}")
        raise Exceptions.InvalidParameterCountError(str(sql_P))
    except sqlite3.IntegrityError as sql_I:
        log.error(f" CHECK constraint failed {sql_I}")
        raise Exceptions.RestrictionError(str(sql_I))

    return True


class CreateTable:

    @staticmethod
    def createTableSafe():
        query = """
            CREATE TABLE IF NOT EXISTS safe (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site_name TEXT NOT NULL,
                id_category INTEGER NOT NULL,
                url TEXT,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                creation_date TEXT DEFAULT CURRENT_DATE,
                last_change TEXT,
                expiry_days INTEGER NOT NULL,
                security_level INTEGER CHECK (security_level > 0 AND security_level < 6),
                
                FOREIGN KEY (id_category) REFERENCES categorySafe (id) ON DELETE CASCADE		
            ) 
        """

        result = conectionDB(query)
        if result is None:
            log.info("Safe table successfully created")

    @staticmethod
    def creatTablecategory():
        query = """
            CREATE TABLE IF NOT EXISTS categorySafe (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """

        result = conectionDB(query)
        if result is None:
            log.info("Category table successfully created")
