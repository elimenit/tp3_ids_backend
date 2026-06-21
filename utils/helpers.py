from database.db import get_connection

from datetime import datetime, timedelta
from flask import request

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

def _execute_update_query(query: str, params: tuple = ()) -> list[dict]:
    """Ejecuta una query que modifica la base de datos con los parámetros dados y retorna la cantidad de registros afectados."""
    print(f"\n\nQUERY DEL UPDATE {query} {str(params)}\n\n")
    try:
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, params)
                rows_af = cursor.rowcount 
                conn.commit()
                return rows_af # type: ignore
    except Exception as e:
        print(f'error en update {e}')
        raise Exception('Ha ocurrido un error en el servidor. Inténtelo de nuevo más tarde.')

def _get_date_range() -> tuple[str, str]:
    """Obtiene inicio y fin de los query params. Defaultea a los últimos 3 meses. Utilizado en dashboards"""
    default_fin = datetime.now()
    default_inicio = default_fin - timedelta(days=90)

    inicio = request.args.get("inicio", default_inicio.strftime("%Y-%m-%d"))
    fin = request.args.get("fin", default_fin.strftime("%Y-%m-%d"))
    return inicio, fin

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