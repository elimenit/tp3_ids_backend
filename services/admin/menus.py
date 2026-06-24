from utils.validators import validar_limit_offset
from database.helpers import _count_rows
from database.admin.menus import db_list_menus

def validation_create_menu(category: str, name: str, description: str, price: float) -> bool:
    is_valid: bool = False
    if category is not None and name is not None and description is not None and price is not None:
        if isinstance(category, str) and category.strip() != '':
            if isinstance(name, str) and name.strip() != '':
                if isinstance(price, (int, float)) and price > 0:
                    is_valid = True
    return is_valid

def validation_update_menu(category: str, name: str, description: str, price: float, available: bool) -> bool:
    is_valid: bool = False
    if category is not None and name is not None and description is not None and price is not None and available is not None:
        if isinstance(category, str) and category.strip() != '':
            if isinstance(name, str) and name.strip() != '':
                if isinstance(price, (int, float)) and price > 0:
                    if isinstance(available, bool):
                        is_valid = True
    return is_valid

def get_all_menus(limit: int, offset: int) -> tuple[list[dict], int]:
    """Devuelve todos los productos en el rango especificado y la cuenta de todos los registros en la tabla 'menus'"""
    if not validar_limit_offset(limit, offset):
        raise ValueError("Error en la selección de números para el paginado.")
    return db_list_menus(limit, offset), _count_rows('menus')