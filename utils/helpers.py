from database.db import get_connection
from database.public.users import db_get_user

from datetime import datetime, timedelta
from flask import request

def _execute_query(query: str, params: tuple) -> list:
    """Ejecuta una query con los parámetros dados y retorna todos los resultados."""
    with get_connection() as conn:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()  # type: ignore
        
def _is_admin(user_id: int) -> bool:
    """Verifica que el usuario sea administrador."""
    user = db_get_user(user_id)
    return user["category"] in ("admin", "root")

def _get_date_range() -> tuple[str, str]:
    """Obtiene inicio y fin de los query params. Defaultea a los últimos 3 meses. Utilizado en dashboards"""
    default_fin = datetime.now()
    default_inicio = default_fin - timedelta(days=90)

    inicio = request.args.get("inicio", default_inicio.strftime("%Y-%m-%d"))
    fin = request.args.get("fin", default_fin.strftime("%Y-%m-%d"))

    return inicio, fin
