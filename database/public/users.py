from database.db import get_connection
from utils.helpers import build_update_query

from datetime import datetime

ALLOWED_FIELDS = {"name", "email", "category", "password"}

def db_get_user(id: int = 0, email: str = "") -> dict:
    """
    Obtiene un usuario por su id o por su email.
    Lanza ValueError si no se provee ningún criterio.
    Lanza Exception si no se encuentra el usuario.
    """
    if not id and not email:
        raise ValueError("Se requiere id o email para buscar un usuario")

    with get_connection() as conn:
        with conn.cursor(dictionary=True) as cursor:
            if id > 0:
                query = "SELECT id, name, email, category, created_at, status FROM users WHERE id = %s"
                cursor.execute(query, (id,))
            else:
                query = "SELECT id, name, email, category, created_at, status FROM users WHERE email = %s"
                cursor.execute(query, (email,))
            user = cursor.fetchone()

    if user is None:
        raise Exception(f"No se ha encontrado el usuario con credencial {id if id > 0 else email}")

    return user  # type: ignore

def db_get_user_with_password(email: str) -> dict:
    with get_connection() as conn:
        with conn.cursor(dictionary=True) as cursor:
            query = "SELECT id, name, email, password, category, created_at, status FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()

    if user is None:
        raise Exception("Credenciales inválidas")

    return user  # type: ignore

def db_create_user(name: str, email: str, password: str, category: str = "normal") -> dict:
    """
    Crea el usuario en la base de datos y devuelve un diccionario con la información del usuario creado.
    Lanza Exception si el email ya existe.
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
            if cursor.fetchone() is not None:
                raise Exception("El usuario ya existe")

            query = "INSERT INTO users (name, email, password, category) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (name, email, password, category))
            conn.commit()
            id_user = cursor.lastrowid

    return {
        "id": id_user,
        "name": name,
        "email": email,
        "category": category,
        "created_at": datetime.now(),
        "status": "active"
    }


def db_update_user_flexible(id: int, updates: dict) -> None:
    """
    Actualiza un usuario con los campos especificados en el diccionario updates.
    Los campos permitidos están definidos en la constante ALLOWED_FIELS definida arriba
    """
    query, values = build_update_query("users", ALLOWED_FIELDS, updates)

    if not query:
        return

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, values + (id,))
            conn.commit()


def db_delete_user(id: int) -> None:
    """
    Realiza un soft delete del usuario, marcándolo como inactivo.
    Lanza Exception si el usuario no existe.
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM users WHERE id = %s", (id,))
            if not cursor.fetchone():
                raise Exception("Usuario no registrado")

            cursor.execute("UPDATE users SET status = 'inactive' WHERE id = %s", (id,))
            conn.commit()