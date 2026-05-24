"""Iniciar session o Crear Cuenta.\n
"""
from database.public.users import db_login

from flask import Blueprint, jsonify, request

public_bp_login = Blueprint("public_login", __name__)

@public_bp_login.route("/", methods=['POST'])
def login():
    """Usuario inicia session.\n
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = db_login(email, password)
    return jsonify({"id": user}), 200