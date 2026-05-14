"""Ordenes.\n
"""
from flask import Blueprint

bp_orders = Blueprint("orders", __name__, url_prefix='/orders')

@bp_orders.route("/", methods=['GET'])
def show()-> list:
    pass

@bp_orders.route("/<int:id>", methods=['GET'])
def get_order(id: int):
    pass

@bp_orders.route("/", methods=['POST'])
def create():
    pass

@bp_orders.route("/<int:id>", methods=['PUT'])
def update(id: int):
    pass

@bp_orders.route("/<int:id>", methods=['DELETE'])
def remove(id: int):
    pass