from database.public.users import (
    db_create_user, db_get_user, db_update_user_flexible, db_delete_user, db_get_user_with_password
)

import bcrypt
import re
from flask_jwt_extended import create_access_token

def hash_password(password: str) -> str:
    """Hashea una contraseña usando bcrypt."""
    password_bytes = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed_password.decode('utf-8')


def verify_password_match(password: str, hashed_password: str):
    """Verifica una contraseña contra su hash. Lanza ValueError si no coincide."""
    password_bytes = password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    if not bcrypt.checkpw(password_bytes, hashed_password_bytes):
        raise ValueError("Contraseña inválida")


def validate_email(email: str):
    """Valida que el email tenga un formato válido. Lanza ValueError si no es válido."""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        raise ValueError("Formato de email inválido")


def validate_password(password: str, min_length: int = 8):
    """Valida que la contraseña tenga longitud mínima. Lanza ValueError si es muy corta."""
    if not password:
        raise ValueError("La contraseña es requerida")
    if len(password.strip()) < min_length:
        raise ValueError(f"La contraseña debe tener mínimo {min_length} caracteres")


def validate_user_id(user_id: int):
    """Valida que el ID de usuario sea un entero positivo. Lanza ValueError si no es válido."""
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("ID de usuario inválido")

def create_user(name: str, email: str, password: str) -> str:
    """
    Crea un nuevo usuario validando datos, hasheando contraseña y devolviendo token JWT.
    """
    name = name.strip().lower()
    email = email.strip().lower()
    password = password.strip()

    validate_email(email)
    validate_password(password)

    hashed_password_str = hash_password(password)
    user = db_create_user(name, email, hashed_password_str)
    
    return create_access_token(identity=str(user['id']))


def login_user(email: str, password: str) -> str:
    """
    Valida credenciales y devuelve token JWT.
    """
    email = email.strip().lower()
    password = password.strip()
    
    user = db_get_user_with_password(email=email)
    verify_password_match(password, user['password'])

    if user["status"] == "inactive":
        raise ValueError("El usuario está inactivo")
    
    return create_access_token(identity=str(user['id']))


def update_user_complete(user_id: int, name: str, password: str) -> str:
    """
    Reemplaza completamente los datos del usuario (nombre y contraseña).
    Valida todos los campos.

    Devuelve el token JWT actualizado con la nueva información del usuario.
    """
    validate_user_id(user_id)

    if not name or not password:
        raise ValueError("Para una actualización completa se requieren nombre y contraseña")

    name = name.strip().lower()
    password = password.strip()
    
    validate_password(password)
    
    hashed_password = hash_password(password)
    db_update_user_flexible(user_id, {
        "name": name,
        "password": hashed_password
    })
    
    user = db_get_user(id=user_id)

    return create_access_token(identity=str(user['id']))


def update_user_partial(user_id: int, updates: dict) -> str:
    """
    Actualiza parcialmente los datos del usuario.
    Valida solo los campos presentes en updates (name, password).

    Devuelve el token JWT actualizado con la nueva información del usuario.
    """
    validate_user_id(user_id)
    
    if not updates:
        raise ValueError("No hay campos para actualizar")
    
    processed_updates = {}
    
    if 'name' in updates:
        name = updates['name'].strip().lower()
        if name:
            processed_updates['name'] = name
    
    if 'password' in updates:
        password = updates['password'].strip()
        if password:
            validate_password(password)
            processed_updates['password'] = hash_password(password)
    
    if processed_updates:
        db_update_user_flexible(user_id, processed_updates)
    
    user = db_get_user(id=user_id)

    return create_access_token(identity=str(user['id']))


def obtain_user(user_id: int) -> dict:
    """
    Devuelve la información del usuario autenticado.
    """
    validate_user_id(user_id)

    user = db_get_user(id=user_id)

    if user["status"] == "inactive":
        raise ValueError("El usuario está inactivo")
    
    return user


def delete_user(user_id: int) -> None:
    """
    Elimina un usuario de la base de datos.
    """
    validate_user_id(user_id)
    
    db_delete_user(user_id)