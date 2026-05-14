"""Iniciar session o Crear Cuenta.\n
"""
from flask import Blueprint

public_bp_login = Blueprint("public_login", __name__, url_prefix="/public/login")

@public_bp_login.route("/", methods=['POST'])
def login():
    """Usuario inicia session.\n
    """
    pass

@public_bp_login.route("/close-session", methods=['POST'])
def logout():
    """Usuario cierra su session.\n
    """
    pass