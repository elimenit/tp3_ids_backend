from database.db import get_connection

def db_get_orders(user_id: int, limit: int = 10, offset: int = 0)-> list:
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.close()
    conn.close()
    
    return lista_orders

def db_get_order(user_id: int, order_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.close()
    conn.close()
    return None

def db_create_order(user_id: int, table_numbers_id: list[int], capacity: int, quantity: int)-> None:
    """Crea una orden.\n
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.close()
    conn.close()
    return None

def db_update_order(id: int)-> None:
    """Actualiza una Orden.\n
    """
    conn = get_connection()
    cursor = conn.cursor()
    query = ""
    cursor.execute(query) 
    cursor.close()
    conn.close()
    return None

def db_delete_order(order_id: int)-> None:
    """Elimina una Orden.\n
    Pero el usuario no deberia poder eliminar una orden sino solo cambiar su estado aexe
    """
    return None