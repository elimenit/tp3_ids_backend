from database.db import get_connection

def db_get_orders(user_id: int, limit: int = 10, offset: int = 0)-> list:
    conn = get_connection()
    cursor = conn.cursor()
    
    query_orders = """
    SELECT id, status, total, fecha,  created_at
    FROM orders WHERE user_id = %s
    LIMIT %s OFFSET %s;
    """
    cursor.execute(query_orders, (user_id, limit, offset))
    lista_orders = cursor.fetchall()

    orders: dict = {
        "user_id": user_id,
        "orders": []
    }
    for order in lista_orders:
        model_order: dict = {}
        model_order["id"] = order[0]
        model_order["status"] = order[1]
        model_order["total"] = order[2]
        model_order["fecha"] = order[3]
        model_order["created_at"] = order[4]

        orders["orders"].append(model_order)

    cursor.close()
    conn.close()
    
    return orders

def db_get_order(user_id: int, order_id: int)-> dict:
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    SELECT status, total, fecha, created_at
    FROM orders 
    WHERE user_id = %s AND id = %s;
    """
    order: dict = {
        "user_id": user_id,
        "id": order_id
    }

    cursor.execute(query, (user_id, order_id))
    order_not_pretty = cursor.fetchone()

    order["status"] = order_not_pretty[0]
    order["total"] = order_not_pretty[1]
    order["fecha"] = order_not_pretty[2]
    order["created_at"] = order_not_pretty[3]

    cursor.close()
    conn.close()
    return order

def db_create_order(user_id: int, tables_menus: dict[int, list[list[int, int]]])-> None:
    """Crea una orden.\n
    tables_menus: diccionario donde la clave es el table_number y valor una lista de los menus y la cantidad.\n
    tables_menus = dict[table_id, list[list[menu_id, quantity]]]
    """
    conn = get_connection()
    cursor = conn.cursor()
    total = 100 # Harcodeado (Autotegenerado)
    # Validacion
    # Falta 

    # Caso Feliz
    query_table_menu = """
    INSERT INTO tables_menus (order_id, table_id, menu_id, quantity)
    VALUES (%s, %s, %s, %s);
    """
    query_order = """
    INSERT INTO orders (user_id, status, total)
    VALUES (%s, %s, %s);
    """
    cursor.execute(query_order, (user_id, 'pending', total))
    order_id = cursor.lastrowid
    
    for table_id in tables_menus:    
        for menu_id, quantity in tables_menus[table_id]:
            table_id = int(table_id)

            cursor.execute(query_table_menu, (order_id, table_id, menu_id, quantity))
            conn.commit()

    cursor.close()
    conn.close()
    return order_id

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

def db_delete_order(user_id: int, order_id: int)-> None:
    """Elimina una Orden.\n
    Pero el usuario no deberia poder eliminar una orden sino solo cambiar su estado aexe
    """
    conn = get_connection()
    cursor = conn.cursor()
    query = """ 
    DELETE FROM orders 
    WHERE id = %s AND user_id = %s;
    """
    cursor.execute(query, (order_id, user_id))

    cursor.close()
    conn.close()
    return None