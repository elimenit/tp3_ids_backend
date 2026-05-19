from database.db import get_connection

def db_get_orders(user_id: int, limit: int = 10, offset: int = 0)-> list:
    """
    Lista de órdenes con sus items.
    """
    
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT o.id, o.table_id, o.order_datetime, so.name, o.total
    FROM orders AS o 
    INNER JOIN status_orders AS so 
    ON o.status_id = so.id
    WHERE o.user_id = %s
    LIMIT %s OFFSET %s
    """

    cursor.execute(query, (user_id, limit, offset))
    orders = cursor.fetchall()

    lista_orders: list = []
    for order in orders:
        
        order_id = order[0]

        model_order: dict = {
            "id": order_id,
            "user_id": user_id,
            "date": order[2],
            "status": order[3],
            "total": order[4],
            "tables": [],
            "menus":[]
        }
        query_menus = """
            SELECT id, menu_item_id, quantity
            FROM order_menus WHERE order_id = %s
        """
        cursor.execute(query_menus, (order_id, ))
        menus = cursor.fetchall()
        
        list_menus: list = []
        for menu in menus:
            menu_id = menu[0]
            model_menu = {
                "id": menu_id,
                "menu": [],
                "quantity": menu[2]
            }

            menu_item_id = menu[1]
            query_item_menu = """
                SELECT mc.name, mi.name, mi.description, mi.price, mi.available 
                FROM menu_items AS mi 
                INNER JOIN menu_categories AS mc
                ON mc.id = mi.category_id
                WHERE mi.id = %s
            """
            cursor.execute(query_item_menu, (menu_item_id, ))
            item_menus = cursor.fetchall()
            menu_items = []

            for item_menu in item_menus:
                items = {
                    "id": menu_item_id,
                    "category": item_menu[0],
                    "name": item_menu[1],
                    "description": item_menu[2],
                    "price": item_menu[3],
                    "available": item_menu[4]
                }
                menu_items.append(items)
            model_menu["menu"] = menu_items
            list_menus.append(menu_items)
    
        model_order["menus"] = list_menus
        
        table_id = order[1]
        query_tables = """
        SELECT rt.id, rt.table_number, rt.capacity, srt.name, rt.price
        FROM restaurant_tables AS rt
        INNER JOIN status_restaurant_tables AS srt
        ON rt.status_table_id = srt.id
        WHERE rt.id = %s
        """
        cursor.execute(query_tables, (table_id, ))
        tables = cursor.fetchall()
        
        list_tables = []
        for table in tables:
            model_table: dict = {
                "id": table[0],
                "number_table": table[1],
                "capacity": table[2],
                "status": table[3],
                "price": table[4]
            }
            list_tables.append(model_table)
        model_order["tables"] = list_tables
        
        lista_orders.append(model_order)

    cursor.close()
    conn.close()
    
    return lista_orders

def db_get_order(user_id: int, order_id: int):
    """Datos de una Orden.\n
    """
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    SELECT o.id, o.table_id, o.order_datetime, so.name, o.total
    FROM orders AS o 
    INNER JOIN status_orders AS so 
    ON o.status_id = so.id
    WHERE o.user_id = %s AND o.id = %s
    """

    cursor.execute(query, (user_id, order_id))
    order = cursor.fetchone()

    model_order: dict = {
        "id": order_id,
        "user_id": user_id,
        "date": order[2],
        "status": order[3],
        "total": order[4],
        "tables": [],
        "menus":[]
    }

    query_menus = """
        SELECT id, menu_item_id, quantity
        FROM order_menus WHERE order_id = %s 
    """
    cursor.execute(query_menus, (order_id, ))
    menus = cursor.fetchall()
    
    list_menus: list = []
    for menu in menus:
        menu_id = menu[0]
        model_menu = {
            "id": menu_id,
            "menu": [],
            "quantity": menu[2]
        }
        menu_item_id = menu[1]
        query_item_menu = """
            SELECT mc.name, mi.name, mi.description, mi.price, mi.available 
            FROM menu_items AS mi 
            INNER JOIN menu_categories AS mc
            ON mc.id = mi.category_id
            WHERE mi.id = %s
        """
        cursor.execute(query_item_menu, (menu_item_id, ))
        item_menus = cursor.fetchall()
        menu_items = []
        for item_menu in item_menus:
            items = {
                "id": menu_item_id,
                "category": item_menu[0],
                "name": item_menu[1],
                "description": item_menu[2],
                "price": item_menu[3],
                "available": item_menu[4]
            }
            menu_items.append(items)
        model_menu["menu"] = menu_items
        list_menus.append(menu_items)

    model_order["menus"] = list_menus
    
    table_id = order[1]
    query_tables = """
    SELECT rt.id, rt.table_number, rt.capacity, srt.name, rt.price
    FROM restaurant_tables AS rt
    INNER JOIN status_restaurant_tables AS srt
    ON rt.status_table_id = srt.id
    WHERE rt.id = %s
    """
    cursor.execute(query_tables, (table_id, ))
    tables = cursor.fetchall()
    
    list_tables = []
    for table in tables:
        model_table: dict = {
            "id": table[0],
            "number_table": table[1],
            "capacity": table[2],
            "status": table[3],
            "price": table[4]
        }
        list_tables.append(model_table)
    model_order["tables"] = list_tables
    return model_order

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