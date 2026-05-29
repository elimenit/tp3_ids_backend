"""Iniciar session o Crear Cuenta.\n
"""
from flask import Blueprint, jsonify, request
from utils.error import error_response
from services.public.users import login_user

public_bp_login = Blueprint("public_login", __name__)

@public_bp_login.route("/", methods=['POST'])
def login():
    """Usuario inicia session.\n
    """
    data = request.get_json()
    if not data:
        return error_response(
            "Cuerpo vacio",
            "Vacio",
            400
        )
    email = data.get('email', "")
    password = data.get('password', "")
    
    try:
        user_id = login_user(email, password)
    except ValueError as e:
        return error_response(
            "Credenciales inválidas",
            str(e),
            401
        )
    except Exception as e:
        return error_response(
            "Error durante el login",
            str(e),
            400
        )
    
    return jsonify({"id": user_id}), 200