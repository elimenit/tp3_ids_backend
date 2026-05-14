"""Endpoint Reservacion.\n
"""
from flask import Blueprint, request

bp_reservations = Blueprint("reservations",__name__, url_prefix="/reservations")

@bp_reservations.route("/", methods=["GET"])
def show()-> list:
    """ Lista de Reservaciones.\n
    """
    limit: int = request.args.get('limit', 10, type=int)
    offset: int = request.args.get('offset', 0, type=int)


@bp_reservations.route("/<int:id>", methods=["GET"])
def get_reservation(id: int):
    """Obtiene Reservacion.\n
    """

@bp_reservations.route("/", methods=['POST'])
def create():
    pass

@bp_reservations.route("/", methods=['PUT'])
def update():
    pass


@bp_reservations.route("/<int:id>", methods=['DELETE'])
def remove(id: int):
    """Elimina Reservacion.\n
    """
    pass

