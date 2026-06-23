from database.db import get_connection


def db_get_all_extra_services() -> list:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM extra_services")
    services = cursor.fetchall()
    cursor.close()
    conn.close()
    return services


def db_get_active_extra_services() -> list:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM extra_services WHERE activo = TRUE")
    services = cursor.fetchall()
    cursor.close()
    conn.close()
    return services


def db_get_extra_service(service_id: int) -> dict | None:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM extra_services WHERE id = %s", (service_id,))
    service = cursor.fetchone()
    cursor.close()
    conn.close()
    return service


def db_create_extra_service(nombre: str, descripcion: str, activo: bool) -> int | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO extra_services (nombre, descripcion, activo) VALUES (%s, %s, %s)",
        (nombre, descripcion, activo)
    )
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return new_id


def db_update_extra_service(service_id: int, nombre: str, descripcion: str, activo: bool) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE extra_services SET nombre=%s, descripcion=%s, activo=%s WHERE id=%s",
        (nombre, descripcion, activo, service_id)
    )
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    return affected > 0


def db_delete_extra_service(service_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM extra_services WHERE id = %s", (service_id,))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    return affected > 0
