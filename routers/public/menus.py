from flask import Blueprint, request, jsonify
from database.public.menus import db_get_menus, db_get_menu
from utils.error import error_response


public_bp_menu = Blueprint("public_menus", __name__)

@public_bp_menu.route("/", methods=["GET"])
def list_menus():
    category = request.args.get("category", None)
    name = request.args.get("name", None)
    limit = request.args.get("_limit", 10, type=int)
    offset = request.args.get("_offset", 0, type=int)
    try:
        menus = db_get_menus(category, name, limit, offset)
    except Exception as e:
        return error_response("Error al obtener el menú", f"Error: {e}", 500)
    return jsonify(menus), 200

@public_bp_menu.route("/<int:menu_id>", methods=["GET"])
def get_menu(menu_id: int):
    try:
        menu = db_get_menu(menu_id)
    except Exception as e:
        return error_response("Error al obtener el plato", f"Error: {e}", 500)

    if menu is None:
        return error_response("Plato no encontrado", f"No existe el plato con id {menu_id}", 404)

    return jsonify(menu), 200
