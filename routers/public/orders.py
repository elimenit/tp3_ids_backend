"""Ordenes.\n
"""
from flask import Blueprint

public_bp_orders = Blueprint("public_orders", __name__, url_prefix='/public/orders')

@public_bp_orders.route("/", methods=['GET'])
def show()-> list:
    pass

@public_bp_orders.route("/<int:id>", methods=['GET'])
def get_order(id: int):
    pass

@public_bp_orders.route("/", methods=['POST'])
def create():
    pass

@public_bp_orders.route("/<int:id>", methods=['PUT'])
def update(id: int):
    pass

@public_bp_orders.route("/<int:id>", methods=['DELETE'])
def remove(id: int):
    pass