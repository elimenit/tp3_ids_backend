from utils.helpers import _execute_query, build_update_query
from database.db import get_connection

def db_list_users(limit: int = 10, offset: int = 0)-> list:
    return _execute_query("SELECT id, name, email, category, status FROM users LIMIT %s OFFSET %s", (limit, offset))

def db_count_users() -> int:
    result = _execute_query("SELECT COUNT(*) as cant FROM users")
    if not result:
        return 0
    return result[0]["cant"]

def db_admin_update_user(id: int, updates: dict) -> None:
    """
    Actualiza un usuario con los campos especificados (uso administrador).
    Permite actualizar name, email, category y password.
    """
    ALLOWED_FIELDS = {"name", "email", "category", "password"}
    query, values = build_update_query("users", ALLOWED_FIELDS, updates)

    if not query:
        return

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, values + (id,))
            conn.commit()


def db_toggle_user_status(id: int) -> str:
    """
    Alterna el estado del usuario entre 'active' e 'inactive'.
    Devuelve el nuevo estado.
    Lanza ValueError si el usuario no existe.
    """
    with get_connection() as conn:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT status FROM users WHERE id = %s", (id,))
            user = cursor.fetchone()
            if not user:
                raise ValueError("Usuario no registrado")

            new_status = "inactive" if user["status"] == "active" else "active"  # type: ignore
            cursor.execute("UPDATE users SET status = %s WHERE id = %s", (new_status, id))
            conn.commit()

    return new_status