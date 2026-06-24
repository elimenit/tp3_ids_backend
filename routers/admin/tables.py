from flask import Blueprint, jsonify, request
from database.admin.tables import (
    db_delete_table, db_get_all_tables
)
from utils.error import error_response
from flask_jwt_extended import jwt_required

admin_bp_tables = Blueprint('admin_tables', __name__)

@admin_bp_tables.route("/", methods=["GET"])
@jwt_required()
def all_tables():
    limit: int = request.args.get('_limit', 10, type=int)
    offset: int = request.args.get('_offset', 0, type=int)
    try: 
        return jsonify(db_get_all_tables(limit, offset)), 200
    except Exception as e:
        return error_response(
            "Error",
            f"{str(e)}",
            400
        )

@admin_bp_tables.route("/", methods=["POST"])
@jwt_required()
def delete():
    """Elimina una mesa.
    """
    body = request.get_json()
    if not body:
        return error_response(
            "Body EMpty",
            "Body Vacio",
            400
        )
    try: 
        table_id = body.get("id", None)
        if not table_id:
            return error_response(
                "No se paso table id",
                "Id invalido",
                400
            )
        return jsonify(db_delete_table(table_id)), 200
    except Exception as e:
        return error_response(
            "Hubo algun Problema",
            f"{str(e)}",
            400
        )
