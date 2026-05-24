"""Rutas para la gestión de dashboards.\n
"""
from flask import Blueprint

adm_bp_dashboards = Blueprint("admin_dashboards", __name__, url_prefix="/admin/dashboards")

@adm_bp_dashboards.route("/show", methods=['GET'])
def show():
    """Dashboard Principal.\n
    """
    pass

# Users
@adm_bp_dashboards.route("/users", methods=["GET"])
def dashboard_users():
    pass

# Deliveries
@adm_bp_dashboards.route("/deliveries", methods=["GET"])
def dashboard_deliveries():
    pass

# Menus
@adm_bp_dashboards.route("/menus", methods=["GET"])
def bashboard_menus():
    pass

# Reservations
@adm_bp_dashboards.route("/reservations", methods=["GET"])
def dashboard_reservations():
    pass