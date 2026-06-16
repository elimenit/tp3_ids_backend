from datetime import datetime

def validar_limit_offset(limit: int, offset: int):
    is_validate: bool = False
    if limit <= 10 and limit >= 0 and offset >= 0:
        is_validate = True
    return is_validate

def is_future_date(ndate: str) -> bool:
    dateformat = "%d/%m/%Y"
    fdate = datetime.strptime(ndate, dateformat).date()
    today = datetime.now().date()
    return fdate > today