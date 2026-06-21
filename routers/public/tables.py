from flask import Blueprint, request, jsonify
from utils.error import error_response
from database.public.tables import db_create_table

public_bp_tables = Blueprint('public_tables', __name__)

@public_bp_tables.route("/", methods=['GET'])
def get():
    pass

@public_bp_tables.route("/", methods=['POST'])
def create():
    body: dict = request.get_json()
    if not body:
        return error_response(
            "Body Empty",
            "Body Vacio",
            400
        )
    print(body)
    table_number = body.get('table_number', None)
    capacity = body.get('capacity', None)
    status = body.get('status', None)

    if not capacity or not status or not table_number:
        return error_response(
            "Campo Vacios",
            "Algun Campo esta Vacio",
            400
        )

    try:
        db_create_table(table_number, capacity, status)
    except Exception as e:
        return error_response(
            "No se registro la mesa", f"exception: {e}",
            400
        )
    return jsonify(), 201
    
