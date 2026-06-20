from utils.helpers import _execute_query, build_update_query, _execute_update_query
from database.db import get_connection

def db_get_all_reservations(limit: int, offset: int) -> list[dict]:
    """
    Trae todas las reservaciones con datos del cliente y la mesa.
    Usa JOIN porque esa informacion vive en tablas distintas.
    """
    query = """
        SELECT
            r.id as id,
            DATE_FORMAT(r.reservation_datetime, '%Y-%m-%d') as fecha,
            HOUR(r.reservation_datetime) as hora,
            r.status_reservation,
            u.email AS user_email,
            r.table_id as table_number,
            r.people_amount as people_amount
        FROM reservations r
        JOIN users u ON r.user_id  = u.id
        ORDER BY r.reservation_datetime DESC
        LIMIT %s OFFSET %s
    """
    return _execute_query(query, (limit, offset))


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
        JOIN restaurant_tables t ON r.table_id = t.id
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
            t.table_number,
            t.capacity
        FROM reservations r
        JOIN restaurant_tables t ON r.table_id = t.id
        WHERE r.user_id = %s
        ORDER BY r.reservation_datetime DESC
    """
    return _execute_query(query, (user_id,))


def db_get_reservation_by_token(token) -> dict | None:
    """
    Trae una reservacion por su token unico.
    Uso: cuando el cliente hace click en cancelar desde el email.
    """
    query = "SELECT id, status_reservation FROM reservations WHERE qr_token = %s"
    results = _execute_query(query, (token,))
    return results[0] if results else None


def db_get_all_tables() -> list[dict]:
    """Trae todas las mesas SIN filtro de disponibilidad."""
    query = """
        SELECT id, table_number, capacity,
               status,
               status AS estado
        FROM restaurant_tables
        ORDER BY table_number
    """
    return _execute_query(query)


def db_get_tables_availability(fecha, hora) -> list[dict]:
    """
    Trae todas las mesas con su estado para una fecha y hora.
    1. Todas las mesas
    2. Mesas ocupadas en ese horario
    """
    all_tables = _execute_query("""
        SELECT id, table_number, capacity, status
        FROM restaurant_tables
        ORDER BY table_number
    """)

    occupied_rows = _execute_query("""
        SELECT table_id
        FROM reservations
        WHERE DATE(reservation_datetime) = %s
        AND HOUR(reservation_datetime)  = %s
        AND status_reservation IN ('Pending', 'Confirmed')
    """, (fecha, hora))

    occupied_ids = [row['table_id'] for row in occupied_rows]

    for table in all_tables:
        if table['id'] in occupied_ids:
            table['estado'] = 'reserved'
        elif table['status'] == 'occupied':
            table['estado'] = 'occupied'
        else:
            table['estado'] = 'available'

    return all_tables


def db_create_reservation(user_id, table_id, reservation_datetime, qr_token):
    """
    Inserta una reservacion nueva en la base de datos.
    Estado inicial siempre es 'Pending'.
    Devuelve el ID del registro creado.
    """
    try:
        conn   = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO reservations
                    (user_id, table_id, reservation_datetime,
                     status_reservation, qr_token)
                VALUES (%s, %s, %s, 'Pending', %s)
            """, (user_id, table_id, reservation_datetime, qr_token))

            conn.commit()

            new_id = cursor.lastrowid
            return new_id

        finally:
            cursor.close()
            conn.close()

    except Exception as e:
        print(f"Error en db_create_reservation: {e}")
        return None

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