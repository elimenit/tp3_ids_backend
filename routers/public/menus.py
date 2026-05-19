"""Menus.\n
Platos accesibles al publico.\n
"""

from flask import Blueprint

public_bp_menu = Blueprint("public_menus", __name__, url_prefix="/public/menus")

@public_bp_menu.route("/", methods=['GET'])
def show()-> list:
    """Lista Menus.\n
    """
    pass

@public_bp_menu.route("/<int:id>", methods=['GET'])
def get_menu(id: int):
    pass

@public_bp_menu.route("/", methods=['POST'])
def create():
    pass

@public_bp_menu.route("/<int:id>", methods=['PUT'])
def update():
    pass

@public_bp_menu.route("/<int:id>", methods=['DELETE'])
def remove(id: int):
    pass

