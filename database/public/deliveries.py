from database.db import get_connection

def db_get_deliveries(user_id: int)-> list | None:
    conn = get_connection()
    cursor = conn.cursor()
    # Validaciones

    # Caso Feliz
    query = """
    SELECT id, address, delivery_datetime
    FROM deliveries 
    WHERE user_id = %s;
    """
    cursor.execute(query, (user_id, ))
    
    deliveries_db = cursor.fetchall()
    if deliveries_db is None:
        cursor.close()
        conn.close()
        return None
    print(deliveries_db)
    deliveries = []
    for delivery in deliveries_db:
        delivery_model: dict = {}
        delivery_model["id"] = delivery[0]
        delivery_model["addres"] = delivery[1]
        delivery_model["datetime"] = delivery[2]
        deliveries.append(delivery_model)

    return deliveries

def db_get_delivery(user_id: int, delivery_id: int)-> dict | None:
    conn = get_connection()
    cursor = conn.cursor()
    # Validaciones

    # Caso Feliz
    query = """
    SELECT address, delivery_datetime, status
    FROM deliveries
    WHERE user_id = %s AND id = %s;
    """
    cursor.execute(query, (user_id, delivery_id))
    info_delivery = cursor.fetchone()
    if info_delivery is None:
        return None

    delivery = {
        "id": delivery_id,
        "user_id": user_id,
        "address": info_delivery[0],
        "date": info_delivery[1],
        "status": info_delivery[2],
        "menus": []
    }
    query = """
    SELECT menu_id, quantity, created_at, qr_code
    FROM deliveries_menus
    WHERE delivery_id = %s;
    """
    cursor.execute(query, (delivery_id, ))
    info_menus = cursor.fetchall()

    for menu in info_menus:
        t: dict = {}
        t["id"] = menu[0]
        t["quantity"] = menu[1]
        t["created_at"] = menu[2]
        t["qr_code"] = menu[3]
        delivery["menus"].append(t)

    return delivery

def db_create_delivery(user_id: int, list_menus_quantity: list[list[int, int]], addres: str, date: str)-> int:
    """ Creacion de un menu.\n
    ids_menus_quantity: lista de una lista que contiene consecutivamente el menu_id y la cantidad.\n
    """
    conn = get_connection()
    cursor = conn.cursor()
    # Validaciones

    # Caso Feliz
    query = """
    INSERT INTO deliveries (user_id, address, status)
    VALUES (%s, %s, %s);
    """
    cursor.execute(query, (user_id, addres, 'pending'))
    conn.commit()

    delivery_id = cursor.lastrowid

    query = """
    INSERT INTO deliveries_menus (
    delivery_id, menu_id, quantity)
    VALUES (%s, %s, %s);
    """
    for (menu_id, quantity) in list_menus_quantity:
        cursor.execute(query, (delivery_id, menu_id, quantity))
        conn.commit()

    return delivery_id

def db_cancelled_delivery(user_id: int, delivery_id: int)-> None:
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE deliveries SET status = 'cancelled'
    WHERE id = %s AND user_id = %s;
    """
    cursor.execute(query, (delivery_id, user_id))
    conn.commit()
    
    cursor.close()
    conn.close()