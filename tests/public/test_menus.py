import requests

URL = "http://127.0.0.1:5000/public/menu"
URL_ADMIN = "http://127.0.0.1:5000/admin/menus"
HEADERS = {
    'User-Agent': 'test',
    'Content-Type': "application/json"
}

def test_list_menus():
    response = requests.get(url=f"{URL}/", headers=HEADERS)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_list_menus_por_categoria():
    for category in ("drinks", "burgers", "pasta", "soup"):
        response = requests.get(url=f"{URL}/?category={category}", headers=HEADERS)
        assert response.status_code == 200
        menus = response.json()
        assert isinstance(menus, list)
        for menu in menus:
            assert menu["category"] == category

def test_get_menu_existente():
    # Crear un plato desde admin para asegurarnos que existe
    nuevo_menu = {
        "category": "pasta",
        "name": "Fideos test publico",
        "description": "Fideos con salsa",
        "price": 900,
        "image_url": None
    }
    response = requests.post(url=f"{URL_ADMIN}/", json=nuevo_menu, headers=HEADERS)
    assert response.status_code == 201
    menu_id = response.json()["id"]

    # Obtenerlo desde el endpoint público
    response = requests.get(url=f"{URL}/{menu_id}", headers=HEADERS)
    assert response.status_code == 200
    menu = response.json()
    assert menu["name"] == nuevo_menu["name"]
    assert menu["price"] == nuevo_menu["price"]

    # Limpiar
    requests.delete(url=f"{URL_ADMIN}/{menu_id}", headers=HEADERS)

def test_get_menu_inexistente():
    response = requests.get(url=f"{URL}/99999", headers=HEADERS)
    assert response.status_code == 404

def test_menu_desactivado_no_visible():
    # Crear plato
    nuevo_menu = {
        "category": "soup",
        "name": "Sopa test desactivada",
        "description": "Sopa de verduras",
        "price": 700,
        "image_url": None
    }
    response = requests.post(url=f"{URL_ADMIN}/", json=nuevo_menu, headers=HEADERS)
    assert response.status_code == 201
    menu_id = response.json()["id"]

    # Desactivarlo desde admin
    menu_desactivado = {
        "category": "soup",
        "name": "Sopa test desactivada",
        "description": "Sopa de verduras",
        "price": 700,
        "available": False,
        "image_url": None
    }
    requests.put(url=f"{URL_ADMIN}/{menu_id}", json=menu_desactivado, headers=HEADERS)

    # Verificar que el público no lo ve
    response = requests.get(url=f"{URL}/{menu_id}", headers=HEADERS)
    assert response.status_code == 404

    # Limpiar
    requests.delete(url=f"{URL_ADMIN}/{menu_id}", headers=HEADERS)
