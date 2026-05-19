"""Errores.\n
Administra Errores 4** y 5***.
"""
from flask import Blueprint

public_bp_error = Blueprint("public_errors", __name__, url_prefix="/public/errors")

