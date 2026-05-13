"""Iniciar session o Crear Cuenta.\n
"""
from flask import Blueprint

bp_login = Blueprint("login", __name__, url_prefix="/login")

@bp_login.route("/", methods=['GET'])
def obtener_session():
    """Usuario inicia session.\n
    """
    pass

@bp_login.route("/create-account", methods=['POST'])
def create_account():
    """Usuario crea una Cuenta.\n
    """
    pass