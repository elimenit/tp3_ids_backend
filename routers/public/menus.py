"""Un usuario no puede alterar un menu.\n
"""
from flask import Blueprint, jsonify, request
from utils.error import error_response
from database.public.menus import (
    db_get_menus, db_get_menu
)
from services.public.menus import validation_limit_offset

public_bp_menu = Blueprint('public_menus', __name__)

@public_bp_menu.route(rule="/", methods=['GET'])
def show():
    limit = request.args.get('_limit', 10, type=int)
    offset = request.args.get('_offset', 0, type=int)
    category = request.args.get('category', None)
    name = request.args.get('name', None)

    if not validation_limit_offset(limit, offset):
        return error_response(
            "Limit u Offset Invalidos",
            "Limit u offset no validos",
            400
        )

    try:
        menus = db_get_menus(name, category, limit, offset)
    except Exception as e:
        print(e)
        return error_response(
            "conexion refused",
            f"Error: {e}",
            400)
        
    return jsonify(menus), 200
    
@public_bp_menu.route("/<int:menu_id>", methods=['GET'])
def get_menu(menu_id: int):
    
    try: 
        menu = db_get_menu(menu_id)
        if menu is None:
            return error_response(
                "Menu not found",
                "Menu no encontrado",
                404)
    except Exception as e:
        return error_response(
            "Conexion refused",
            f"Error: {e}",
            400)
    return jsonify(menu), 200