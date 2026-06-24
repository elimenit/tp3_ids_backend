from database.helpers import _execute_query
from database.db import get_connection

def db_list_menus(limit: int = 10, offset: int = 0) -> list:
    return _execute_query('''
    SELECT image_url, id, name, category, description, price, available
    FROM menus ORDER BY category, name LIMIT %s OFFSET %s''', (limit, offset)
    )

def db_get_menu(menu_id: int) -> dict | None:
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT id, category, name, description, price, available, image_url
    FROM menus
    WHERE id = %s;
    """
    cursor.execute(query, (menu_id,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "category": row[1],
        "name": row[2],
        "description": row[3],
        "price": float(row[4]),
        "available": bool(row[5]),
        "image_url": row[6]
    }

def db_create_menu(category: str, name: str, description: str, price: float, image_url: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO menus (category, name, description, price, available, image_url)
    VALUES (%s, %s, %s, %s, TRUE, %s);
    """
    cursor.execute(query, (category, name, description, price, image_url))
    conn.commit()

    new_id = cursor.lastrowid
    cursor.close()
    conn.close()

    return new_id

def db_update_menu(menu_id: int, category: str, name: str, description: str, price: float, available: bool, image_url: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE menus
    SET category = %s, name = %s, description = %s, price = %s, available = %s, image_url = %s
    WHERE id = %s;
    """
    cursor.execute(query, (category, name, description, price, available, image_url, menu_id))
    conn.commit()

    affected = cursor.rowcount
    cursor.close()
    conn.close()

    return affected > 0

def db_delete_menu(menu_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    query = "DELETE FROM menus WHERE id = %s;"
    cursor.execute(query, (menu_id,))
    conn.commit()

    affected = cursor.rowcount
    cursor.close()
    conn.close()

    return affected > 0
