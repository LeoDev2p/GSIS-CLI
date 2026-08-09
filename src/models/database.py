"""Module responsible for handling database connections and table creations for the application."""

from src.core import config, Exceptions
from src.core.logger import get_logger
import sqlite3

log = get_logger("DATABASE")


def conectionDB(query, *args, select=False):
    """Executes SQL query with SQL injection prevention.

    Args:
        query: SQL query with placeholders (?).
        *args: Query parameters.
        select: True for SELECT, False for INSERT/UPDATE/DELETE.

    Returns:
        list if select=True, bool if successful.

    Raises:
        DataBaseError: SQLite error.
        InvalidParameterCountError: Invalid parameters.
        RestrictionError: Constraint violation.

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



class CreateTable:
    """Create necessary tables for the aplication if they do not exist."""
    @staticmethod
    def createTableSafe():
        """Craate the 'safe' table in the database if it does not exist."""
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
        return conectionDB(query)

    @staticmethod
    def creatTablecategory():
        """Create the 'categorySafe' table in the database if it does not exist."""
        query = """
            CREATE TABLE IF NOT EXISTS categorySafe (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """
        return conectionDB(query)
