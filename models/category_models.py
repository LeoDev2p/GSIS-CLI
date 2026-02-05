from .database import conectionDB
from core.logger import get_logger

log = get_logger ("DATABASE")

class QueryCatgory:
    # insertar categoria
    @staticmethod
    def _SQL_insert (id):
        query = """
            INSERT INTO categorySafe (name)
            VALUES (?)
        """

        result = conectionDB (query, id)
        if result is None:
            log.info ("Nueva categoria agregada cone éxito")

    # Traendo el ID de la categoria especifica
    @staticmethod
    def _SQL_select (category):
        query = """
            SELECT id FROM categorysafe
            WHERE name = ?
        """
        return conectionDB (query, category, select=True)[0][0]

    # actualizacion de la tabla categoria
    @staticmethod
    def _SQL_update (name, id):
        query = """
            UPDATE categorysafe
            SET name = ?
            WHERE id = ?
        """

        result = conectionDB (query, name, id)
        if result:
            log.info (f"categoria {name} actualziada con éxito")
    
    # eliminacion de elemento de la tabla categoria
    @staticmethod
    def _SQL_delete (self, id):
        query = """
            DELETE FROM categorySafe
            WHERE id = ?
        """

        result = conectionDB (query, id)
        if result:
            log.info (f"Categoria id: {id} elimina con éxito")