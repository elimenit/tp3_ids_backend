from mysql.connector import Error

from database.public.extra_services import (
    db_create_extra_service,
    db_delete_extra_service,
    db_get_active_extra_services,
    db_get_all_extra_services,
    db_get_extra_service,
    db_update_extra_service
)

class ExtraServicesService:
    def get_all_services(self):
        try:
            return db_get_all_extra_services()
        except Error as e:
            print(f"Error al obtener servicios: {e}")
            return []

    def get_active_services(self):
        try:
            return db_get_active_extra_services()
        except Error as e:
            print(f"Error al obtener servicios activos: {e}")
            return []

    def get_service_by_id(self, service_id):
        try:
            return db_get_extra_service(service_id)
        except Error as e:
            print(f"Error al obtener servicio: {e}")
            return None

    def create_service(self, data):
        try:
            nombre = data.get('nombre')
            descripcion = data.get('descripcion', '')
            activo = data.get('activo', True)

            if not nombre:
                return False

            new_id = db_create_extra_service(nombre, descripcion, activo)
            return new_id is not None
        except Error as e:
            print(f"Error al crear servicio: {e}")
            return False

    def update_service(self, service_id, data):
        try:
            nombre = data.get('nombre')
            descripcion = data.get('descripcion')
            activo = data.get('activo')

            return db_update_extra_service(service_id, nombre, descripcion, activo)
        except Error as e:
            print(f"Error al actualizar servicio: {e}")
            return False

    def delete_service(self, service_id):
        try:
            return db_delete_extra_service(service_id)
        except Error as e:
            print(f"Error al eliminar servicio: {e}")
            return False
