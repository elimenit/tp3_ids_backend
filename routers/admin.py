"""Usuario Admin.\n
Endpoints correspondientes al usuario administrador.
"""
from flask import Blueprint

bp_admin = Blueprint("admin", __name__, url_prefix='/admin')