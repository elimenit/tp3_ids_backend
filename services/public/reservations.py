import secrets

from werkzeug import Response

from database.admin.tables import db_check_table_capacity, db_table_exists
from database.public.reservations import (
    db_get_reservation_by_id,
    db_get_reservations_by_user,
    db_get_reservation_by_token,
    db_create_reservation,
    db_check_previous_amount,
    db_check_new_amount,
    db_reservation_not_available,
    db_cancel_reservation,
    db_confirm_reservation
)

from utils.error import error_response
from utils.qr_generator import generar_qr
from utils.email_sender import enviar_email_reserva

def validate_table_capacity(table_id: int | None, amount: int | None, reservation_id: int) -> bool:
    """
    Valida las 3 posibilidades de cambio:
    - Cambio de mesa y cambio de gente simultáneo.
    - Cambio de mesa sola (mantiene comensales actuales).
    - Cambio de gente sola (mantiene mesa actual).
    
    Tiene que tener 2 de los 3 parámetros
    """
    if table_id is not None and amount is not None:
        return db_check_table_capacity(table_id, amount)
    if table_id is not None:
        return db_check_previous_amount(reservation_id, table_id)
    if amount is not None:
        return db_check_new_amount(reservation_id, amount)
    return True

def service_get_my_reservations(user_id):
    """Devuelve solo las reservaciones del usuario logueado."""
    return db_get_reservations_by_user(user_id)

def service_get_reservation(reservation_id):
    """
    Devuelve una reservacion por ID.
    Si no existe devuelve None y el router maneja el error 404.
    """
    return db_get_reservation_by_id(reservation_id)

def service_create_reservation(data: dict, user_id: int) -> tuple[None | Response, int]:
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
    campos_necesarios = ['table_id', 'fecha', 'hora', 'people_amount']
    fecha = data.get('fecha')
    hora = data.get('hora')
    table_id = data.get('table_id')
    people_amount = data.get('people_amount')

    if not all(campo in data for campo in campos_necesarios):
        return error_response('Error en los datos', f'Se esperaban los campos {campos_necesarios}', 400)

    if not db_table_exists(table_id): # type: ignore
        return error_response('Error en los datos', 'La mesa seleccionada no existe', 404)

    qr_token = secrets.token_urlsafe(16)    
    reservation_datetime = f"{fecha} {int(hora):02d}:00:00" # type: ignore

    if db_reservation_not_available(fecha, table_id): # type: ignore
        return error_response('Error', f'La mesa seleccionada ya está ocupada para el día {fecha}.', 409)

    reserva_id = db_create_reservation(user_id, table_id, reservation_datetime, qr_token, people_amount) # type: ignore
    if not reserva_id:
        return error_response('Error al crear la reservacion', 'No se pudo guardar la reservacion en la base de datos', 500)

    reserva = db_get_reservation_by_id(reserva_id)
    if not reserva:
        return error_response('Error al crear la reservacion', 'No se pudo recuperar la reservacion creada', 500)
    
    qr_path = generar_qr(reserva_id, qr_token)

    try:
        enviar_email_reserva(
            destinatario = reserva['user_email'],
            nombre = reserva['user_name'],
            reserva_id = reserva_id,
            fecha = reservation_datetime,
            qr_path = qr_path,
            qr_token = qr_token
        )
    except Exception as error_email:
        rows = db_cancel_reservation(reserva_id)
        if not rows:
            return error_response('Error', 'No se ha podido cancelar la reserva.', 500)
        return error_response('Error', f"Advertencia: el email no se envio. Motivo: {error_email}", 500)

    return None, reserva_id


def service_cancel_by_token(token):
    """
    Cancela una reservacion usando el token del QR.
    El cliente llega aca desde el link del email.
    Devuelve (True, mensaje) o (False, mensaje_de_error)
    """
    reserva = db_get_reservation_by_token(token)

    if reserva is None:
        return False, "Token invalido o reservacion no encontrada"

    estado_actual = reserva['status_reservation']

    if estado_actual == 'Cancelled':
        return False, "Esta reservacion ya fue cancelada"

    if estado_actual == 'Arrived':
        return False, "No se puede cancelar una reservacion ya completada"

    ok = db_cancel_reservation(reserva['id'])

    if ok:
        return True, "Reservacion cancelada exitosamente"
    else:
        return False, "Error al cancelar la reservacion"
    
def qr_confirm_reservation(qr_token: str) -> tuple[dict | Response, int]:
    reservation = db_get_reservation_by_token(qr_token)
    if reservation.get('status_reservation') != 'Arrived':
        rows = db_confirm_reservation(reservation.get('id')) # type: ignore
        if not rows:
            return error_response('Error durante la confirmación.', 'Ha ocurrido un error durante la confirmación de la reserva.', 500)
        else:
            reservation['status_reservation'] = 'Arrived'
            return reservation, 200
    return error_response('Advertencia', 'No se ha confirmado la reserva, dado que ya se encuentra confirmada', 409)