
from database.db import get_connection


def db_get_all_reservations():
    """
    Trae todas las reservaciones con datos del cliente y la mesa.
    Usa JOIN porque esa informacion vive en tablas distintas.
    """
    try:
        conn   = get_connection()
        cursor = conn.cursor(dictionary=True)
        # dictionary=True hace que cada fila sea un diccionario
        # fila['user_name'] en lugar de fila[0]
        try:
            cursor.execute("""
                SELECT
                    r.id,
                    r.reservation_datetime,
                    r.status_reservation,
                    u.name  AS user_name,
                    u.email AS user_email,
                    t.table_number,
                    t.capacity
                FROM reservations r
                JOIN users             u ON r.user_id  = u.id
                JOIN restaurant_tables t ON r.table_id = t.id
                ORDER BY r.reservation_datetime DESC
            """)
            reservations = cursor.fetchall()
            return reservations
        finally:
            # finally se ejecuta SIEMPRE haya error o no
            # garantiza que la conexion siempre se cierra
            cursor.close()
            conn.close()

    except Exception as e:
        print(f"Error en db_get_all_reservations: {e}")
        return None


def db_get_reservation_by_id(reservation_id):
    """
    Trae UNA reservacion por su ID.
    Uso: admin viendo el detalle, o justo despues de crear una reservacion.
    Devuelve None si no existe.
    """
    try:
        conn   = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT
                    r.id,
                    r.reservation_datetime,
                    r.status_reservation,
                    r.qr_token,
                    u.name  AS user_name,
                    u.email AS user_email,
                    t.table_number,
                    t.capacity
                FROM reservations r
                JOIN users             u ON r.user_id  = u.id
                JOIN restaurant_tables t ON r.table_id = t.id
                WHERE r.id = %s
            """, (reservation_id,))
            # (reservation_id,) con coma al final es una tupla de un elemento
            # sin la coma seria solo un parentesis, no una tupla

            reservation = cursor.fetchone()
            # fetchone() devuelve solo la primera fila
            # si no existe devuelve None
            return reservation
        finally:
            cursor.close()
            conn.close()

    except Exception as e:
        print(f"Error en db_get_reservation_by_id: {e}")
        return None


def db_get_reservation_by_token(token):
    """
    Trae una reservacion por su token unico.
    Uso: cuando el cliente hace click en cancelar desde el email.

    Por que no usar el ID para cancelar:
    Los IDs son numeros consecutivos (1,2,3...) cualquiera podria
    adivinarlos y cancelar reservaciones ajenas.
    El token es aleatorio e imposible de adivinar.
    """
    try:
        conn   = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT id, status_reservation FROM reservations WHERE qr_token = %s",
                (token,)
            )
            reservation = cursor.fetchone()
            return reservation
        finally:
            cursor.close()
            conn.close()

    except Exception as e:
        print(f"Error en db_get_reservation_by_token: {e}")
        return None


# def db_get_all_tables():
#     """
#     Trae todas las mesas SIN filtro de disponibilidad.
#     Se usa cuando el usuario todavia no eligio fecha y hora.
#     """
#     try:
#         conn   = get_connection()
#         cursor = conn.cursor(dictionary=True)
#         try:
#             cursor.execute("""
#                 SELECT id, table_number, capacity, price, status
#                 FROM restaurant_tables
#                 ORDER BY table_number
#             """)
#             tables = cursor.fetchall()
#             return tables
#         finally:
#             cursor.close()
#             conn.close()

#     except Exception as e:
#         print(f"Error en db_get_all_tables: {e}")
#         return None


def db_get_all_tables():
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, table_number, capacity, price,
                   status,
                   status AS estado
            FROM restaurant_tables
            ORDER BY table_number
        """)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def db_get_tables_availability(fecha, hora):
    """
    Trae todas las mesas con su estado para una fecha y hora.
    Usa DOS queries simples en lugar de un query complejo.

    Query 1: todas las mesas
    Query 2: que mesas estan ocupadas en ese horario
    Python:  calcula el estado de cada mesa combinando los dos
    """
    try:
        conn   = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # ── QUERY 1: todas las mesas ──────────────────────────
            cursor.execute("""
                SELECT id, table_number, capacity, price, status
                FROM restaurant_tables
                ORDER BY table_number
            """)
            all_tables = cursor.fetchall()
            # Resultado: lista de diccionarios, uno por mesa
            # [
            #   {'id':1, 'table_number':1, 'capacity':4, 'status':'available'},
            #   {'id':2, 'table_number':2, 'capacity':4, 'status':'available'},
            # ]

            # ── QUERY 2: mesas con reservacion activa ese horario ─
            cursor.execute("""
                SELECT table_id
                FROM reservations
                WHERE DATE(reservation_datetime) = %s
                AND HOUR(reservation_datetime)   = %s
                AND status_reservation IN ('Pending', 'Confirmed')
            """, (fecha, hora))

            rows = cursor.fetchall()
            # rows es una lista de diccionarios:
            # [{'table_id': 1}, {'table_id': 3}]

            # Armamos una lista con solo los IDs de las mesas ocupadas
            # forma simple con for loop
            occupied_ids = []
            for row in rows:
                occupied_ids.append(row['table_id'])
            # occupied_ids queda asi: [1, 3]

            # ── PYTHON: calcular estado de cada mesa ──────────────
            for table in all_tables:

                if table['id'] in occupied_ids:
                    # Su ID esta en la lista de ocupadas
                    # tiene una reservacion activa en ese horario
                    table['estado'] = 'reserved'

                elif table['status'] == 'occupied':
                    # El admin la marco como ocupada en tiempo real
                    table['estado'] = 'occupied'

                else:
                    # No esta en ninguna condicion, esta libre
                    table['estado'] = 'available'

            # Ahora all_tables tiene el campo 'estado' agregado:
            # [
            #   {'id':1, ..., 'estado': 'reserved'},
            #   {'id':2, ..., 'estado': 'available'},
            # ]
            return all_tables

        finally:
            cursor.close()
            conn.close()

    except Exception as e:
        print(f"Error en db_get_tables_availability: {e}")
        return None


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
            # commit() confirma el INSERT en la base de datos
            # sin commit() el registro no se guarda

            new_id = cursor.lastrowid
            # lastrowid es el ID que MySQL asigno al registro nuevo
            return new_id

        finally:
            cursor.close()
            conn.close()

    except Exception as e:
        print(f"Error en db_create_reservation: {e}")
        return None


def db_update_reservation_status(reservation_id, new_status):
    """
    Cambia el estado de una reservacion.
    Devuelve True si cambio algo, False si no existia.
    """
    try:
        conn   = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE reservations
                SET status_reservation = %s
                WHERE id = %s
            """, (new_status, reservation_id))

            conn.commit()

            # rowcount dice cuantas filas se modificaron
            # si es 0 la reservacion no existia
            if cursor.rowcount > 0:
                return True
            else:
                return False

        finally:
            cursor.close()
            conn.close()

    except Exception as e:
        print(f"Error en db_update_reservation_status: {e}")
        return False