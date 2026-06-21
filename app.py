from datetime import timedelta

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from database.db import build_initial_database
from constants import SECRET_KEY, FLASK_HOST, FLASK_PORT

def create_app()-> Flask:
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

    CORS(app, resources={r"/*": {"origins": "*"}})
    JWTManager(app)
    
    from routers.login import public_bp_login
    from routers.public.menus import public_bp_menu
    from routers.public.reservations import public_bp_reservations
    from routers.public.users import public_bp_users
    from routers.public.reviews import public_bp_reviews
    from routers.admin.tables import admin_bp_tables
    from routers.admin.users import adm_bp_users
    from routers.admin.menus import adm_bp_menus
    from routers.admin.dashboards import adm_bp_dashboards
    from routers.admin.reservations import adm_bp_reservations
    
    app.register_blueprint(public_bp_login, url_prefix="/public/login")
    app.register_blueprint(admin_bp_tables, url_prefix="/admin/tables")
    app.register_blueprint(public_bp_menu, url_prefix="/public/menus")
    app.register_blueprint(public_bp_reservations, url_prefix="/public/reservations")
    app.register_blueprint(public_bp_users, url_prefix="/public/users")
    app.register_blueprint(public_bp_reviews, url_prefix="/public/reviews")
    app.register_blueprint(adm_bp_users, url_prefix="/admin/users")
    app.register_blueprint(adm_bp_dashboards, url_prefix="/admin/dashboards")
    app.register_blueprint(adm_bp_menus, url_prefix="/admin/menus")
    app.register_blueprint(adm_bp_reservations, url_prefix="/admin/reservations")
   
    # Errores
    @app.errorhandler(ValueError)
    def not_found(error):
        return jsonify({
            "message": "Error de usuario",
            "description": str(error)
        }), 400

    @app.errorhandler(Exception)
    def server_failed(error):
        return jsonify(
            {
                "message": "Error",
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
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=False) # type: ignore

if __name__ == '__main__':
    build_initial_database()
    main()   
