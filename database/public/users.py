from database.db import get_connection

from datetime import datetime

def db_get_user(id: int = 0, email: str = "") -> dict:
    """
    Obtiene un usuario o bien por su id, o bien por su email
    """
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
    
    return user # type: ignore

def db_create_user(name: str, email: str, password: str, category: str = "normal") -> dict:
    """
    Crea el usuario en la base de datos y devuelve un diccionario con la información del usuario creado.
     - Si el email ya existe, lanza una excepción.
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT email from users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user is not None:
                raise Exception("El usuario ya existe")
            
            query = "INSERT INTO users (name, email, password, category) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (name, email, password, category))
            conn.commit()
            id_user = cursor.lastrowid
            
    user = {
        "id": id_user,
        "name": name,
        "email": email,
        "category": category,
        "created_at": datetime.now(),
        "status": "active"
    }
    
    return user 

def db_update_user(id: int, name: str, password: str)-> None:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            query = """
            UPDATE users
            SET name = %s, password = %s
            WHERE id = %s;
            """
            cursor.execute(query, (name, password, id))
            conn.commit()

def db_delete_user(id: int)-> bool:
    """
    Elimina un usuario por su id.\n
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT email FROM users WHERE id = %s", (id, ))
            email = cursor.fetchone()
            print(email)
            if not email:
                raise Exception("Usuario no registrado!")

            query = "UPDATE users SET status = 'inactive' WHERE id = %s"
            cursor.execute(query, (id,))
            conn.commit()
    
    return email # type: ignore