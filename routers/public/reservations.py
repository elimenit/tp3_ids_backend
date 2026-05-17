"""Endpoint Reservacion.\n
"""
from flask import Blueprint, request

public_bp_reservations = Blueprint("public_reservations", __name__, url_prefix="/public/reservations")

@public_bp_reservations.route("/<int:id>", methods=["GET"])
def get_reservation(id: int):
    """Obtiene Reservacion.\n
    """

@public_bp_reservations.route("/", methods=['POST'])
def create():
    pass

@public_bp_reservations.route("/", methods=['PUT'])
def update():
    pass


@public_bp_reservations.route("/<int:id>", methods=['DELETE'])
def remove(id: int):
    """Elimina Reservacion.\n
    """
    pass

