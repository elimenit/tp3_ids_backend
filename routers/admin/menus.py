from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from database.admin.menus import (
    db_get_menu, db_create_menu, db_update_menu, db_delete_menu
)
from services.admin.menus import validation_create_menu, validation_update_menu, get_all_menus
from utils.error import error_response
from utils.auth import is_admin

adm_bp_menus = Blueprint("admin_menus", __name__)

@adm_bp_menus.get(rule="/")
@jwt_required()
def show():
    """Obtiene el menú con paginación."""
    if not is_admin():
        return error_response('Error al acceder', 'Acceso no autorizado',status_code=403)

    limit = request.args.get('_limit', 10, type=int)
    offset = request.args.get('_offset', 0, type=int)

    try:
        products, prod_count = get_all_menus(limit, offset)
        return jsonify({
            "data": products,
            "count": prod_count
        }), 200
    except (ValueError, Exception) as e:
        return error_response('Error al obtener el menú', str(e), 400)

@adm_bp_menus.route("/<int:menu_id>", methods=["GET"])
@jwt_required()
def get_menu(menu_id: int):
    if not is_admin():
        return error_response("Sin permisos", "Solo administradores pueden acceder", 403)
    try:
        menu = db_get_menu(menu_id)
    except Exception as e:
        return error_response("Error al obtener el menú", f"Error: {e}", 500)

    if menu is None:
        return error_response("Menú no encontrado", f"No existe el menú con id {menu_id}", 404)

    return jsonify(menu), 200

@adm_bp_menus.route("/", methods=["POST"])
@jwt_required()
def create_menu():
    if not is_admin():
        return error_response("Sin permisos", "Solo administradores pueden acceder", 403)

    body = request.get_json()

    if not body:
        return error_response("Body inválido", "El body está vacío", 400)

    category = body.get("category")
    name = body.get("name")
    description = body.get("description")
    try:
        price = float(body.get("price"))
    except TypeError:
        return error_response('Campo inválido', f'El campo `precio` debe tener un número positivo.', 400)
    image_url = body.get("image_url")

    if not validation_create_menu(category, name, description, price):
        return error_response("Campos inválidos", "Revisá los campos enviados", 400)

    try:
        new_id = db_create_menu(category, name, description, price, image_url)
    except Exception as e:
        return error_response("Error al crear el menú", f"Error: {e}", 500)

    return jsonify({"id": new_id}), 201

@adm_bp_menus.route("/<int:menu_id>", methods=["PUT"])
@jwt_required()
def update_menu(menu_id: int):
    if not is_admin():
        return error_response("Sin permisos", "Solo administradores pueden acceder", 403)

    body = request.get_json()

    if not body:
        return error_response("Body inválido", "El body está vacío", 400)

    category = body.get("category")
    name = body.get("name")
    description = body.get("description")
    try:
        price = float(body.get("price"))
    except TypeError:
        return error_response('Campo inválido', f'El campo `precio` debe tener un número positivo.', 400)
    available = body.get("available") == 'on'
    image_url = body.get("image_url")

    if not validation_update_menu(category, name, description, price, available):
        return error_response("Campos inválidos", "Revisá los campos enviados", 400)

    try:
        updated = db_update_menu(menu_id, category, name, description, price, available, image_url)
    except Exception as e:
        return error_response("Error al actualizar el menú", f"Error: {e}", 500)

    if not updated:
        return error_response("No se pudo actualizar", f"No existe el menú con id {menu_id}", 404)

    return jsonify({"mensaje": "Menú actualizado correctamente"}), 200

@adm_bp_menus.route("/<int:menu_id>", methods=["DELETE"])
@jwt_required()
def delete_menu(menu_id: int):
    if not is_admin():
        return error_response("Sin permisos", "Solo administradores pueden acceder", 403)

    try:
        deleted = db_delete_menu(menu_id)
    except Exception as e:
        return error_response("Error al eliminar el menú", f"Error: {e}", 500)

    if not deleted:
        return error_response("No se pudo eliminar", f"No existe el menú con id {menu_id}", 404)

    return jsonify({"mensaje": "Menú eliminado correctamente"}), 200
