from database.db import get_connection

def db_login(email: str) -> dict:
    """Obtiene usuario por email con su contraseña hasheada.\n
    """
    with get_connection() as conn:
        with conn.cursor(dictionary=True) as cursor:
            query = "SELECT id, password FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            if not user:
                raise Exception("Usuario no encontrado")
            
    return user # type: ignore
    
def db_get_user(id: int) -> dict:
    """Obtener usuario.\n
    """
    with get_connection() as conn:
        with conn.cursor(dictionary=True) as cursor:
            query = "SELECT id, name, email, category, created_at, status FROM users WHERE id = %s"
            cursor.execute(query, (id, ))
            user = cursor.fetchone()
            
    if user is None:
        raise Exception("No se ha encontrado el usuario")
    
    return user # type: ignore

def db_create_user(name: str, email: str, password: str) -> int:
    """ Inserta un usuario.\n
    Devuelve el id del usuario creado 
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT email from users WHERE email = %s", (email, ))
            user = cursor.fetchone()
            if user is not None:
                raise Exception("El usuario ya existe")
            
            query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, email, password))
            conn.commit()
            id_user = cursor.lastrowid
    
    return id_user # type: ignore

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