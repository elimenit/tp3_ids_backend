"""Pagos.\n
"""
from flask import Blueprint

public_bp_payment = Blueprint("public_payments", __name__)

@public_bp_payment.route("/<int:id>", methods=['GET'])
def get_payment(id: int):
    """Obtener pagos. También puede obtener un pago específico.\n
    """
    pass

@public_bp_payment.route("/", methods=['POST'])
def create():
    pass

@public_bp_payment.route("/", methods=['PUT'])
def update():
    pass

@public_bp_payment.route("/<int:id>", methods=['DELETE'])
def remove(id: int):
    pass
