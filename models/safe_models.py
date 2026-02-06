"""Módulo para manejar consultas SQL relacionadas con datos sensibles en la base de datos."""

from .database import conectionDB
from core.logger import get_logger

log = get_logger('DATABASE')


class QuerySafe:
    # Insertando datos sensibles
    def _SQL_insert(self, *args):
        query = """
            INSERT INTO safe (site_name, id_category, url, username, email, password, last_change, expiry_days, security_level)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        result = conectionDB(query, *args)
        if result:
            log.info("Data successfully inserted into the Safe table")

    # seleccionar todos los datos
    def _SQL_select(self):
        query = """
            SELECT s.id, c.name, s.site_name, s.email, s.expiry_days FROM safe s
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

        result = conectionDB(query, *args)
        if result:
            log.info(f"Data successfully updated for id: {args[0]}")

    # eliminar datos sensible
    def _SQL_delete(self, id):
        query = """
            DELETE FROM safe
            WHERE id = ?
        """

        result = conectionDB(query, id)
        if result:
            log.info(f"Deleted id: {id}, from the database")

    # filtrar por id
    def _SQL_filterById(self, id):
        query = """
            SELECT s.id, c.name, s.site_name, s.email FROM categorySafe c
            JOIN safe s ON c.id = s.id_category
            WHERE s.id = ?
        """

        return conectionDB(query, id, select=True)

    # filtrar por nombre de sitio
    def _SQL_filterBySitename(self, site_name):
        query = """
            SELECT s.id, c.name, s.site_name, s.email FROM categorySafe c
            JOIN safe s ON c.id = s.id_category
            WHERE s.site_name = ?
        """

        return conectionDB(query, site_name, select=True)

    # filtrar por id de categoria
    def _SQL_filterBycategory(self, id_category):
        query = """
            SELECT s.id, c.name, s.site_name, s.email, s.expiry_days from categorySafe c
            JOIN safe s ON c.id = s.id_category
            WHERE c.id = ?
        """

        return conectionDB(query, id_category, select=True)

    # filtrar por año y mes de modificacion
    def _SQL_filterBylastChange(self, year, month=0):
        query = """
            SELECT s.id, c.name, s.site_name, s.email, s.expiry_days FROM safe s
            JOIN categorySafe c ON s.id_category = c.id
            WHERE CAST (strftime ('%Y', last_change) as INTEGER) = ? OR CAST (strftime ('%m', last_change) as INTEGER) = ?
        """

        return conectionDB(query, year, month, select=True)

    # filtrar por rango de fechas 'YYYY-MM-DD'
    def _SQL_filterRangeLastChange(self, date1: str = "YYYY-mm-dd", date2: str = "YYYY-mm-dd") -> list:
        """Filtra los registros por un rango de fechas de último cambio.

        Args:
            date1 (str): Fecha de inicio del rango (YYYY-MM-DD).
            date2 (str): Fecha de fin del rango (YYYY-MM-DD).

        Returns:
            list: Una lista con los registros encontrados en la base de datos.
        """
        query = """
            SELECT s.id, c.name, s.site_name, s.email, s.expiry_days FROM safe s
            JOIN categorySafe c ON s.id_category = c.id
            WHERE last_change BETWEEN ? AND ?
        """

        return conectionDB(query, date1, date2, select=True)

