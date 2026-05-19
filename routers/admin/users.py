"""Administracion de Usuarios.
"""

from flask import Blueprint, request
from database.db import get_connection
from utils.error import error_response

adm_bp_users = Blueprint("admin_users", __name__, url_prefix="/admin/users")

@adm_bp_users.route(rule="/", methods=["GET"])
def show()-> list:
    """Obtiene una lista de Usuarios.\n
    """
    # Query Params del endpoint
    limit: int = request.args.get('limit', 10, type=int)
    offset: int = request.args.get('offset', 0, type=int)
    
    query: str = "SELECT * FROM users WHERE LIMIT %s AND OFFSET %s"
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (limit, offset))
        users = cursor.fetchall() # devuelve una lista asi sea un elemento
        cursor.close()
        conn.close()
    except Exception as e:
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