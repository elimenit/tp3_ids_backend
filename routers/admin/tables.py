from utils.auth import is_admin
from utils.error import error_response
from database.admin.tables import db_create_table, db_deactivate_table, db_get_all_tables, db_update_table

from flask_jwt_extended import jwt_required
from flask import Blueprint, request, jsonify

admin_bp_tables = Blueprint('admin_tables', __name__)

@admin_bp_tables.get(rule="/")
@jwt_required()
def show():
    """Obtiene una lista de Mesas."""
    if not is_admin():
        return error_response("Acceso no autorizado", "No tienes permisos para realizar esta acción", 403)

    limit = request.args.get('_limit', 10, type=int)
    offset = request.args.get('_offset', 0, type=int)
    tables, tables_count = db_get_all_tables(limit, offset)
    return jsonify({
        "data": tables,
        "count": tables_count
    }), 200

@admin_bp_tables.route("/", methods=['POST'])
@jwt_required()
def create():
    if not is_admin():
        return error_response("Acceso denegado", "No tienes permisos para realizar esta acción", 403)
    body: dict = request.get_json()
    if not body:
        return error_response("Error en la solicitud", "Body Vacio", 400)
    capacity = body.get('capacity')

    if capacity:
        db_create_table(capacity)
        return jsonify(), 201
    else:
        return error_response("Error en la solicitud", "Algun Campo esta Vacio", 400)    

@admin_bp_tables.put(rule="/<int:table_id>")
@jwt_required()
def update(table_id: int):
    """Actualiza los datos de una mesa."""
    if not is_admin():
        return error_response("Acceso no autorizado", "No tienes permisos para realizar esta acción", 403)
    data = request.get_json()
    if not data:
        return error_response("Error en la solicitud", "Body Vacio", 400)
    affected_rows = db_update_table(table_id, data)
    if not affected_rows:
        return error_response("Error al actualizar la mesa", "No se encontró la mesa", 404)
    return jsonify(), 204


@admin_bp_tables.delete(rule="/<int:table_id>")
@jwt_required()
def deactivate(table_id: int):
    """Desactiva una mesa, cambiando su estado a 'inactive'."""
    if not is_admin():
        return error_response("Acceso no autorizado", "No tienes permisos para realizar esta acción", 403)
    affected_rows = db_deactivate_table(table_id)
    if not affected_rows:
        return error_response("Error al desactivar la mesa", "No se encontró la mesa o ya está inactiva", 404)
    return jsonify(), 204

    