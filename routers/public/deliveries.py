"""Rutas para la gestión de deliverys.\n
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from database.public.deliveries import (
    db_create_delivery, db_get_deliveries, db_get_delivery, db_cancelled_delivery
)
from services.public.deliveries import validation_create_delivery
from utils.error import error_response

public_bp_delivery = Blueprint("public_delivery", __name__)

@public_bp_delivery.route("/", methods=['GET'])
@jwt_required()
def show():
    """Usuario Obtiene informacion de sus deliveries.\n
    """
    user_id = int(get_jwt_identity())
    try:
        deliveries = db_get_deliveries(user_id)  
        if deliveries is None:
            return error_response(
                "User not found",
                "No se encontro al usuario",
                404)

    except Exception as e:
        print(e)
        return error_response(
            "conexion refused",
            f"Error: {e}",
            400)

    return jsonify(deliveries), 200
    
@public_bp_delivery.route("/<int:delivery_id>", methods=["GET"])
@jwt_required()
def get_delivery(delivery_id: int)-> dict:
    user_id = int(get_jwt_identity())
    try:
        
        delivery = db_get_delivery(user_id, delivery_id)
        if delivery is None:
            return error_response(
                "User o delivery not found",
                "usuario o delivery no encontrado",
                404)    
    
    except Exception as e:
        print(f"Error: {e}")
        return error_response(
            "conexion refused",
            f"Error: {e}",
            400)

    return jsonify(delivery), 200

@public_bp_delivery.route("/", methods=['POST'])
@jwt_required()
def create():
    """Crea el pedido de delivery.\n
    """
    user_id = int(get_jwt_identity())
    body = request.get_json()

    if not body:
        return error_response(
            "Campos Invalidos",
            "Body vacio",
            400)
    

    list_menus_quantity = body.get('list_menus', None)
    address = body.get('address', None)
    date = body.get('date', None)
    
    if not validation_create_delivery(list_menus_quantity, address, date):
        return error_response(
            "Campo Invalido",
            "Algun campo Invalido",
            400)
    try:
        id_deli = db_create_delivery(user_id, list_menus_quantity, address, date)
    except Exception as e:
        print(e)
        return error_response(
            "Hubo un error",
            f"Error: {e}",
            404)
    return jsonify({"id": id_deli if id_deli else 'null'}), 201

@public_bp_delivery.route("/<int:delivery_id>", methods=["DELETE"])
@jwt_required()
def cancelled(delivery_id: int):
    user_id = int(get_jwt_identity())
    try:
        db_cancelled_delivery(user_id, delivery_id)
    
    except Exception as e:
        print(e)
        return error_response(
            "Usuario o id no encontrado",
            f"Error: {e}",
            404
        )
    return jsonify(), 204
