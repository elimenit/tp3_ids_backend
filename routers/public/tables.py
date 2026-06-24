from database.public.tables import db_get_active_tables

from flask import Blueprint, request, jsonify

public_bp_tables = Blueprint('public_tables', __name__)

@public_bp_tables.get(rule="/")
def show():
    """Obtiene una lista de Mesas."""
    limit = request.args.get('_limit', 10, type=int)
    offset = request.args.get('_offset', 0, type=int)
    tables, tables_count = db_get_active_tables(limit, offset)
    return jsonify({
        "data": tables,
        "count": tables_count
    }), 200