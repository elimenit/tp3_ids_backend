from database.db import get_connection

def db_get_reviews(limit: int = 10, offset: int = 0) -> list:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT r.id, r.user_id, u.name AS user_name, r.reservation_id, r.description, r.stars, r.created_at
    FROM reviews r
    JOIN users u ON r.user_id = u.id
    ORDER BY r.created_at DESC
    LIMIT %s OFFSET %s;
    """
    cursor.execute(query, (limit, offset))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    for row in rows:
        row["created_at"] = str(row["created_at"])

    return rows

def db_get_review(review_id: int) -> dict | None:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT r.id, r.user_id, u.name AS user_name, r.reservation_id, r.description, r.stars, r.created_at
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

    row["created_at"] = str(row["created_at"])
    return row

def db_get_review_by_reservation(user_id: int, reservation_id: int) -> dict | None:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT id FROM reviews
    WHERE user_id = %s AND reservation_id = %s;
    """
    cursor.execute(query, (user_id, reservation_id))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return row

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
