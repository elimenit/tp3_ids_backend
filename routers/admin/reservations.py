"""Administracion de Reservaciones.
"""
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from utils.error import error_response
from services.public.reservations import (
    service_get_all_reservations,
    service_get_reservation,
    service_update_status,
)

adm_bp_reservations = Blueprint("admin_reservations", __name__)


@adm_bp_reservations.route(rule="/", methods=["GET"])
@jwt_required()
def show():
    """Obtiene todas las reservaciones.\n
    """
    reservas = service_get_all_reservations()

    if reservas is None:
        return error_response(
            "Error al obtener reservaciones",
            "Base de datos no disponible",
            500
        )

    return reservas


@adm_bp_reservations.route(rule="/<int:id>", methods=["GET"])
@jwt_required()
def get_reservation(id: int):
    """Obtiene una reservacion por ID.\n
    """
    reserva = service_get_reservation(id)

    if reserva is None:
        return error_response(
            f"id no existente: {id}",
            "Reservacion no encontrada",
            404
        )

    return reserva


@adm_bp_reservations.route(rule="/<int:id>/estado", methods=["POST"])
@jwt_required()
def update_status(id: int):
    """Actualiza el estado de una reservacion.\n
    """
    datos = request.get_json()

    if datos is None:
        return error_response(
            "Se esperaba JSON en el body",
            "Formato inválido",
            400
        )

    nuevo_estado = datos.get("status_reservation")

    if nuevo_estado is None:
        return error_response(
            "Falta status_reservation",
            "Campo obligatorio",
            400
        )

    ok, mensaje = service_update_status(id, nuevo_estado)

    if not ok:
        return error_response(mensaje, "", 400)

    return {"mensaje": mensaje}


@adm_bp_reservations.route(rule="/<int:id>", methods=["DELETE"])
@jwt_required()
def cancel(id: int):
    """Cancela una reservacion por ID.\n
    """
    ok, mensaje = service_update_status(id, "Cancelled")

    if not ok:
        return error_response(mensaje, "", 400)

    return {"mensaje": mensaje}