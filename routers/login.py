"""Iniciar session o Cerrar session.
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from services.public.users import login_user

public_bp_login = Blueprint("public_login", __name__)

@public_bp_login.route("/", methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        raise ValueError("El cuerpo no puede estar vacío")
    token = login_user(data.get('email', ''), data.get('password', ''))
    return jsonify({"token": token}), 200