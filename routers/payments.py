"""Pagos.\n
"""
from flask import Blueprint

bp_payment = Blueprint("payment", __name__, url_prefix="/payment")

@bp_payment.route("/", methods=['GET'])
def show():
    """Lista Historial de Pagos.\n
    """
    pass

@bp_payment.route("/<int:id>", methods=['GET'])
def get_payment(id: int):
    pass

@bp_payment.route("/", methods=['POST'])
def create():
    pass

@bp_payment.route("/", methods=['PUT'])
def update():
    pass

@bp_payment.route("/<int: id>", methods=['DELETE'])
def remove(id: int):
    pass
