"""Módulo para manejar consultas SQL relacionadas con datos sensibles en la base de datos."""

from .database import conectionDB

class SafeSQL:
    """Class to manage SQL queries with SQL injection prevention related to sensitive data in the database."""

    def _SQL_insert(self, *args):
        query = """
            INSERT INTO safe (site_name, id_category, url, username, email, password, last_change, expiry_days, security_level)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        conectionDB(query, *args)

    # seleccionar todos los datos
    def _SQL_select(self) -> list[tuple]:
        query = """
            SELECT s.id, c.name, s.site_name, s.email, s.password, s.expiry_days FROM safe s
            JOIN categorySafe c ON s.id_category = c.id
        """

        return conectionDB(query, select=True)

    # actualizar datos sensibles
    def _SQL_update(self, *args):
        query = """
            UPDATE safe
            SET username = ?, password = ?, last_change = ?, expiry_days = ?, security_level = ?
            WHERE id = ?
        """

        conectionDB(query, *args)


    # eliminar datos sensible
    def _SQL_delete(self, id):
        query = """
            DELETE FROM safe
            WHERE id = ?
        """

        conectionDB(query, id)

    # filtrar por id
    def _SQL_filterById(self, id) -> list[tuple]:
        query = """
            SELECT s.id, c.name, s.site_name, s.email, s.password FROM categorySafe c
            JOIN safe s ON c.id = s.id_category
            WHERE s.id = ?
        """

        return conectionDB(query, id, select=True)

    # filtrar por nombre de sitio
    def _SQL_filterBySitename(self, site_name) -> list[tuple]:
        query = """
            SELECT s.id, c.name, s.site_name, s.email, s.password FROM categorySafe c
            JOIN safe s ON c.id = s.id_category
            WHERE s.site_name = ?
        """

        return conectionDB(query, site_name, select=True)

    # filtrar por coincidencia parcial (LIKE) en sitio o categoría
    def _SQL_filterByLike(self, termino: str) -> list[tuple]:
        query = """
            SELECT s.id, c.name, s.site_name, s.email, s.password, s.expiry_days
            FROM categorySafe c
            JOIN safe s ON c.id = s.id_category
            WHERE s.site_name LIKE ? ESCAPE '\\' OR c.name LIKE ?
            ORDER BY s.site_name
        """

        like = f"%{termino}%"
        return conectionDB(query, like, like, select=True)


    # filtrar por año y mes de modificacion
    def _SQL_filterBylastChange(self, year, month=0) -> list[tuple]:
        query = """
            SELECT s.id, c.name, s.site_name, s.email, s.password, s.expiry_days FROM safe s
            JOIN categorySafe c ON s.id_category = c.id
            WHERE CAST (strftime ('%Y', last_change) as INTEGER) = ? OR CAST (strftime ('%m', last_change) as INTEGER) = ?
        """

        return conectionDB(query, year, month, select=True)

