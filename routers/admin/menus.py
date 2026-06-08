from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from database.admin.menus import (
    db_list_menus, db_get_menu, db_create_menu, db_update_menu, db_delete_menu
)
from services.admin.menus import validation_create_menu, validation_update_menu
from utils.error import error_response
from utils.auth import is_admin

adm_bp_menus = Blueprint("admin_menus", __name__)

@adm_bp_menus.route("/", methods=["GET"])
@jwt_required()
def list_menus():
    if not is_admin():
        return error_response("Sin permisos", "Solo administradores pueden acceder", 403)
    try:
        menus = db_list_menus()
    except Exception as e:
        return error_response("Error al obtener menús", f"Error: {e}", 500)
    return jsonify(menus), 200

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
    price = body.get("price")
    image_url = body.get("image_url")

    if not validation_create_menu(category, name, description, price):
        return error_response("Campos inválidos", "Revisá los campos. La categoría debe ser una de: drinks, burgers, pasta, soup", 400)

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
    price = body.get("price")
    available = body.get("available")
    image_url = body.get("image_url")

    if not validation_update_menu(category, name, description, price, available):
        return error_response("Campos inválidos", "Revisá los campos. La categoría debe ser una de: drinks, burgers, pasta, soup", 400)

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
