"""Administracion de Usuarios.
"""

from flask import Blueprint, request
from utils.error import error_response
from database.admin.users import db_list_users
from services.admin.users import validar_limit_offset

adm_bp_users = Blueprint("admin_users", __name__)

@adm_bp_users.route(rule="/", methods=["GET"])
def show()-> list:
    """Obtiene una lista de Usuarios.\n
    """
    # Query Params del endpoint
    limit: int = request.args.get('limit', 10, type=int)
    offset: int = request.args.get('offset', 0, type=int)
    if not validar_limit_offset(limit, offset):
        return error_response(
            "Limit u Offset Invalidos",
            "Limit u offset fuera de rango",
            400
        )
        
    try:    
        users = db_list_users(limit, offset)
    except:         
        return error_response(message=f"Exception: {e}", description="Base de Datos no Inicializada", status_code=500)
    
    return users

@adm_bp_users.route(rule="/<int:id>", methods=["GET"])
def get_user(id: int):
    """Obtiene un Usuario.\n
    """
    query: str = "SELECT * FROM users WHERE id = %s"
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (id, ))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user is None:
            return error_response(message=f"id no existente: {id}", description="Usuario no encontrado", status_code=404)

    except Exception as e:
        return error_response(message=f"Exception: {e}", description="Base de Datos no Inicializada", status_code=500)
    return user

@adm_bp_users.route(rule="/<int:id>", methods=["PUT"])
def update(id: int):
    """Actualizar Usuario.\n
    """
    pass

@adm_bp_users.route(rule="/<int:id>", methods=["PATCH"])
def partial_update(id: int):
    """Actualizacion Parcial.\n
    """
    pass

@adm_bp_users.route(rule="/<int:id>", methods=["DELETE"])
def delete(id: int):
    """ Eliminar un Usuario.\n
    """
    pass