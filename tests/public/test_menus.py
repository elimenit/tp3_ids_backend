import requests

URL = "http://127.0.0.1:15000/public/menus"
URL_ADMIN = "http://127.0.0.1:15000/admin/menus"
HEADERS = {
    'User-Agent': 'test',
    'Content-Type': "application/json"
}

def get_admin_token() -> str:
    response = requests.post(
        url="http://127.0.0.1:15000/public/login/",
        json={"email": "admin@restaurant.com", "password": "admin1234"},
        headers=HEADERS
    )
    return response.json()["token"]

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

def test_list_menus_solo_muestra_disponibles():
    response = requests.get(url=f"{URL}/", headers=HEADERS)
    assert response.status_code == 200
    for menu in response.json():
        assert "available" not in menu

def test_get_menu_existente():
    token = get_admin_token()
    auth_headers = {**HEADERS, "Authorization": f"Bearer {token}"}

    nuevo_menu = {
        "category": "pasta",
        "name": "Fideos test publico",
        "description": "Fideos con salsa",
        "price": 900,
        "image_url": None
    }
    response = requests.post(url=f"{URL_ADMIN}/", json=nuevo_menu, headers=auth_headers)
    assert response.status_code == 201
    menu_id = response.json()["id"]

    response = requests.get(url=f"{URL}/{menu_id}", headers=HEADERS)
    assert response.status_code == 200
    menu = response.json()
    assert menu["name"] == nuevo_menu["name"]
    assert menu["price"] == nuevo_menu["price"]

    requests.delete(url=f"{URL_ADMIN}/{menu_id}", headers=auth_headers)

def test_get_menu_inexistente():
    response = requests.get(url=f"{URL}/99999", headers=HEADERS)
    assert response.status_code == 404

def test_menu_desactivado_no_visible():
    token = get_admin_token()
    auth_headers = {**HEADERS, "Authorization": f"Bearer {token}"}

    nuevo_menu = {
        "category": "soup",
        "name": "Sopa test desactivada",
        "description": "Sopa de verduras",
        "price": 700,
        "image_url": None
    }
    response = requests.post(url=f"{URL_ADMIN}/", json=nuevo_menu, headers=auth_headers)
    assert response.status_code == 201
    menu_id = response.json()["id"]

    menu_desactivado = {
        "category": "soup",
        "name": "Sopa test desactivada",
        "description": "Sopa de verduras",
        "price": 700,
        "available": False,
        "image_url": None
    }
    requests.put(url=f"{URL_ADMIN}/{menu_id}", json=menu_desactivado, headers=auth_headers)

    response = requests.get(url=f"{URL}/{menu_id}", headers=HEADERS)
    assert response.status_code == 404

    requests.delete(url=f"{URL_ADMIN}/{menu_id}", headers=auth_headers)
