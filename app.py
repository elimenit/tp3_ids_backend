"""Aplicacion Principal.\n
Por Favor el el app.run(debug=False) 
ejecutenlo asi porque sino se ejecuta dos veces este archivo-> se ejecutan 2 veces las mismas querys en la Base de datos.
"""
from flask import Flask, jsonify
from flask_cors import CORS
from database.db import build_initial_database
# Blueprints
from routers.login import public_bp_login
from routers.public.deliveries import public_bp_delivery
from routers.public.menus import public_bp_menu
from routers.public.reservations import public_bp_reservations
from routers.public.users import public_bp_users
from routers.admin.users import adm_bp_users
from routers.admin.dashboards import adm_bp_dashboards

def create_app()-> Flask:
    # 1. Configuraciones Globales
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False  # Para manejar tildes y Ñ en JSON
    app.config['SECRET_KEY'] = 'tu_llave_secreta_muy_segura' # Cambiar por variable de entorno
    # 2. Administrar CORS
    # Permite peticiones desde cualquier origen (puedes restringirlo en producción)
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    app.register_blueprint(public_bp_delivery, url_prefix="/public/deliveries")
    app.register_blueprint(public_bp_login, url_prefix="/public/login")
    app.register_blueprint(public_bp_menu, url_prefix="/public/menu")
    app.register_blueprint(public_bp_reservations, url_prefix="/public/reservations")
    app.register_blueprint(public_bp_users, url_prefix="/public/users")
    app.register_blueprint(adm_bp_users, url_prefix="/admin/users")
    app.register_blueprint(adm_bp_dashboards, url_prefix="/admin/dashboard")
    
    # Errores
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "message": "Page not found",
            "description": f"{error}"
        }), 404

    @app.errorhandler(Exception)
    def server_failed(error):
        return jsonify(
            {
                "message": "Server Failed",
                "description": str(error)
            }
        ), 500

    @app.route("/", methods=["GET"])
    def index():
        return {
            "status": "online",
            "message": "Restaurant API Backend Corriendo",
            "version": "1.0.0"
        }
    return app

def main():
    app = Flask(__name__)
    app = create_app()
    app.run(host="localhost", port=5000, debug=False) # debug=True -> Llama dos veces las querys del archivo init.sql.

if __name__ == '__main__':
    build_initial_database()
    main()   
