from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from database.public.reviews import (
    db_get_reviews, db_get_review, db_get_review_by_reservation, db_create_review, db_update_review, db_delete_review
)
from services.public.reviews import validation_create_review, validation_update_review, validation_limit_offset
from utils.auth import get_current_user
from utils.error import error_response

public_bp_reviews = Blueprint("public_reviews", __name__)

@public_bp_reviews.route("/", methods=["GET"])
def get_all_reviews():
    limit = request.args.get("_limit", 10, type=int)
    offset = request.args.get("_offset", 0, type=int)

    if not validation_limit_offset(limit, offset):
        return error_response("Parámetros inválidos", "El límite debe estar entre 0 y 10, y el offset debe ser mayor o igual a 0", 400)

    try:
        reviews = db_get_reviews(limit, offset)
    except Exception as e:
        return error_response("Error al obtener reseñas", f"Error: {e}", 500)
    return jsonify(reviews), 200

@public_bp_reviews.route("/<int:review_id>", methods=["GET"])
def get_review(review_id: int):
    try:
        review = db_get_review(review_id)
    except Exception as e:
        return error_response("Error al obtener la reseña", f"Error: {e}", 500)

    if review is None:
        return error_response("Reseña no encontrada", f"No existe la reseña con id {review_id}", 404)

    return jsonify(review), 200

@public_bp_reviews.route("/", methods=["POST"])
@jwt_required()
def create_review():
    user = get_current_user()
    body = request.get_json()

    if not body:
        return error_response("Body inválido", "El body está vacío", 400)

    reservation_id = body.get("reservation_id")
    description = body.get("description")
    stars = body.get("stars")

    if not validation_create_review(reservation_id, description, stars):
        return error_response("Campos inválidos", "Revisá que todos los campos sean correctos y que las estrellas estén entre 1 y 5", 400)

    if db_get_review_by_reservation(user["id"], reservation_id):
        return error_response("Reseña duplicada", "Ya existe una reseña para esta reserva", 409)

    try:
        new_id = db_create_review(user["id"], reservation_id, description, stars)
    except Exception as e:
        return error_response("Error al crear la reseña", f"Error: {e}", 500)

    return jsonify({"id": new_id}), 201

@public_bp_reviews.route("/<int:review_id>", methods=["PUT"])
@jwt_required()
def update_review(review_id: int):
    user = get_current_user()
    body = request.get_json()

    if not body:
        return error_response("Body inválido", "El body está vacío", 400)

    description = body.get("description")
    stars = body.get("stars")

    if not validation_update_review(description, stars):
        return error_response("Campos inválidos", "Revisá la descripción y que las estrellas estén entre 1 y 5", 400)

    try:
        updated = db_update_review(review_id, user["id"], description, stars)
    except Exception as e:
        return error_response("Error al actualizar la reseña", f"Error: {e}", 500)

    if not updated:
        return error_response("No se pudo actualizar", "La reseña no existe o no te pertenece", 404)

    return jsonify({"mensaje": "Reseña actualizada correctamente"}), 200

@public_bp_reviews.route("/<int:review_id>", methods=["DELETE"])
@jwt_required()
def delete_review(review_id: int):
    user = get_current_user()

    try:
        deleted = db_delete_review(review_id, user["id"])
    except Exception as e:
        return error_response("Error al eliminar la reseña", f"Error: {e}", 500)

    if not deleted:
        return error_response("No se pudo eliminar", "La reseña no existe o no te pertenece", 404)

    return jsonify({"mensaje": "Reseña eliminada correctamente"}), 200
