"""Rutas para la gestión de deliverys.\n
"""
from flask import Blueprint

public_bp_delivery = Blueprint("public_delivery", __name__, url_prefix="/public/delivery")

@public_bp_delivery.route("/create-account", methods=['GET'])
def show_delivery():
    """Usuario crea una Cuenta.\n
    """
    pass

@public_bp_delivery.route("/create-delivery", methods=['POST'])
def create_delivery():
    """Crea el pedido de delivery.\n
    """
    pass