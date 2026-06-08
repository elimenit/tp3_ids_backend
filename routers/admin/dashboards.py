from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from utils.helpers import _is_admin, _get_date_range
from database.admin.dashboard import (
    db_get_reservations_dashboard,
    db_get_delivery_dashboard,
    db_get_reviews_dashboard,
)

adm_bp_dashboards = Blueprint("admin_dashboards", __name__)

@adm_bp_dashboards.get("/reservations")
@jwt_required()
def get_reservations_dashboard():
    user_id = int(get_jwt_identity())
    if not _is_admin(user_id):
        return jsonify({"error": "Acceso no autorizado"}), 403

    inicio, fin = _get_date_range()
    data = db_get_reservations_dashboard(inicio, fin)
    return jsonify(data), 200


@adm_bp_dashboards.get("/deliveries")
@jwt_required()
def get_deliveries_dashboard():
    user_id = int(get_jwt_identity())
    if not _is_admin(user_id):
        return jsonify({"error": "Acceso no autorizado"}), 403

    inicio, fin = _get_date_range()
    data = db_get_delivery_dashboard(inicio, fin)
    return jsonify(data), 200


@adm_bp_dashboards.get("/reviews")
@jwt_required()
def get_reviews_dashboard():
    user_id = int(get_jwt_identity())
    if not _is_admin(user_id):
        return jsonify({"error": "Acceso no autorizado"}), 403

    inicio, fin = _get_date_range()
    data = db_get_reviews_dashboard(inicio, fin)
    return jsonify(data), 200