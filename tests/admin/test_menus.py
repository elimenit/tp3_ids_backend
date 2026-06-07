import requests

URL = "http://127.0.0.1:5000/admin/menus"
HEADERS = {
    'User-Agent': 'test',
    'Content-Type': "application/json"
}

def test_create_get_update_delete_menu():
    # Crear plato
    nuevo_menu = {
        "category": "burgers",
        "name": "Hamburguesa test",
        "description": "Pan, carne y queso",
        "price": 1500,
        "image_url": "https://ejemplo.com/burger.jpg"
    }
    response = requests.post(url=f"{URL}/", json=nuevo_menu, headers=HEADERS)
    assert response.status_code == 201
    menu_id = response.json()["id"]

    # Obtener el plato creado
    response = requests.get(url=f"{URL}/{menu_id}", headers=HEADERS)
    assert response.status_code == 200
    menu = response.json()
    assert menu["name"] == nuevo_menu["name"]
    assert menu["price"] == nuevo_menu["price"]
    assert menu["available"] == True

    # Actualizar el plato
    menu_actualizado = {
        "category": "burgers",
        "name": "Hamburguesa test",
        "description": "Pan, carne, queso y bacon",
        "price": 1800,
        "available": True,
        "image_url": "https://ejemplo.com/burger_v2.jpg"
    }
    response = requests.put(url=f"{URL}/{menu_id}", json=menu_actualizado, headers=HEADERS)
    assert response.status_code == 200

    # Verificar que se actualizó
    response = requests.get(url=f"{URL}/{menu_id}", headers=HEADERS)
    assert response.status_code == 200
    menu = response.json()
    assert menu["price"] == menu_actualizado["price"]
    assert menu["description"] == menu_actualizado["description"]

    # Eliminar el plato
    response = requests.delete(url=f"{URL}/{menu_id}", headers=HEADERS)
    assert response.status_code == 200

    # Verificar que ya no existe
    response = requests.get(url=f"{URL}/{menu_id}", headers=HEADERS)
    assert response.status_code == 404

def test_list_menus():
    response = requests.get(url=f"{URL}/", headers=HEADERS)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_menu_campos_invalidos():
    # Categoría inválida
    menu_invalido = {
        "category": "pizza",
        "name": "Pizza test",
        "description": "Mozzarella",
        "price": 1200
    }
    response = requests.post(url=f"{URL}/", json=menu_invalido, headers=HEADERS)
    assert response.status_code == 400

def test_create_menu_precio_invalido():
    menu_invalido = {
        "category": "burgers",
        "name": "Burger precio invalido",
        "description": "Test",
        "price": -100
    }
    response = requests.post(url=f"{URL}/", json=menu_invalido, headers=HEADERS)
    assert response.status_code == 400

def test_create_menu_body_vacio():
    response = requests.post(url=f"{URL}/", json={}, headers=HEADERS)
    assert response.status_code == 400

def test_delete_menu_inexistente():
    response = requests.delete(url=f"{URL}/99999", headers=HEADERS)
    assert response.status_code == 404
