from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.public.users import (
    create_user, delete_user, update_user_complete, 
    update_user_partial, obtain_user
)

public_bp_users = Blueprint("public_users", __name__)


@public_bp_users.route("/", methods=['POST'])
def create():
    data = request.get_json()
    if not data:
        raise ValueError("El cuerpo no puede estar vacío")
    
    token = create_user(
        data.get('name', ''),
        data.get('email', ''),
        data.get('password', '')
    )
    return jsonify({"token": token}), 201


@public_bp_users.route("/me", methods=['GET'])
@jwt_required()
def get_user():
    user_id = int(get_jwt_identity())
    user = obtain_user(user_id)
    return jsonify(user), 200


@public_bp_users.route("/me", methods=['PUT'])
@jwt_required()
def update_user():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    if not data:
        raise ValueError("El cuerpo no puede estar vacío")
    
    token = update_user_complete(
        user_id,
        data.get('name', ''),
        data.get('password', '')
    )
    return jsonify({"token": token}), 200


@public_bp_users.route("/me", methods=['PATCH'])
@jwt_required()
def partial_update_user():
    user_id = int(get_jwt_identity())

    data = request.get_json()
    if not data:
        raise ValueError("El cuerpo no puede estar vacío")
    
    token = update_user_partial(user_id, data)
    return jsonify({"token": token}), 200


@public_bp_users.route("/me", methods=['DELETE'])
@jwt_required()
def delete():
    user_id = int(get_jwt_identity())
    delete_user(user_id)
    return "", 204
