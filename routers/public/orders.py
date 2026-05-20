"""Ordenes.\n
"""
from flask import Blueprint, request, jsonify
# validaciones
from services.public.orders import validation_limit_offset
# Base de Datos
from database.public.orders import (
    db_get_orders, db_get_order, db_create_order, db_delete_order
)
from utils.error import error_response

public_bp_orders = Blueprint("public_orders", __name__)

@public_bp_orders.route("/<int:user_id>", methods=['GET'])
def show(user_id: int)-> list:
    limit = request.args.get('_limit', 10, type=int)
    offset = request.args.get('_offset', 0, type=int)

    if not validation_limit_offset(limit, offset):
        return error_response(
            message="Limit y offset invalidos",
            description="Incumple el tamanio maximo de 10 elementos",
            status_code=400
        )
    orders: list = db_get_orders(user_id, limit, offset)

    return jsonify(orders), 200

@public_bp_orders.route("/<int:user_id>/<int:order_id>", methods=['GET'])
def get_order(user_id: int, order_id: int):
    order = {}
   
    try:
        order = db_get_order(user_id, order_id)
    except Exception as e:
        print(e)
       
        return error_response(
            "Orden no encontrada",
            f"error: {e}",
            404
        )
    return jsonify(order), 200

@public_bp_orders.route("/<int:user_id>", methods=['POST'])
def create(user_id: int):
    body = request.get_json()
    if not body:
        return error_response(
            "Body Vacio",
            "Body Empty",
            400
        )
    
    
    

@public_bp_orders.route("/<int:id>", methods=['PUT'])
def update(id: int):
    pass

@public_bp_orders.route("/<int:id>", methods=['DELETE'])
def remove(id: int):
    pass