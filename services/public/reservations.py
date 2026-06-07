# =============================================================================
# services/public/reservations.py
# Capa de servicios para reservaciones.
# Unica responsabilidad: logica de negocio y validaciones.
# No sabe nada de HTTP. No toca la BD directamente.
# =============================================================================

import secrets

from database.public.reservations import (
    db_get_all_reservations,
    db_get_reservation_by_id,
    db_get_reservations_by_user,
    db_get_reservation_by_token,
    db_get_all_tables,
    db_get_tables_availability,
    db_create_reservation,
    db_update_reservation_status,
)
from utils.qr_generator import generar_qr
from utils.email_sender import enviar_email_reserva

# Estados validos segun el ENUM del schema
# Solo estos cuatro valores son aceptados
VALID_STATUSES = ['Pending', 'Confirmed', 'Cancelled', 'Arrived']


def service_get_all_reservations():
    """Devuelve todas las reservaciones. Uso: panel admin."""
    return db_get_all_reservations()


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
        # Convertimos hora a entero porque del formulario llega como string
        # '20' (string) → 20 (entero) para que coincida con HOUR() en MySQL
        tables = db_get_tables_availability(fecha, int(hora))
    else:
        # Sin fecha y hora traemos todas sin filtro
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

    # ── Paso 1: validar campos obligatorios ───────────────────────
    campos_necesarios = ['table_id', 'fecha', 'hora']

    for campo in campos_necesarios:
        if not datos.get(campo):
            # datos.get(campo) devuelve None si el campo no existe
            return None, {"tipo": "error", "mensaje": f"Falta el campo: {campo}"}

    fecha   = datos.get('fecha')
    hora    = datos.get('hora')
    mesa_id = datos.get('table_id')

    # ── Paso 2: traer todas las mesas con disponibilidad ──────────
    tables, error = service_get_tables(fecha, hora)

    if error:
        return None, {"tipo": "error", "mensaje": error}

    # ── Paso 3: buscar la mesa que eligio el usuario ──────────────
    # Recorremos la lista buscando la mesa con el ID correcto
    mesa_elegida = None

    for mesa in tables:
        if str(mesa['id']) == str(mesa_id):
            # Convertimos los dos a string para comparar
            # mesa_id puede llegar como '3' (string del formulario)
            # mesa['id'] puede ser 3 (entero de la BD)
            mesa_elegida = mesa
            break
        # break sale del for cuando encontro la mesa

    # Si no encontro ninguna mesa con ese ID
    if mesa_elegida is None:
        return None, {"tipo": "error", "mensaje": "La mesa no existe"}

    # ── Paso 4: verificar que la mesa este disponible ─────────────
    if mesa_elegida['estado'] != 'available':

        # Armar lista de mesas libres para mostrarselas al usuario
        mesas_libres = []
        for mesa in tables:
            if mesa['estado'] == 'available':
                mesas_libres.append(mesa)

        return None, {
            "tipo":         "mesa_no_disponible",
            "mensaje":      "Esa mesa no esta disponible para ese horario.",
            "mesas_libres": mesas_libres
        }

    # ── Paso 5: generar token unico ───────────────────────────────
    # secrets.token_urlsafe(16) genera algo como 'xK9mP2nQr7vL4wZj'
    # Es imposible de adivinar, por eso es seguro para el link de cancelar
    qr_token = secrets.token_urlsafe(16)

    # Armamos el datetime completo para guardar en la BD
    # :02d formatea el numero con dos digitos (9 → 09, 20 → 20)
    reservation_datetime = f"{fecha} {int(hora):02d}:00:00"

    # ── Paso 6: guardar en la BD ──────────────────────────────────
    reserva_id = db_create_reservation(
        user_id,
        mesa_id,
        reservation_datetime,
        qr_token
    )

    if reserva_id is None:
        return None, {"tipo": "error", "mensaje": "Error al guardar la reservacion"}

    # ── Paso 7: generar QR ────────────────────────────────────────
    qr_path = generar_qr(reserva_id, qr_token)

    # ── Paso 8: enviar email ──────────────────────────────────────
    # try/except porque si el email falla la reservacion igual existe
    # no queremos deshacer todo por un problema de email
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
        # Mostramos el error pero no frenamos el flujo
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


def service_update_status(reservation_id, new_status):
    """
    Cambia el estado desde el panel admin.
    Valida que el nuevo estado sea uno de los permitidos por el ENUM.
    """

    # Verificar que el estado pedido existe en nuestra lista
    if new_status not in VALID_STATUSES:
        return False, f"Estado invalido. Debe ser uno de: {VALID_STATUSES}"

    ok = db_update_reservation_status(reservation_id, new_status)

    if ok:
        return True, "Estado actualizado correctamente"
    else:
        return False, "Reservacion no encontrada"