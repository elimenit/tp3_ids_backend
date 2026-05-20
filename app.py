from flask import Flask, jsonify
from flask_cors import CORS
from database.db import build_initial_database

def create_app():
    app = Flask(__name__)

    # 1. Configuraciones Globales
    app.config['JSON_AS_ASCII'] = False  # Para manejar tildes y Ñ en JSON
    app.config['SECRET_KEY'] = 'tu_llave_secreta_muy_segura' # Cambiar por variable de entorno

    # 2. Administrar CORS
    # Permite peticiones desde cualquier origen (puedes restringirlo en producción)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # 3. Inicialización de la Base de Datos
    # Esto asegura que las tablas existan antes de que entre la primera petición
    with app.app_context():
        try:
            build_initial_database()
            print("✔ Base de datos verificada/inicializada.")
        except Exception as e:
            print(f"✘ Error inicializando la base de datos: {e}")

    # 4. Registro de Rutas
    from routers.login import public_bp_login
    from routers.public.deliverys import public_bp_delivery
    from routers.public.payments import public_bp_payment
    from routers.public.menus import public_bp_menu
    from routers.public.orders import public_bp_orders
    from routers.public.reservations import public_bp_reservations
    from routers.public.users import public_bp_users
    from routers.admin.users import adm_bp_users
    from routers.admin.dashboards import adm_bp_dashboards
    
    app.register_blueprint(public_bp_delivery, url_prefix="/public/delivery")
    app.register_blueprint(public_bp_payment, url_prefix="/public/payments")
    app.register_blueprint(public_bp_login, url_prefix="/public/login")
    app.register_blueprint(public_bp_menu, url_prefix="/public/menu")
    app.register_blueprint(public_bp_orders, url_prefix="/public/orders")
    app.register_blueprint(public_bp_reservations, url_prefix="/public/reservations")
    app.register_blueprint(public_bp_users, url_prefix="/public/users")
    app.register_blueprint(adm_bp_users, url_prefix="/admin/users")
    app.register_blueprint(adm_bp_dashboards, url_prefix="/admin/dashboard")
    
    # Errores
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "message": "Page not found",
            "error": f"{error}"
        }), 404

    @app.errorhandler(Exception)
    def server_failed(error):
        return jsonify(
            {
                "message": "Server Failed",
                "error": f"{error}"
            }
        )

    @app.route("/", methods=["GET"])
    def index():
        return {
            "status": "online",
            "message": "Restaurant API Backend Corriendo",
            "version": "1.0.0"
        }

    return app

if __name__ == '__main__':
    app = create_app()
    # Usar debug=True solo en desarrollo
    app.run(host="0.0.0.0", port=5000, debug=True)