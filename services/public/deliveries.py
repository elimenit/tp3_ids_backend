"""
Lógica de negocio para los deliverys.\n
"""
def validation_create_delivery(list_menus_quantity: list[list[int, int]], addres: str, date: str):
    is_valide: bool = False
    if list_menus_quantity is None or addres is None or date is None:
        return is_valide

    is_validate = True
    return is_validate