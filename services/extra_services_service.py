from mysql.connector import Error

from database.public.extra_services import (
    db_create_extra_service,
    db_delete_extra_service,
    db_get_active_extra_services,
    db_get_all_extra_services,
    db_get_extra_service,
    db_update_extra_service
)


def get_all_services():
    try:
        return db_get_all_extra_services()
    except Error as e:
        return []


def get_active_services():
    try:
        return db_get_active_extra_services()
    except Error as e:
        return []


def get_service_by_id(service_id):
    try:
        return db_get_extra_service(service_id)
    except Error as e:
        return None


def create_service(data):
    try:
        nombre = data.get('nombre')
        descripcion = data.get('descripcion', '')
        activo = data.get('activo', True)

        if not nombre:
            return False

        new_id = db_create_extra_service(nombre, descripcion, activo)
        return new_id is not None
    except Error as e:
        return False


def update_service(service_id, data):
    try:
        nombre = data.get('nombre')
        descripcion = data.get('descripcion')
        activo = data.get('activo')

        return db_update_extra_service(service_id, nombre, descripcion, activo)
    except Error as e:
        return False


def delete_service(service_id):
    try:
        return db_delete_extra_service(service_id)
    except Error as e:
        return False