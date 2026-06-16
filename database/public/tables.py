from utils.helpers import _execute_query
from database.db import get_connection

def db_create_table(table_number: int, capacity: int, status: str, price: int)-> None:
    conn = get_connection()
    cursor = conn.cursor()
    validate_query = """
    SELECT id FROM restaurant_tables 
    WHERE table_number = %s;
    """
    cursor.execute(validate_query, (table_number, ))
    table_id = cursor.fetchone()
    if table_id :
        raise Exception("El Usuario Ya existe!")
    query = """
    INSERT INTO restaurant_tables(table_number, capacity, status, price)
    VALUES (%s, %s, %s, %s);
    """
    cursor.execute(query, (table_number, capacity, status, price))
    conn.commit()
    cursor.close()
    conn.close()    

def db_get_table(table_numer: int)-> dict:
    pass

def db_table_exists(table_id: int) -> bool:
    """Devuelve un booleano indicando la existencia de un ID de mesa"""
    return bool(_execute_query('SELECT 1 FROM restaurant_tables WHERE id = %s', (table_id,)))

def db_check_table_capacity(table_id: int, amount: int) -> bool:
    """Recibe el ID de mesa y un número. 
    Si esa mesa existe y su capacidad no excede el número ingresado, devuelve True. Caso contrario False."""
    return bool(_execute_query('SELECT 1 FROM restaurant_tables WHERE id = %s AND capacity >= %s', (table_id, amount)))