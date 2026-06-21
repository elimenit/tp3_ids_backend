from database.helpers import _execute_query, _execute_update_query
from database.db import get_connection

def db_get_all_tables(limit: int, offset: int) -> list[dict]:
    return _execute_query('SELECT id, capacity, status FROM restaurant_tables ORDER BY id LIMIT %s OFFSET %s', (limit, offset))

def get_table_by_id(table_id: int) -> dict:
    return _execute_query('SELECT id, capacity, status FROM restaurant_tables WHERE id = %s', (table_id,))[0]

def db_create_table(capacity: int, status: str) -> None:
    ok = _execute_update_query('INSERT INTO restaurant_tables (capacity, status) VALUES (%s, %s)', (capacity, status))
    if not ok:
        raise Exception("No se pudo crear la mesa")

def db_table_exists(table_id: int) -> bool:
    """Devuelve un booleano indicando la existencia de un ID de mesa"""
    return bool(_execute_query('SELECT 1 FROM restaurant_tables WHERE id = %s', (table_id,)))

def db_check_table_capacity(table_id: int, amount: int) -> bool:
    """Recibe el ID de mesa y un número. 
    Si esa mesa existe y su capacidad no excede el número ingresado, devuelve True. Caso contrario False."""
    return bool(_execute_query('SELECT 1 FROM restaurant_tables WHERE id = %s AND capacity >= %s', (table_id, amount)))