from database.db import get_connection

def db_get_reviews() -> list:
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT r.id, r.user_id, u.name, r.reservation_id, r.description, r.stars, r.created_at
    FROM reviews r
    JOIN users u ON r.user_id = u.id
    ORDER BY r.created_at DESC;
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    reviews = []
    for row in rows:
        reviews.append({
            "id": row[0],
            "user_id": row[1],
            "user_name": row[2],
            "reservation_id": row[3],
            "description": row[4],
            "stars": row[5],
            "created_at": str(row[6])
        })
    return reviews

def db_get_review(review_id: int) -> dict | None:
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT r.id, r.user_id, u.name, r.reservation_id, r.description, r.stars, r.created_at
    FROM reviews r
    JOIN users u ON r.user_id = u.id
    WHERE r.id = %s;
    """
    cursor.execute(query, (review_id,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "user_id": row[1],
        "user_name": row[2],
        "reservation_id": row[3],
        "description": row[4],
        "stars": row[5],
        "created_at": str(row[6])
    }

def db_create_review(user_id: int, reservation_id: int, description: str, stars: int) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO reviews (user_id, reservation_id, description, stars)
    VALUES (%s, %s, %s, %s);
    """
    cursor.execute(query, (user_id, reservation_id, description, stars))
    conn.commit()

    new_id = cursor.lastrowid
    cursor.close()
    conn.close()

    return new_id

def db_update_review(review_id: int, user_id: int, description: str, stars: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    # Solo puede editar su propia reseña (user_id debe coincidir)
    query = """
    UPDATE reviews
    SET description = %s, stars = %s
    WHERE id = %s AND user_id = %s;
    """
    cursor.execute(query, (description, stars, review_id, user_id))
    conn.commit()

    affected = cursor.rowcount
    cursor.close()
    conn.close()

    return affected > 0

def db_delete_review(review_id: int, user_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    # Solo puede borrar su propia reseña (user_id debe coincidir)
    query = """
    DELETE FROM reviews
    WHERE id = %s AND user_id = %s;
    """
    cursor.execute(query, (review_id, user_id))
    conn.commit()

    affected = cursor.rowcount
    cursor.close()
    conn.close()

    return affected > 0
