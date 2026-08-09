"""Module responsible for handling database operations related to category management."""

from .database import conectionDB


class CategorySQL:
    """Class to manage SQL queries with SQL injection prevention related to category management in the database."""
    @staticmethod
    def _SQL_insert(id):
        query = """
            INSERT INTO categorySafe (name)
            VALUES (?)
        """

        conectionDB(query, id)

    # Traendo el ID de la categoria especifica
    @staticmethod
    def _SQL_select(category) -> list[tuple]:
        query = """
            SELECT id FROM categorysafe
            WHERE name = ?
        """
        return conectionDB(query, category, select=True)

    # Listar todas las categorías existentes
    @staticmethod
    def _SQL_getAll() -> list[tuple]:
        query = """
            SELECT id, name FROM categorysafe
            ORDER BY name
        """
        return conectionDB(query, select=True)

    # actualizacion de la tabla categoria
    @staticmethod
    def _SQL_update(name, id):
        query = """
            UPDATE categorysafe
            SET name = ?
            WHERE id = ?
        """

        conectionDB(query, name, id)

    # eliminacion de elemento de la tabla categoria
    @staticmethod
    def _SQL_delete(id):

        query = """
            DELETE FROM categorySafe
            WHERE id = ?
        """

        conectionDB(query, id)

    # filtrar por id de categoria
    def _SQL_filterBycategory(self, id_category) -> list[tuple]:
        query = """
            SELECT s.id, c.name, s.site_name, s.email, s.password, s.expiry_days from categorySafe c
            JOIN safe s ON c.id = s.id_category
            WHERE c.id = ?
        """
    
        return conectionDB(query, id_category, select=True)
