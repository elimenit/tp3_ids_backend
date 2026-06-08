VALID_CATEGORIES = ('drinks', 'burgers', 'pasta', 'soup')

def validation_create_menu(category: str, name: str, description: str, price: float) -> bool:
    is_valid: bool = False
    if category is not None and name is not None and description is not None and price is not None:
        if isinstance(category, str) and category in VALID_CATEGORIES:
            if isinstance(name, str) and name.strip() != '':
                if isinstance(price, (int, float)) and price > 0:
                    is_valid = True
    return is_valid

def validation_update_menu(category: str, name: str, description: str, price: float, available: bool) -> bool:
    is_valid: bool = False
    if category is not None and name is not None and description is not None and price is not None and available is not None:
        if isinstance(category, str) and category in VALID_CATEGORIES:
            if isinstance(name, str) and name.strip() != '':
                if isinstance(price, (int, float)) and price > 0:
                    if isinstance(available, bool):
                        is_valid = True
    return is_valid
