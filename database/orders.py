from database.db import get_connection

def db_get_orders(limit: int = 10, offset: int = 0):
    """Lista de Ordenes.\n
    Obtiene las primeras 10 ordenes.
    """
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM orders LIMIT %s AND OFFSET %s;"
    cursor.execute(query, (limit, offset))
    orders: list = cursor.fetchall()
    cursor.close()
    conn.close()
    return orders


def db_get_order(id: int):
    """Datos de una Orden.\n
    """
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = %s;"
    cursor.execute(query, (id, ))
    user = cursor.fetchone() 
    cursor.close()
    conn.close()
    return user

def db_create_order(customer_id: int)-> None:
    """Crea una orden.\n
    """
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM restaurant_tables WHERE ")
    table_id: int
    status_id: int

    query = "INSERT IGNORE orders (customer_id, table_id, status_id) VALUES (%s, %s, %s);"
    cursor.execute(query, (customer_id, table_id, status_id)) 
    conn.commit()
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
    """
    conn = get_connection()
    cursor = conn.cursor()
    query = "DELETE orders WHERE id = %s;"
    cursor.execute(query, (order_id, )) 
    cursor.close()
    conn.close()
    return None