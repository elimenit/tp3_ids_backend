from database.db import get_connection

def db_login(email: str, password: str):
    """Login de usuario.\n
    """
    conn = get_connection()
    if conn:
        with conn.cursor(dictionary=True) as cursor:
            query = "SELECT id FROM users WHERE email = %s AND password = %s"
            cursor.execute(query, (email, password))
            user = cursor.fetchone()
            if not user:
                raise Exception("Credenciales inválidas")
    else:
        raise Exception("Error de conexión a la base de datos")
    return user['id']

def db_get_user(id: int):
    """Obtener usuario.\n
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT id, name, email, category, created_at FROM users WHERE id = %s"
    cursor.execute(query, (id, ))
    user = cursor.fetchone()

    if user is None:
        cursor.close()
        conn.close()
        raise Exception("El usuario no existe")
    
    cursor.close()
    conn.close()
    
    return user

def db_create_user(name: str, email: str, password: str)-> None:
    """ Inserta un usuario.\n
    Devuelve el id del usuario creado 
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT email from users WHERE email = %s", (email, ))
    user = cursor.fetchone()
    if user is not None:
        cursor.close()
        conn.close()
        raise Exception("EL usuario ya existe")
    
    query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, email, password))
    conn.commit()

    id_user = cursor.lastrowid
    
    cursor.close()
    conn.close()
    return id_user

def db_update_user(id: int, name: str, password: str)-> None:
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    UPDATE users
    SET name = %s, password = %s
    WHERE id = %s;
    """
    cursor.execute(query, (name, password, id))
    conn.commit()
    cursor.close()
    conn.close()

def db_delete_user(id: int)-> bool:
    """
    Elimina un usuario por su id.\n
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT email FROM users WHERE id = %s", (id, ))
    email = cursor.fetchone()
    print(email)
    if not email:
        raise Exception("Usuario no registrado!")

    query = "DELETE FROM users WHERE id = %s"
    cursor.execute(query, (id,))
    conn.commit()
    
    cursor.close()
    conn.close()
    return email