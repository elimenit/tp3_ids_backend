"""Validacion de los Orders
"""

def validation_limit_offset(limit, offset)-> bool:
    is_validate: bool = False
    
    if limit >= 0 and limit <= 10 and offset >= 0:
        is_validate = True
    
    return is_validate