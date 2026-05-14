"""Menus.\n
Platos accesibles al publico.\n
"""

from flask import Blueprint

bp_menu = Blueprint("menu", __name__, url_prefix="/menus")

@bp_menu.route("/", methods=['GET'])
def show()-> list:
    """Lista Menus.\n
    """
    pass

@bp_menu.route("/<int:id>", methods=['GET'])
def get_menu(id: int):
    pass

@bp_menu.route("/", methods=['POST'])
def create():
    pass

@bp_menu.route("/<int:id>", methods=['PUT'])
def update():
    pass

@bp_menu.route("/<int:id>", methods=['DELETE'])
def remove(id: int):
    pass

