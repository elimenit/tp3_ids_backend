import bcrypt
from database.public.users import db_create_user, db_login

def validation_creation(name: str, email: str, password: str)-> bool:
    is_validate: bool = False
    if name and email and password:
        if '@' in email and email.count('@') == 1:
            if len(email[email.index('@'):]) >=2:
                if password.isalnum():
                    is_validate = True

    return is_validate

def validation_id_user(id: int)-> bool:
    is_validate: bool = False
    if isinstance(id, (int)):
        if id > 0:
            is_validate = True
    return is_validate

def create_user(name: str, email: str, password: str) -> int:
    """
    Crea un usuario en la base de datos con contraseña hasheada.
    
    Args:
        name (str): Nombre del usuario
        email (str): Email del usuario
        password (str): Contraseña en texto plano
    
    Returns:
        int: ID del usuario creado
    
    Raises:
        Exception: Si la validación falla o hay error en la base de datos
    """
    name = name.strip().lower()
    email = email.strip().lower()
    password = password.strip()
    # Validar datos
    if not validation_creation(name, email, password):
        raise ValueError("Datos inválidos")
    
    # Hashear contraseña
    password_bytes = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    hashed_password_str = hashed_password.decode('utf-8')
    
    # Crear usuario en la base de datos
    user_id = db_create_user(name, email, hashed_password_str)
    
    return user_id

def login_user(email: str, password: str) -> int:
    """
    Verifica las credenciales del usuario y retorna su ID.
    
    Args:
        email (str): Email del usuario
        password (str): Contraseña en texto plano
    
    Returns:
        int: ID del usuario
    
    Raises:
        Exception: Si las credenciales son inválidas o el usuario no existe
    """
    email = email.strip().lower()
    password = password.strip()
    
    # Obtener usuario con hash de contraseña
    user = db_login(email)
    
    # Verificar contraseña con bcrypt
    password_bytes = password.encode('utf-8')
    hashed_password_bytes = user['password'].encode('utf-8')
    
    if not bcrypt.checkpw(password_bytes, hashed_password_bytes):
        raise ValueError("Credenciales inválidas")
    
    return user['id']
