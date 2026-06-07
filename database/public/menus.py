from database.db import get_connection

def db_get_menus(category: str = None, name: str = None, limit: int = 10, offset: int = 0) -> list:
    conn = get_connection()
    cursor = conn.cursor()

    conditions = ["available = TRUE"]
    params = []

    if category is not None:
        conditions.append("category = %s")
        params.append(category)
    if name is not None:
        conditions.append("name LIKE %s")
        params.append(f"%{name}%")

    where = " AND ".join(conditions)
    params.extend([limit, offset])

    query = f"""
    SELECT id, category, name, description, price, image_url
    FROM menus
    WHERE {where}
    ORDER BY category, name
    LIMIT %s OFFSET %s;
    """
    cursor.execute(query, params)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    menus = []
    for row in rows:
        menus.append({
            "id": row[0],
            "category": row[1],
            "name": row[2],
            "description": row[3],
            "price": float(row[4]),
            "image_url": row[5]
        })
    return menus

def db_get_menu(menu_id: int) -> dict | None:
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT id, category, name, description, price, image_url
    FROM menus
    WHERE id = %s AND available = TRUE;
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
        "image_url": row[5]
    }
