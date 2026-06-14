from database.admin.users import db_list_users, db_count_users, db_admin_update_user, db_toggle_user_status
from database.public.users import db_create_user
from services.public.users import hash_password, validate_email, validate_password, validate_user_id

ALLOWED_CATEGORIES = {"normal", "client", "employee", "admin", "root", "system"}

def validar_limit_offset(limit: int, offset: int):
    is_validate: bool = False
    if limit <= 10 and limit >= 0 and offset >= 0:
        is_validate = True
    return is_validate

def validate_category(category: str):
    """Valida que la categoría sea una de las permitidas. Lanza ValueError si no lo es."""
    if category not in ALLOWED_CATEGORIES:
        raise ValueError("Categoría inválida")

def get_all_users(limit: int, offset: int) -> tuple[list[dict], int]:
    """Devuelve todos los usuarios en el rango especificado y la cuenta de todos los registros en la tabla usuarios"""
    if not validar_limit_offset(limit, offset):
        raise ValueError("Error en la selección de números para el paginado.")
    return db_list_users(limit, offset), db_count_users()

def create_user(name: str, email: str, password: str, category: str = "normal") -> dict:
    """Crea un nuevo usuario desde el panel administrador, con categoría asignable."""
    name = name.strip().lower()
    email = email.strip().lower()
    password = password.strip()
    category = category.strip().lower()

    validate_email(email)
    validate_password(password)
    validate_category(category)

    hashed_password = hash_password(password)
    return db_create_user(name, email, hashed_password, category)

def update_user(user_id: int, updates: dict) -> None:
    """Actualiza los datos de un usuario desde el panel administrador (name, email, category, password)."""
    validate_user_id(user_id)

    if not updates:
        raise ValueError("No hay campos para actualizar")

    processed_updates = {}

    if updates.get('name'):
        processed_updates['name'] = updates['name'].strip().lower()

    if updates.get('email'):
        email = updates['email'].strip().lower()
        validate_email(email)
        processed_updates['email'] = email

    if updates.get('category'):
        category = updates['category'].strip().lower()
        validate_category(category)
        processed_updates['category'] = category

    if updates.get('password'):
        password = updates['password'].strip()
        validate_password(password)
        processed_updates['password'] = hash_password(password)

    if not processed_updates:
        raise ValueError("No hay campos válidos para actualizar")

    db_admin_update_user(user_id, processed_updates)

def toggle_user_status(user_id: int) -> str:
    """Alterna el estado de un usuario entre activo e inactivo."""
    validate_user_id(user_id)
    return db_toggle_user_status(user_id)