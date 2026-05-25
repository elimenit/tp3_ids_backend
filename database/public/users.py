from database.db import get_connection

def db_get_user(id: int)-> dict | None:
    """Obtener usuario.\n
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT id, name, email, category, created_at FROM users WHERE id = %s"
    cursor.execute(query, (id, ))
    user = cursor.fetchone()

    cursor.close()
    conn.close()
    return user

def db_get_user_email(email: str, password: str)-> dict | None:
    """Obtener usuario.\n
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT id, name, category, created_at FROM users WHERE email = %s AND password = %s;"
    cursor.execute(query, (email, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return user

def db_create_user(name: str, email: str, password: str)-> None | int:
    """ Inserta un usuario.\n
    Devuelve el id del usuario creado 
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT email from users WHERE email = %s", (email, ))
    user = cursor.fetchone()
    if user:
        cursor.close()
        conn.close()
        return None

    query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, email, password))
    conn.commit()

    id_user = cursor.lastrowid
    cursor.close()
    conn.close()
    return id_user

def db_update_user(id: int, name: str, password: str)-> int | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM users WHERE id =%s;", (id, ))
    email = cursor.fetchone()
    if email is None:
        return None
    query = """
    UPDATE users
    SET name = %s, password = %s
    WHERE id = %s;
    """
    cursor.execute(query, (name, password, id))
    conn.commit()
    cursor.close()
    conn.close()
    return id

def db_delete_user(id: int)-> str | None:
    """
    Elimina un usuario por su id.\n
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT email FROM users WHERE id = %s", (id, ))
    email = cursor.fetchone()

    if not email:
        cursor.close()
        conn.close()
        return None

    query = "DELETE FROM users WHERE id = %s"
    cursor.execute(query, (id,))
    conn.commit()
    
    cursor.close()
    conn.close()
    return email