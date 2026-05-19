"""
Rutas para la autogestión del usuario.\n
"""

from flask import Blueprint

public_bp_users = Blueprint("public_users", __name__, url_prefix="/public/users")

@public_bp_users.route(rule="/<int:id>", methods=["PUT"])
def update(id: int):
    """Actualizar Usuario.\n
    """
    pass

@public_bp_users.route(rule="/<int:id>", methods=["PATCH"])
def partial_update(id: int):
    """Actualizacion Parcial.\n
    """
    pass

@public_bp_users.route(rule="/<int:id>", methods=["DELETE"])
def delete(id: int):
    """ Eliminar su Usuario.\n
    """
    pass