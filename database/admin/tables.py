from database.helpers import _execute_query, _execute_update_query, build_update_query, _count_rows

def db_get_all_tables(limit: int, offset: int) -> tuple[list[dict], int]:
    tables = _execute_query('SELECT id, capacity, status FROM restaurant_tables ORDER BY id LIMIT %s OFFSET %s', (limit, offset))
    count = _count_rows('restaurant_tables')
    return tables, count

def db_deactivate_table(table_id: int) -> int:
    return _execute_update_query('UPDATE restaurant_tables SET status = "inactive" WHERE id = %s', (table_id,))

def db_update_table(table_id: int, updates: dict) -> int:
    """Actualiza los datos de una mesa. Recibe un diccionario con los campos a actualizar."""
    allowed_fields = {'capacity', 'status'}
    query, values = build_update_query('restaurant_tables', allowed_fields, updates)
    return _execute_update_query(query, values + (table_id,))

def get_table_by_id(table_id: int) -> dict:
    return _execute_query('SELECT id, capacity, status FROM restaurant_tables WHERE id = %s', (table_id,))[0]

def db_create_table(capacity: int) -> None:
    ok = _execute_update_query('INSERT INTO restaurant_tables (capacity, status) VALUES (%s, "active")', (capacity,))
    if not ok:
        raise Exception("No se pudo crear la mesa")

def db_table_exists(table_id: int) -> bool:
    """Devuelve un booleano indicando la existencia de un ID de mesa"""
    return bool(_execute_query('SELECT 1 FROM restaurant_tables WHERE id = %s', (table_id,)))

def db_check_table_capacity(table_id: int, amount: int) -> bool:
    """Recibe el ID de mesa y un número. 
    Si esa mesa existe y su capacidad no excede el número ingresado, devuelve True. Caso contrario False."""
    return bool(_execute_query('SELECT 1 FROM restaurant_tables WHERE id = %s AND capacity >= %s', (table_id, amount)))