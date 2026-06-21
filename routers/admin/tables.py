from utils.error import error_response
from database.admin.tables import db_create_table

from flask import Blueprint, request, jsonify

admin_bp_tables = Blueprint('admin_tables', __name__)

@admin_bp_tables.route("/", methods=['POST'])
def create():
    body: dict = request.get_json()
    if not body:
        return error_response("Error en la solicitud", "Body Vacio", 400)
    capacity = body.get('capacity')
    status = body.get('status')

    if capacity and status:
        db_create_table(capacity, status)
        return jsonify(), 201
    else:
        return error_response("Error en la solicitud", "Algun Campo esta Vacio", 400)    
