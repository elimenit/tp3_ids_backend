from database.helpers import _execute_query, build_update_query, _execute_update_query
from database.db import get_connection

def db_get_all_reservations(limit: int, offset: int) -> list[dict]:
    """
    Trae todas las reservaciones con datos del cliente y la mesa.
    Usa JOIN porque esa informacion vive en tablas distintas.
    """
    query = """
        SELECT
            r.id as id,
            DATE_FORMAT(r.reservation_datetime, '%Y-%m-%d') as fecha,
            HOUR(r.reservation_datetime) as hora,
            r.status_reservation,
            u.email AS user_email,
            r.table_id as table_number,
            r.people_amount as people_amount
        FROM reservations r
        JOIN users u ON r.user_id  = u.id
        ORDER BY r.reservation_datetime DESC
        LIMIT %s OFFSET %s
    """
    return _execute_query(query, (limit, offset))