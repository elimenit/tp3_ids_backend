from database.helpers import _execute_query

def db_get_active_tables(limit: int, offset: int) -> tuple[list[dict], int]:
    tables = _execute_query('SELECT id, capacity FROM restaurant_tables WHERE status = "active" ORDER BY id LIMIT %s OFFSET %s', (limit, offset))
    count = _execute_query('SELECT COUNT(*) as total FROM restaurant_tables WHERE status = "active"')[0]['total']
    return tables, count