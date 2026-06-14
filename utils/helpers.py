from database.db import get_connection

from datetime import datetime, timedelta
from flask import request

def _execute_query(query: str, params: tuple = ()) -> list:
    """Ejecuta una query SELECT con los parámetros dados y retorna todos los resultados."""
    with get_connection() as conn:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()  # type: ignore

def _get_date_range() -> tuple[str, str]:
    """Obtiene inicio y fin de los query params. Defaultea a los últimos 3 meses. Utilizado en dashboards"""
    default_fin = datetime.now()
    default_inicio = default_fin - timedelta(days=90)

    inicio = request.args.get("inicio", default_inicio.strftime("%Y-%m-%d"))
    fin = request.args.get("fin", default_fin.strftime("%Y-%m-%d"))
    return inicio, fin

def build_update_query(table: str, allowed_fields: set, updates: dict, id_field: str = "id") -> tuple[str | None, tuple]:
    """
    Construye una query UPDATE dinámica a partir de un diccionario de campos.
    Solo incluye los campos presentes en allowed_fields.

    Devuelve (query, values) o (None, ()) si no hay campos válidos para actualizar.
    """
    safe_updates = {k: v for k, v in updates.items() if k in allowed_fields}

    if not safe_updates:
        return None, ()

    fields = [f"{key} = %s" for key in safe_updates]
    values = tuple(safe_updates.values())

    query = f"UPDATE {table} SET {', '.join(fields)} WHERE {id_field} = %s"
    print(query)
    return query, values