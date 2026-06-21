import secrets

from database.public.users import db_get_user
from database.public.tables import db_check_table_capacity, db_table_exists
from database.public.reservations import (
    db_get_all_reservations,
    db_get_reservation_by_id,
    db_get_reservations_by_user,
    db_get_reservation_by_token,
    db_get_all_tables,
    db_get_tables_availability,
    db_create_reservation,
    db_update_reservation,
    db_check_previous_amount,
    db_check_new_amount,
    db_check_reservation_date
)

from utils.error import error_response
from utils.qr_generator import generar_qr
from utils.email_sender import enviar_email_reserva
from utils.validators import validar_limit_offset, is_future_date
from utils.helpers import _count_rows

from flask import Response

VALID_STATUSES = ['Pending', 'Confirmed', 'Cancelled', 'Arrived']

def validate_table_capacity(table_id: int | None, amount: int | None, reservation_id: int) -> bool:
    """
    Valida las 3 posibilidades de cambio:
    - Cambio de mesa y cambio de gente simultáneo.
    - Cambio de mesa sola (mantiene comensales actuales).
    - Cambio de gente sola (mantiene mesa actual).
    """
    if table_id is not None and amount is not None:
        return db_check_table_capacity(table_id, amount)
    if table_id is not None:
        return db_check_previous_amount(reservation_id, table_id)
    if amount is not None:
        return db_check_new_amount(reservation_id, amount)
    return True

def service_get_all_reservations(limit: int, offset: int) -> tuple[list[dict], int]:
    """Devuelve todas las reservaciones y la cantidad total de registros. Uso: panel admin."""
    if not validar_limit_offset(limit, offset):
        raise ValueError("Error en la selección de números para el paginado.")
    return db_get_all_reservations(limit, offset), _count_rows('reservations')

def update_reservation(reservation_id: int, updates: dict) -> tuple[Response | str, int]:
    """
    Espera un ID de reserva y un diccionario de forma {'<nombre_de_columna>': <valor>}. 
    Esto a excepción de las fechas que son ingresadas como 'fecha' y 'hora'.

    Valida:
    - Que hayan cambios
    - Que la reserva a modificar es futura
    - Si se ingresó una fecha y la misma es futura (no es posible actualizar reservas pasadas)
    - Formato de hora
    - Existencia de mesa
    - Capacidad (más detalle en la función validate_table_capacity)
    - Existencia de usuario
    - Estado de reserva ingresado 
    """
    if not updates:
        return error_response("Error en la actualización", "No hay campos para actualizar.", 400)
    print(updates)

    if not db_check_reservation_date(reservation_id):
        return error_response('Error', 'La reserva a modificar es pasada o no existe. Debe editar reservas futuras.', 400)

    res_date = updates.get('fecha')
    hour = updates.get('hora')
    if res_date and hour:
        try:
            hour = int(hour)
        except TypeError:
            return error_response('Error en la hora', 'Se debe ingresar una hora numérica', 400)
        if not is_future_date(res_date):
            return error_response('Error en la fecha', 'Debe ingresar una fecha futura.', 400)
        for clave in ['fecha', 'hora']:
            updates.pop(clave, None)
        updates['reservation_datetime'] = f"{res_date} {hour:02d}:00:00"

    table_id = updates.get('table_id')
    amount = updates.get('people_amount')
    if table_id:
        print('chequeando mesa... \n')
        if not db_table_exists(table_id):
            return error_response('Mesa no encontrada', f'La mesa de número [{table_id}] no ha sido encontrada.', 404)

    if table_id or amount:
        if not validate_table_capacity(table_id, amount, reservation_id):
            return error_response('Capacidad excedida', 'La cantidad de comensales supera la capacidad de la mesa', 400)

    user_email = updates.get('user_email')
    if user_email:
        user = db_get_user(email=user_email)
        if not user:
            return error_response('Error en el email', f'No se ha encontrado usuario con el email: {user_email}', 404)
        updates.pop('user_email', None)
        updates['user_id'] = user['id']

    status = updates.get('status_reservation')
    if status: 
        if status not in VALID_STATUSES:
            return error_response('Error en el estado', 'Se ha ingresado un estado no válido.', 400)
    
    processed_updates = {k: v for k, v in updates.items() if v is not None}
    print(processed_updates)
    db_update_reservation(reservation_id, processed_updates)
    return '', 204

def service_get_my_reservations(user_id):
    """Devuelve solo las reservaciones del usuario logueado."""
    return db_get_reservations_by_user(user_id)


def service_get_reservation(reservation_id):
    """
    Devuelve una reservacion por ID.
    Si no existe devuelve None y el router maneja el error 404.
    """
    return db_get_reservation_by_id(reservation_id)


def service_get_tables(fecha, hora):
    """
    Devuelve las mesas con su estado de disponibilidad.
    Si llegan fecha y hora: filtra por ese horario.
    Si no llegan: devuelve todas sin filtro.
    Siempre devuelve dos valores: (resultado, error)
    """

    if fecha and hora is not None:
        tables = db_get_tables_availability(fecha, int(hora))
    else:
        tables = db_get_all_tables()

    if tables is None:
        return None, "Error al obtener las mesas"

    return tables, None


def service_create_reservation(datos, user_id):
    """
    Crea una reservacion completa paso a paso.

    Pasos:
    1. Valida que llegaron los campos necesarios
    2. Trae todas las mesas con su disponibilidad
    3. Busca la mesa que eligio el usuario
    4. Verifica que la mesa este libre
    5. Genera un token unico y seguro
    6. Guarda la reservacion en la BD
    7. Genera la imagen del QR
    8. Envia el email con el QR

    Devuelve (reserva_id, None) si todo salio bien
    Devuelve (None, diccionario_con_error) si algo fallo
    """

    campos_necesarios = ['table_id', 'fecha', 'hora']

    for campo in campos_necesarios:
        if not datos.get(campo):
            return None, {"tipo": "error", "mensaje": f"Falta el campo: {campo}"}

    fecha   = datos.get('fecha')
    hora    = datos.get('hora')
    mesa_id = datos.get('table_id')

    tables, error = service_get_tables(fecha, hora)

    if error:
        return None, {"tipo": "error", "mensaje": error}

    mesa_elegida = None

    for mesa in tables:
        if str(mesa['id']) == str(mesa_id):
            mesa_elegida = mesa
            break

    if mesa_elegida is None:
        return None, {"tipo": "error", "mensaje": "La mesa no existe"}

    if mesa_elegida['estado'] != 'available':

        mesas_libres = []
        for mesa in tables:
            if mesa['estado'] == 'available':
                mesas_libres.append(mesa)

        return None, {
            "tipo":         "mesa_no_disponible",
            "mensaje":      "Esa mesa no esta disponible para ese horario.",
            "mesas_libres": mesas_libres
        }

    qr_token = secrets.token_urlsafe(16)
    reservation_datetime = f"{fecha} {int(hora):02d}:00:00"

    reserva_id = db_create_reservation(
        user_id,
        mesa_id,
        reservation_datetime,
        qr_token
    )

    if reserva_id is None:
        return None, {"tipo": "error", "mensaje": "Error al guardar la reservacion"}

    qr_path = generar_qr(reserva_id, qr_token)

    try:
        reserva = db_get_reservation_by_id(reserva_id)
        enviar_email_reserva(
            destinatario = reserva['user_email'],
            nombre       = reserva['user_name'],
            reserva_id   = reserva_id,
            fecha        = reservation_datetime,
            qr_path      = qr_path,
            qr_token     = qr_token
        )
    except Exception as error_email:
        print(f"Advertencia: el email no se envio. Motivo: {error_email}")

    return reserva_id, None


def service_cancel_by_token(token):
    """
    Cancela una reservacion usando el token del QR.
    El cliente llega aca desde el link del email.
    Devuelve (True, mensaje) o (False, mensaje_de_error)
    """

    # Buscar la reservacion por token
    reserva = db_get_reservation_by_token(token)

    if reserva is None:
        return False, "Token invalido o reservacion no encontrada"

    # Guardar el estado actual para verificar si se puede cancelar
    estado_actual = reserva['status_reservation']

    if estado_actual == 'Cancelled':
        return False, "Esta reservacion ya fue cancelada"

    if estado_actual == 'Arrived':
        return False, "No se puede cancelar una reservacion ya completada"

    # Cambiar el estado a Cancelled
    ok = db_update_reservation_status(reserva['id'], 'Cancelled')

    if ok:
        return True, "Reservacion cancelada exitosamente"
    else:
        return False, "Error al cancelar la reservacion"