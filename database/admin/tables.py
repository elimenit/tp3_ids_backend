from database.db import get_connection

def db_get_all_tables(limit: int, offset: int)-> list:
    """Obtiene una lista de mesas del administrador.

    Args:
        limit (int): limite de mesas.
        offset (int): desde donde comienza a buscar las mesas.

    Returns:
        list: lista de mesas.
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT id, table_number, capacity, status
    LIMIT %s OFFSET %s;
    """

    cursor.execute(query, (limit, offset))
    tables = cursor.fetchall()

    return [
        {
            "id": table[0],
            "number": table[1],
            "capacity": table[2],
            "status": table[3]
        }
        for table in tables
    ]

def db_update_table():
    pass

def db_delete_tables(tables_ids: list[int]):
    """Elimina una lista de tablas.

    Args:
        tables_ids (list[int]): lista de los ids de las tablas a eliminar.
    """
    pass

def db_delete_table(table_id: int)-> bool:
    """
    Elimina una mesa.
    """
    conn = get_connection()
    cursor = conn.cursor()

    query_validation = """
    SELECT id, table_number FROM restaurant_tables 
    WHERE id = %s;
    """
    cursor.execute(query_validation)
    table = cursor.fetchone()
    if not table:
        raise Exception("No se puede eliminar mesa no existente!")

    query = """
    DELETE FROM restaurant_tables
    WHERE id = %s;
    """
    cursor .execute(query, (table_id, ))
    return True
