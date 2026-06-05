from database.db import get_connection

def db_get_menus(name: str, category: str, limit: int, offset: int)-> dict | None:
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    SELECT id, category, name, description, available
    FROM menus LIMIT %s OFFSET %s
    """
    menus = []
    if name is not None:
        query += ' WHERE name =%s'
    
        if category is not None:
            query += ' category =%s'
            
            cursor.execute(query, (limit, offset, name, category))
            menus_db = cursor.fetchall()
            menus = _package_menus(menus_db)
            cursor.close()
            conn.close()
            return menus
        else:
            cursor.execute(query, (limit, offset, name))
            menus_db = cursor.fetchall()
            menus = _package_menus(menus_db)
            cursor.close()
            conn.close()
            return menus
    
    elif category is not None:
        query += ' WHERE category = %s'
        cursor.execute(query, (limit, offset, category))
        menus_db = cursor.fetchall()
        menus = _package_menus(menus_db)
        cursor.close()
        conn.close()
        return menus
        
    cursor.execute(query, (limit, offset))
    menus_db = cursor.fetchall()
    menus = _package_menus(menus_db)

    cursor.close()
    conn.close()
    return menus

def db_create_menu(category: str, name: str, description: str, price: int, available: int)-> None:
    conn = get_connection()
    cursor = conn.cursor()
    validate_query = """
    SELECT id FROM menus WHERE name = %s AND category = %s;
    """
    cursor.execute(validate_query, (name, category))
    menu_id = cursor.fetchone()
    if menu_id:
        raise Exception("Ya existe el menu")
    
    query = """
    INSERT INTO menus (category, name, description, price, available)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (category, name, description, price, available))
    conn.commit()
    cursor.close()
    conn.close()

def _package_menus(menus_db)->list:
    """Empaquetado de los menus.\n
    Precio no se incluye.
    """
    menus = []
    for menu in menus_db:
        t: dict = {}
        t["id"] = menu[0]
        t["category"] = menu[1]
        t["name"] = menu[2]
        t["description"] = menu[3]
        t["available"] = menu[4]
        menus.append(t)
    return menus

def db_get_menu(menu_id: int)-> dict | None:
    """Obtiene un Menu.\n
    """
    conn =  get_connection()
    cursor = conn.cursor()

    query = """
    SELECT id, category, name, description, price, available
    FROM menus
    WHERE id = %s;
    """
    cursor.execute(query, (menu_id, ))
    menu_db = cursor.fetchone()
    
    if menu_db is None:
        cursor.close()
        conn.close()
        return None
    
    menu: dict = {}
    menu["id"] = menu_db[0]
    menu["category"] = menu_db[1]
    menu["name"] = menu_db[2]
    menu["description"] = menu_db[3]
    menu["price"] = menu_db[4]
    menu["available"] = menu_db[5]
    return menu