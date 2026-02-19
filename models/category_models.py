"""Module responsible for handling database operations related to category management."""

from .database import conectionDB
from core.logger import get_logger

log = get_logger("DATABASE")


class QueryCatgory:
    """Class to manage SQL queries with SQL injection prevention related to category management in the database."""
    @staticmethod
    def _SQL_insert(id):
        query = """
            INSERT INTO categorySafe (name)
            VALUES (?)
        """

        result = conectionDB(query, id)
        if result:
            log.info("New category added successfully")

    # Traendo el ID de la categoria especifica
    @staticmethod
    def _SQL_select(category) -> list[tuple]:
        query = """
            SELECT id FROM categorysafe
            WHERE name = ?
        """
        return conectionDB(query, category, select=True)

    # actualizacion de la tabla categoria
    @staticmethod
    def _SQL_update(name, id):
        query = """
            UPDATE categorysafe
            SET name = ?
            WHERE id = ?
        """

        result = conectionDB(query, name, id)
        if result:
            log.info(f"Category {name} successfully updated")

    # eliminacion de elemento de la tabla categoria
    @staticmethod
    def _SQL_delete(id):

        query = """
            DELETE FROM categorySafe
            WHERE id = ?
        """

        result = conectionDB(query, id)
        if result:
            log.info(f"Category id: {id} deleted successfully")
