import requests

URL = "http://127.0.0.1:15000/admin/menus"
URL_LOGIN = "http://127.0.0.1:15000/public/login/"
HEADERS = {
    'User-Agent': 'test',
    'Content-Type': "application/json"
}

def get_admin_token() -> str:
    response = requests.post(
        url=URL_LOGIN,
        json={"email": "admin@restaurant.com", "password": "admin1234"},
        headers=HEADERS
    )
    return response.json()["token"]

def get_auth_headers() -> dict:
    token = get_admin_token()
    return {**HEADERS, "Authorization": f"Bearer {token}"}

def test_sin_token_devuelve_401():
    response = requests.get(url=f"{URL}/", headers=HEADERS)
    assert response.status_code == 401

def test_list_menus():
    response = requests.get(url=f"{URL}/", headers=get_auth_headers())
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_list_menus_incluye_campo_available():
    response = requests.get(url=f"{URL}/", headers=get_auth_headers())
    assert response.status_code == 200
    menus = response.json()
    if menus:
        assert "available" in menus[0]

def test_create_get_update_delete_menu():
    auth_headers = get_auth_headers()

    nuevo_menu = {
        "category": "burgers",
        "name": "Hamburguesa test",
        "description": "Pan, carne y queso",
        "price": 1500,
        "image_url": "https://ejemplo.com/burger.jpg"
    }
    response = requests.post(url=f"{URL}/", json=nuevo_menu, headers=auth_headers)
    assert response.status_code == 201
    menu_id = response.json()["id"]

    response = requests.get(url=f"{URL}/{menu_id}", headers=auth_headers)
    assert response.status_code == 200
    menu = response.json()
    assert menu["name"] == nuevo_menu["name"]
    assert menu["price"] == nuevo_menu["price"]
    assert menu["available"] == True

    menu_actualizado = {
        "category": "burgers",
        "name": "Hamburguesa test",
        "description": "Pan, carne, queso y bacon",
        "price": 1800,
        "available": True,
        "image_url": "https://ejemplo.com/burger_v2.jpg"
    }
    response = requests.put(url=f"{URL}/{menu_id}", json=menu_actualizado, headers=auth_headers)
    assert response.status_code == 200

    response = requests.get(url=f"{URL}/{menu_id}", headers=auth_headers)
    assert response.status_code == 200
    menu = response.json()
    assert menu["price"] == menu_actualizado["price"]
    assert menu["description"] == menu_actualizado["description"]

    response = requests.delete(url=f"{URL}/{menu_id}", headers=auth_headers)
    assert response.status_code == 200

    response = requests.get(url=f"{URL}/{menu_id}", headers=auth_headers)
    assert response.status_code == 404

def test_create_menu_precio_invalido():
    menu_invalido = {
        "category": "burgers",
        "name": "Burger precio invalido",
        "description": "Test",
        "price": -100
    }
    response = requests.post(url=f"{URL}/", json=menu_invalido, headers=get_auth_headers())
    assert response.status_code == 400

def test_create_menu_body_vacio():
    response = requests.post(url=f"{URL}/", json={}, headers=get_auth_headers())
    assert response.status_code == 400

def test_delete_menu_inexistente():
    response = requests.delete(url=f"{URL}/99999", headers=get_auth_headers())
    assert response.status_code == 404

def test_get_menu_inexistente():
    response = requests.get(url=f"{URL}/99999", headers=get_auth_headers())
    assert response.status_code == 404
