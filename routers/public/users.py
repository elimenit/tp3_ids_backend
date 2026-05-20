"""Administracion de Usuarios.
"""

from flask import Blueprint, request, jsonify

from database.public.users import (
    db_get_user, db_create_user, db_delete_user
)
from utils.error import error_response

from services.public.users import (
    validation_creation, validation_id_user
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
  
    return jsonify(
        {
            "id": user[0],
            "name": user[1],
            "email": user[2],
            "category": user[3],
            "date": user[4],
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
    name: str = body.get('name', None)
    email: str = body.get('email', None)
    password: str = body.get('password', None)

    if not validation_creation(name, email, password):
        return error_response(
            "Campos Invalidos",
            "Uno o mas campos invalidos",
            400
        )
    name = name.strip().lower()
    email = email.strip().lower()
    password = password.strip()
    try:
        id_user = db_create_user(name, email, password)
    except Exception as e:
        return error_response(
            "Usuario ya existe",
            f"El error: {e}",
            400
        )
    return jsonify({"id": id_user}), 201

@public_bp_users.route(rule="/<int:id>", methods=["PUT"])
def update(id: int):
    """Actualizar Usuario.\n
    """
    pass

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
