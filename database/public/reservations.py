from database.helpers import _execute_query, build_update_query, _execute_update_query

def db_get_reservation_by_id(reservation_id) -> dict | None:
    """
    Trae UNA reservacion por su ID.
    Devuelve None si no existe.
    """
    query = """
        SELECT
            r.id as id,
            r.reservation_datetime,
            r.status_reservation,
            u.email AS user_email,
            u.name AS user_name,
            r.table_id as table_number,
            r.people_amount as people_amount
        FROM reservations r
        JOIN users u ON r.user_id  = u.id
        WHERE r.id = %s
    """
    results = _execute_query(query, (reservation_id,))
    return results[0] if results else None


def db_get_reservations_by_user(user_id) -> list[dict]:
    """Trae todas las reservaciones de un usuario específico."""
    query = """
        SELECT
            r.id,
            r.reservation_datetime,
            r.status_reservation,
            r.table_id as table_number,
            r.people_amount
        FROM reservations r
        WHERE r.user_id = %s
        ORDER BY r.reservation_datetime DESC
    """
    return _execute_query(query, (user_id,))

def db_get_reservation_by_token(token) -> dict:
    """
    Trae una reservacion por su token unico.
    Uso: cuando el cliente hace click en cancelar desde el email.
    """
    query = "SELECT id, people_amount, table_id, status_reservation FROM reservations WHERE qr_token = %s"
    results = _execute_query(query, (token,))
    return results[0] if results else {}

def db_create_reservation(user_id: int, table_id: int, reservation_datetime: str, qr_token: str, people_amount: int) -> int | None:
    reservation_id = _execute_update_query("""
        INSERT INTO reservations
        (user_id, table_id, reservation_datetime, status_reservation, qr_token, people_amount)
        VALUES
        (%s, %s, %s, 'Pending', %s, %s)
        """, (user_id, table_id, reservation_datetime, qr_token, people_amount), return_lastrowid=True)
    return reservation_id

def db_update_reservation(id: int, updates: dict) -> None:
    ALLOWED_FIELDS = {'user_id', 'table_id', 'reservation_datetime', 'status_reservation', 'people_amount'}
    query, values = build_update_query('reservations', ALLOWED_FIELDS, updates)
    params = values + (id,)
    affected_rows = _execute_update_query(query, params)
    if not affected_rows:
        raise ValueError('No se han actualizado los campos. Es posible que los cambios propuestos sean idénticos a los valores actuales.')
    
def db_check_previous_amount(reservation_id: int, table_id: int) -> bool:
    """Aplicada antes de hacer un cambio de mesa. 
    En caso de que la cantidad de gente asignada previamente en la reserva exceda la capacidad de la nueva mesa, 
    devuelve False. Caso contrario True"""
    result = _execute_query("""
        SELECT 1
        FROM restaurant_tables
        WHERE id = %s
        AND capacity >= (SELECT people_amount FROM reservations WHERE id = %s)
    """, (table_id, reservation_id))
    return bool(result)

def db_check_new_amount(reservation_id: int, amount: int) -> bool:
    """Aplicada para cambio de cantidad de comensales"""
    query = """
        SELECT 1 FROM reservations r
        JOIN restaurant_tables rt ON r.table_id = rt.id
        WHERE r.id = %s AND rt.capacity >= %s
    """
    result = _execute_query(query, (reservation_id, amount))
    return bool(result)

def db_check_reservation_date(reservation_id: int) -> bool:
    """Revisa si una reserva es futura, en dicho caso devuelve True. Caso contrario False"""
    return bool(_execute_query('SELECT 1 FROM reservations WHERE id = %s AND reservation_datetime > NOW()', (reservation_id,)))

def db_reservation_not_available(fecha: str, table_id: int) -> bool:
    """Revisa si una mesa ya se encuentra reservada para ese día"""
    return bool(_execute_query("""
        SELECT 1 FROM reservations
        WHERE DATE(reservation_datetime) = %s 
          AND table_id = %s
          AND status_reservation NOT IN ('Cancelled')
        LIMIT 1
        """, (fecha, table_id)))

def db_cancel_reservation(reservation_id: int) -> int:
    return _execute_update_query('UPDATE reservations SET status_reservation = "Cancelled" WHERE id = %s', (reservation_id,))

def db_confirm_reservation(reservation_id: int) -> int:
    return _execute_update_query('UPDATE reservations SET status_reservation = "Arrived" WHERE id = %s', (reservation_id,))
