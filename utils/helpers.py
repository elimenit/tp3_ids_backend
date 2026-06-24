from datetime import datetime, timedelta
from flask import request

def _get_date_range() -> tuple[str, str]:
    """Obtiene inicio y fin de los query params. Defaultea a los últimos 3 meses. Utilizado en dashboards"""
    default_fin = datetime.now()
    default_inicio = default_fin - timedelta(days=90)

    inicio = request.args.get("inicio", default_inicio.strftime("%Y-%m-%d"))
    fin = request.args.get("fin", default_fin.strftime("%Y-%m-%d"))
    return inicio, fin