from utils.auth import is_admin
from utils.error import error_response
from services.admin.reservations import (
    service_get_all_reservations,
    update_reservation
)

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

adm_bp_reservations = Blueprint("admin_reservations", __name__)

@adm_bp_reservations.get(rule="/")
@jwt_required()
def show():
    """Obtiene una lista de todas las reservaciones con paginación."""
    if not is_admin():
        return error_response('Error al obtener las reservaciones', 'Acceso no autorizado',status_code=403)
        
    limit = request.args.get('_limit', 10, type=int)
    offset = request.args.get('_offset', 0, type=int)

    try:
        reservations, reservations_count = service_get_all_reservations(limit, offset)
        return jsonify({
            "data": reservations,
            "count": reservations_count
        }), 200
    except (ValueError, Exception) as e:
        return error_response('Error al obtener las reservaciones', str(e), 400)

@adm_bp_reservations.put(rule="/<int:res_id>")
@jwt_required()
def update(res_id: int):
    if not is_admin():
        return error_response("Acceso no autorizado", "No tienes permisos para realizar esta acción", 403)
    data = request.get_json()
    try:
        res, code = update_reservation(res_id, data)
    except (ValueError, Exception) as e:
        return error_response('Error durante la actualizacion.', str(e), 400)
    if code != 204:
        return res, code
    return '', 204