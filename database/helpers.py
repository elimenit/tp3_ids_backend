from database.db import get_connection

def _execute_query(query: str, params: tuple = ()) -> list[dict]:
    """Ejecuta una query SELECT con los parámetros dados y retorna todos los resultados."""
    try:
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()  # type: ignore
    except Exception as e:
        print(f'error en select {e}')
        raise Exception('Ha ocurrido un error en el servidor. Inténtelo de nuevo más tarde.')

def _count_rows(table: str) -> int:
    """Devuelve la cantidad de registros que hay en la tabla insertada como parámetro"""
    query = "SELECT COUNT(*) FROM " + table
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchone()[0] # type: ignore
    except Exception as e:
        print(f'error en cuenta {e}')
        raise Exception('Ha ocurrido un error en el servidor. Inténtelo de nuevo más tarde.')

def _execute_update_query(query: str, params: tuple = (), return_lastrowid: bool = False) -> int:
    """Ejecuta una query que modifica la base de datos con los parámetros dados y retorna la cantidad de registros afectados.
    Acepta un parámetro opcional en caso de que se quiera recibir el ID del registro creado"""
    print(f"\n\nQUERY DEL UPDATE {query} {str(params)}\n\n")
    try:
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, params)
                result = cursor.rowcount if not return_lastrowid else cursor.lastrowid
                conn.commit()
                return result # type: ignore
    except Exception as e:
        print(f'error en update {e}')
        raise Exception('Ha ocurrido un error en el servidor. Inténtelo de nuevo más tarde.')
    
def build_update_query(table: str, allowed_fields: set, updates: dict, id_field: str = "id") -> tuple[str, tuple]:
    """
    Construye una query UPDATE dinámica a partir de un diccionario de campos.
    Solo incluye los campos presentes en allowed_fields.

    Devuelve (query, values) o (None, ()) si no hay campos válidos para actualizar.

    Ejemplo de updates: 
    - {'name': 'tiziano', 'password': 12345678, ...} 
    -> Las claves coinciden con el nombre de las columnas en la tabla
    -> Por eso recibe la variable allowed_fields, se chequea qué campos se pueden actualizar dentro de la tabla
    -> El orden de la tupla `values` es FUNDAMENTAL!
    """
    safe_updates = {k: v for k, v in updates.items() if k in allowed_fields}

    if not safe_updates:
        raise ValueError('Los campos a actualizar no coinciden con los nombrados en la tabla. Por favor, revíselos.')

    fields = [f"{key} = %s" for key in safe_updates]
    values = tuple(safe_updates.values())

    query = f"UPDATE {table} SET {', '.join(fields)} WHERE {id_field} = %s"
    print(query)
    return query, values