from database.db import get_connection

def db_list_users(limit: int = 10, offset: int = 0)-> list:
    conn = get_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM users LIMIT %s OFFSET %s"
    cursor.execute(query, (limit, offset))
    users = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return users