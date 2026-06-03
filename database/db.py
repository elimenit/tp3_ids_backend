import mysql.connector
from mysql.connector import Error
from os import getenv
from dotenv import load_dotenv

load_dotenv()

# Configuración desde variables de entorno
DB_CONFIG = {
    "user": getenv("MYSQL_USER"),
    "password": getenv("MYSQL_PASSWORD"),
    "host": getenv("MYSQL_HOST"),
    "port": getenv("MYSQL_PORT", 3306)
}
NAME_DB = getenv("MYSQL_NAME_DB")

def build_initial_database() -> None:
    """
    Lee el archivo init.sql y ejecuta todas las sentencias 
    de forma segura.
    """
    query_except = ""
    conn = None
    try:
        print("*** Inizializando la Base de datos! ***")
        # 1. Conexión inicial (sin base de datos específica todavía)
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        with open(file="database/init.sql", mode='r', encoding='utf-8') as f:
            sql_script = f.read()
        
        for query in sql_script.split(';'):
            query = query.strip()
            query_except = query
            if query:
                cursor.execute(query)
                if query.lower().startswith('insert'):
                    conn.commit()
        
        print("|----> Base de datos inicializada con éxito <----|")

    except FileNotFoundError:
        print("Error: No se encontró el archivo 'database/init.sql'")
    except Error as e:
        print(f"Error de MySQL: {e} \n en la query: {query_except}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def get_connection():
    """
    Devuelve una conexión a la base de datos específica.
    """
    try:
        conn = mysql.connector.connect(
            **DB_CONFIG,
            database=NAME_DB
        )
    except Exception as e:
        raise Exception(f"Error en la conexión a la base de datos: {e}")
    return conn