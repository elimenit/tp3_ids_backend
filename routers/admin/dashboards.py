"""Rutas para la gestión de dashboards.\n
"""
from flask import Blueprint

adm_bp_dashboards = Blueprint("admin_dashboards", __name__, url_prefix="/admin/dashboards")

@adm_bp_dashboards.route("/show-dashboards", methods=['GET'])
def show_dashboards():
    """Muestra los dashboards.\n
    """
    pass