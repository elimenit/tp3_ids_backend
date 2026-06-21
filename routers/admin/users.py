from utils.error import error_response
from utils.auth import is_admin
from services.admin.users import get_all_users, create_user, update_user, toggle_user_status

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

adm_bp_users = Blueprint("admin_users", __name__)

@adm_bp_users.get(rule="/")
@jwt_required()
def show():
    """Obtiene una lista de Usuarios."""
    if not is_admin():
        return error_response("Acceso no autorizado", "No tienes permisos para realizar esta acción", 403)

    limit = request.args.get('_limit', 10, type=int)
    offset = request.args.get('_offset', 0, type=int)
    users, users_count = get_all_users(limit, offset)
    return jsonify({
        "data": users,
        "count": users_count
    }), 200

@adm_bp_users.post(rule="/")
@jwt_required()
def create():
    """Crea un nuevo usuario."""
    if not is_admin():
        return error_response("Acceso no autorizado", "No tienes permisos para realizar esta acción", 403)

    data = request.get_json()

    try:
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        category = data.get("category", "normal")

        if not name or not email or not password:
            return error_response('Error durante la creación de usuario', 'Se deben proveer nombre, email, constraseña y categoría.', 400)

        user = create_user(name, email, password, category)
        return jsonify(user), 201

    except (ValueError, Exception) as e:
        return error_response('Error durante la creación de usuario', str(e), 400)


@adm_bp_users.put(rule="/<int:user_id>")
@jwt_required()
def update(user_id: int):
    """Actualiza los datos de un usuario."""
    if not is_admin():
        return error_response("Acceso no autorizado", "No tienes permisos para realizar esta acción", 403)

    data = request.get_json()

    try:
        update_user(user_id, data)
        return jsonify({"mensaje": "Usuario actualizado correctamente"}), 200

    except (ValueError, Exception) as e:
        return error_response('Error durante la actualizacion.', str(e), 400)


@adm_bp_users.delete(rule="/<int:user_id>")
@jwt_required()
def delete(user_id: int):
    """Alterna el estado del usuario entre activo e inactivo."""
    if not is_admin():
        return error_response("Acceso no autorizado", "No tienes permisos para realizar esta acción", 403)

    try:
        new_status = toggle_user_status(user_id)
        return jsonify({"mensaje": "Estado actualizado correctamente", "status": new_status}), 200

    except (ValueError, Exception) as e:
        return error_response('Error durante la alternación de estado.', str(e), 400)