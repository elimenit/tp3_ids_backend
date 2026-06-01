from database.public.users import db_create_user, db_get_user
from utils.error import error_response

import bcrypt
from flask_jwt_extended import create_access_token, get_jwt_identity
from flask import jsonify, Response

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

def create_user(name: str, email: str, password: str) -> str:
    """
    Recibe el nombre, email y contraseña de un nuevo usuario, 
    valida los datos, hashea la contraseña y crea el usuario en la base de datos.
    
    Devuelve un token JWT con la información del usuario creado.
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
    user = db_create_user(name, email, hashed_password_str)
    
    return create_access_token(identity=user)
    

def login_user(email: str, password: str) -> str:
    """
    Recibe el email y contraseña de un usuario, valida las credenciales, 
    y devuelve un token JWT con la información del usuario.
    """
    email = email.strip().lower()
    password = password.strip()
    
    # Obtener usuario con hash de contraseña
    user = db_get_user(email=email)
    
    # Verificar contraseña con bcrypt
    password_bytes = password.encode('utf-8')
    hashed_password_bytes = user['password'].encode('utf-8')
    
    if not bcrypt.checkpw(password_bytes, hashed_password_bytes):
        raise ValueError("Credenciales inválidas")
    
    return create_access_token(identity=user)

def obtain_user(user: dict) -> tuple[Response, int]:
    """
    Obtiene un Usuario. Utilizado principalmente para actualizar los datos del token de usuario en el frontend.
    
    Devuelve una Response con el token con los datos actualizados del usuario, y con el usuario
    """
    id: int = user.get("id", 0)
    if not id:
        return error_response(
            "Id Invalido",
            "Id del usuario fuera de rango",
            400
        )
    try:
        user = db_get_user(id)
    except Exception as e:
        return error_response(
            message="Error en la búsqueda de usuario", 
            description=str(e), 
            status_code=404
        )
    print(user)
    if user["status"] == "inactive":
        return error_response(
            message="Usuario inactivo", 
            description="El usuario se encuentra inactivo", 
            status_code=403
        )
    new_token = create_access_token(identity=user)  
    return jsonify({"token": new_token, "user": user}), 200

