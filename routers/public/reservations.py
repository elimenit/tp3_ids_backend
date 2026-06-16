from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from services.public.reservations import (
    service_get_my_reservations,
    service_get_reservation,
    service_get_tables,
    service_create_reservation,
    service_cancel_by_token,
    update_reservation
)

public_bp_reservations = Blueprint("public_reservations", __name__)

@public_bp_reservations.route("/<int:id>", methods=["GET"])
def get_one(id):
    """
    Trae una reservacion por ID.
    GET /public/reservations/5
    """
    reserva = service_get_reservation(id)

    if reserva is None:
        return jsonify({"error": "Reservacion no encontrada"}), 404

    return jsonify(reserva), 200


@public_bp_reservations.route("/me", methods=["GET"])
@jwt_required()
def get_my_reservations():
    """
    Devuelve las reservaciones del usuario logueado.
    GET /public/reservations/me
    """
    user_id = get_jwt_identity()
    reservas = service_get_my_reservations(user_id)

    if reservas is None:
        return jsonify({"error": "Error al obtener las reservaciones"}), 500

    return jsonify(reservas), 200


@public_bp_reservations.route("/tables", methods=["GET"])
def get_tables():
    """
    Devuelve todas las mesas con su disponibilidad.
    Si llegan fecha y hora filtra por ese horario.
    Si no llegan devuelve todas sin filtro.

    GET /public/reservations/tables
    GET /public/reservations/tables?fecha=2026-06-01&hora=20
    """
    fecha = request.args.get("fecha")
    hora  = request.args.get("hora")

    tables, error = service_get_tables(fecha, hora)

    if error:
        return jsonify({"error": error}), 500

    return jsonify(tables), 200


@public_bp_reservations.route("/", methods=["POST"])
@jwt_required()
def create():
    """
    Crea una reservacion nueva.
    Requiere token JWT en el header: Authorization: Bearer <token>
    Espera JSON con: table_id, fecha, hora

    POST /public/reservations/
    Body: {"table_id": 2, "fecha": "2026-06-01", "hora": "20"}
    """
    user_id = get_jwt_identity()

    datos = request.get_json()

    if datos is None:
        return jsonify({"error": "Se esperaba JSON en el body"}), 400

    reserva_id, error = service_create_reservation(datos, user_id)

    if error is not None:
        if isinstance(error, dict) and error.get("tipo") == "mesa_no_disponible":
            return jsonify(error), 409
        return jsonify(error), 400

    return jsonify({
        "mensaje":    "Reservacion creada exitosamente",
        "reserva_id": reserva_id
    }), 201


@public_bp_reservations.route("/cancelar", methods=["GET"])
def cancelar_por_token():
    """
    Cancela una reservacion usando el token del QR.
    El cliente llega aca desde el link del email.

    GET /public/reservations/cancelar?token=xK9mP2nQr7vL4wZj
    """
    token = request.args.get("token")

    if token is None:
        return jsonify({"error": "Token requerido"}), 400

    ok, mensaje = service_cancel_by_token(token)

    if ok:
        return jsonify({"mensaje": mensaje}), 200
    else:
        return jsonify({"error": mensaje}), 400