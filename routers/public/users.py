"""Administracion de Usuarios.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from database.public.users import (
    db_update_user, db_delete_user
)
from utils.error import error_response

from services.public.users import (
    create_user, validation_id_user, obtain_user
)

public_bp_users = Blueprint("public_users", __name__)

@public_bp_users.route(rule="/", methods=["GET"])
@jwt_required()
def get_user():
    user: dict = get_jwt_identity()
    if not user:
        return error_response(
            "Error durante la obtención de datos",
            "No se ha encontrado el usuario",
            400
        )
    return obtain_user(user)

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
        token = create_user(name, email, password)
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
    return jsonify({"token": token}), 201

@public_bp_users.route(rule="/", methods=["PUT"])
@jwt_required()
def update():
    """Actualizar Usuario.\n
    """
    user: dict = get_jwt_identity()
    if not user:
        return error_response(
            "Error durante la obtención de datos",
            "No se ha encontrado el usuario",
            400
        )
    id = user.get("id", 0)
    if not validation_id_user(id):
        return error_response(
            "Error",
            "Se ha proporcionado un ID inválido",
            400
        )
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
 

@public_bp_users.route(rule="/", methods=["PATCH"])
def partial_updat():
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
