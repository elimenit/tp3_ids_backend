from database.db import get_connection
from mysql.connector import Error

class ExtraServicesService:
    def get_all_services(self):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM extra_services")
            services = cursor.fetchall()
            cursor.close()
            conn.close()
            return services
        except Error as e:
            print(f"Error al obtener servicios: {e}")
            return []

    def get_service_by_id(self, service_id):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM extra_services WHERE id = %s", (service_id,))
            service = cursor.fetchone()
            cursor.close()
            conn.close()
            return service
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

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO extra_services (nombre, descripcion, activo) VALUES (%s, %s, %s)",
                (nombre, descripcion, activo)
            )
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Error as e:
            print(f"Error al crear servicio: {e}")
            return False

    def update_service(self, service_id, data):
        try:
            nombre = data.get('nombre')
            descripcion = data.get('descripcion')
            activo = data.get('activo')

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE extra_services SET nombre=%s, descripcion=%s, activo=%s WHERE id=%s",
                (nombre, descripcion, activo, service_id)
            )
            conn.commit()
            result = cursor.rowcount > 0
            cursor.close()
            conn.close()
            return result
        except Error as e:
            print(f"Error al actualizar servicio: {e}")
            return False

    def delete_service(self, service_id):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM extra_services WHERE id = %s", (service_id,))
            conn.commit()
            result = cursor.rowcount > 0
            cursor.close()
            conn.close()
            return result
        except Error as e:
            print(f"Error al eliminar servicio: {e}")
            return False
