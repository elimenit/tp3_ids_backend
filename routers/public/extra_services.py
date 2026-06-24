from flask import Blueprint, jsonify
from services.extra_services_service import get_active_services
from utils.error import error_response

public_bp_extra_services = Blueprint('public_extra_services', __name__)

@public_bp_extra_services.route('/', methods=['GET'])
def list_services():
    try:
        services = get_active_services()
    except Exception as e:
        return error_response('Error al obtener servicios extra', f'Error: {e}', 500)

    return jsonify(services), 200