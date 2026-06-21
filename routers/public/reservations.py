from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from services.public.reservations import service_get_my_reservations, service_get_reservation, service_create_reservation, service_cancel_by_token
from utils.error import error_response

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
    if not datos:
        return error_response('Error en los datos', 'No se recibieron datos en formato JSON', 400)

    res, code = service_create_reservation(datos, user_id)
    if res:
        return res, code
    
    return jsonify({
        "message":    "Reservacion creada exitosamente",
        "reserva_id": code
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