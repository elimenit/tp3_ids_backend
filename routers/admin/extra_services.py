from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.extra_services_service import (
    get_all_services,
    get_service_by_id,
    create_service,
    update_service,
    delete_service
)

adm_bp_extra_services = Blueprint('adm_bp_extra_services', __name__)

@adm_bp_extra_services.route("/", methods=["GET"])
@jwt_required()
def get_all():
    services = get_all_services()
    return jsonify(services), 200

@adm_bp_extra_services.route("/<int:service_id>", methods=["GET"])
@jwt_required()
def get_one(service_id):
    result = get_service_by_id(service_id)
    if result:
        return jsonify(result), 200
    return jsonify({"message": "Servicio no encontrado"}), 404

@adm_bp_extra_services.route("/", methods=["POST"])
@jwt_required()
def create():
    data = request.get_json()
    if not data:
        return jsonify({"message": "JSON inválido"}), 400
    result = create_service(data)
    if result:
        return jsonify({"message": "Servicio creado con éxito"}), 201
    return jsonify({"message": "Error al crear el servicio"}), 400

@adm_bp_extra_services.route("/<int:service_id>", methods=["PUT"])
@jwt_required()
def update(service_id):
    data = request.get_json()
    if not data:
        return jsonify({"message": "JSON inválido"}), 400
    result = update_service(service_id, data)
    if result:
        return jsonify({"message": "Servicio actualizado con éxito"}), 200
    return jsonify({"message": "Servicio no encontrado o error al actualizar"}), 404

@adm_bp_extra_services.route("/<int:service_id>", methods=["DELETE"])
@jwt_required()
def delete(service_id):
    result = delete_service(service_id)
    if result:
        return jsonify({"message": "Servicio eliminado con éxito"}), 200
    return jsonify({"message": "Servicio no encontrado"}), 404