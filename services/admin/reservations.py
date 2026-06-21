from utils.error import error_response
from utils.validators import is_future_date, validar_limit_offset
from database.helpers import _count_rows
from database.admin.reservations import db_get_all_reservations
from database.public.reservations import db_check_reservation_date, db_update_reservation
from database.admin.tables import db_table_exists
from services.public.reservations import validate_table_capacity
from database.public.users import db_get_user

from werkzeug import Response

VALID_STATUSES = ['Pending', 'Confirmed', 'Cancelled', 'Arrived']

def service_get_all_reservations(limit: int, offset: int) -> tuple[list[dict], int]:
    """Devuelve todas las reservaciones y la cantidad total de registros"""
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
    db_update_reservation(reservation_id, processed_updates)
    return '', 204