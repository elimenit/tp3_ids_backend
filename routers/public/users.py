"""Administracion de Usuarios.
"""

from flask import Blueprint, request, jsonify

from database.public.users import (
    db_get_user, db_update_user, db_delete_user
)
from utils.error import error_response

from services.public.users import (
    create_user, validation_id_user
)

public_bp_users = Blueprint("public_users", __name__)

@public_bp_users.route(rule="/<int:id>", methods=["GET"])
def get_user(id: int):
    """Obtiene un Usuario.\n
    """
    try:
        user = db_get_user(id)
    except Exception as e:
        return error_response(message="Usuario No encontrado", description=f"error: {e}", status_code=404)
    print(user)
    if user["status"] == "inactive":
        return error_response(message="Usuario Inactivo", description="El usuario se encuentra inactivo", status_code=403)
    
    return jsonify(
        {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "category": user["category"],
            "date": user["created_at"],
            "status": user["status"]
        }
    ), 200

@public_bp_users.route("/", methods=["POST"])
def create():
    body = request.get_json()
    print(body)
    if not body:
        return error_response(
            "Cuerpo vacio",
            "Vacio",
            400
        )
    name: str = body.get('name', "")
    email: str = body.get('email', "")
    password: str = body.get('password', "")

    try:
        id_user = create_user(name, email, password)
    except ValueError as e:
        return error_response(
            "Campos Invalidos",
            str(e),
            400
        )
    except Exception as e:
        return error_response(
            "Error durante la creación del usuario",
            str(e),
            400
        )
    return jsonify({"id": id_user}), 201

@public_bp_users.route(rule="/<int:id>", methods=["PUT"])
def update(id: int):
    """Actualizar Usuario.\n
    """
    body = request.get_json()
    if not body:
        return error_response(
            "Cuerpo vacio",
            "Vacio",
            400
        )
    name: str = body.get('name', None)
    password: str = body.get('password', None)

    try:
        db_update_user(id, name, password)
    except Exception as e:
        print(e)
        return error_response(
            "No se Encontro al usuario",
            f"Error:{e}",
            404
        )
    return jsonify(), 204
 

@public_bp_users.route(rule="/<int:id>", methods=["PATCH"])
def partial_update(id: int):
    """Actualizacion Parcial.\n
    """
    pass

@public_bp_users.route(rule="/<int:id>", methods=["DELETE"])
def delete(id: int):
    """ Eliminar un Usuario.\n
    """
    if not validation_id_user(id):
        return error_response(
            "Id Invalido",
            "Id del usuario fuera de rango",
            400
        )
    try:
        email = db_delete_user(id)
    except Exception as e:
        return error_response(
            "El usuario no fue encontrado",
           f"error: {e}",
           404
        )
        
    return jsonify({"id": id, "email": email}), 200
