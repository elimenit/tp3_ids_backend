import requests

URL = "http://127.0.0.1:15000/public/reviews"
URL_LOGIN = "http://127.0.0.1:15000/public/login/"
HEADERS = {
    'User-Agent': 'test',
    'Content-Type': "application/json"
}

# Reserva con id=1 ya existe en el seed (usuario test, mesa 1, status Arrived)
RESERVATION_ID = 1

def get_token(email: str, password: str) -> str:
    response = requests.post(url=URL_LOGIN, json={"email": email, "password": password}, headers=HEADERS)
    return response.json()["token"]

def get_user_headers() -> dict:
    token = get_token("admin@restaurant.com", "admin1234")
    return {**HEADERS, "Authorization": f"Bearer {token}"}

def test_get_all_reviews():
    response = requests.get(url=f"{URL}/", headers=HEADERS)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_review_inexistente():
    response = requests.get(url=f"{URL}/99999", headers=HEADERS)
    assert response.status_code == 404

def test_crear_review_sin_token_devuelve_401():
    nueva_review = {
        "reservation_id": RESERVATION_ID,
        "description": "Muy buena comida",
        "stars": 5
    }
    response = requests.post(url=f"{URL}/", json=nueva_review, headers=HEADERS)
    assert response.status_code == 401

def test_create_get_update_delete_review():
    auth_headers = get_user_headers()

    nueva_review = {
        "reservation_id": RESERVATION_ID,
        "description": "Muy buena comida",
        "stars": 5
    }
    response = requests.post(url=f"{URL}/", json=nueva_review, headers=auth_headers)
    assert response.status_code == 201
    review_id = response.json()["id"]

    response = requests.get(url=f"{URL}/{review_id}", headers=HEADERS)
    assert response.status_code == 200
    review = response.json()
    assert review["description"] == nueva_review["description"]
    assert review["stars"] == nueva_review["stars"]

    review_actualizada = {
        "description": "Estuvo bien pero podria mejorar",
        "stars": 3
    }
    response = requests.put(url=f"{URL}/{review_id}", json=review_actualizada, headers=auth_headers)
    assert response.status_code == 200

    response = requests.get(url=f"{URL}/{review_id}", headers=HEADERS)
    assert response.status_code == 200
    review = response.json()
    assert review["description"] == review_actualizada["description"]
    assert review["stars"] == review_actualizada["stars"]

    response = requests.delete(url=f"{URL}/{review_id}", headers=auth_headers)
    assert response.status_code == 200

    response = requests.get(url=f"{URL}/{review_id}", headers=HEADERS)
    assert response.status_code == 404

def test_create_review_campos_invalidos():
    auth_headers = get_user_headers()
    review_invalida = {
        "reservation_id": RESERVATION_ID,
        "description": "Buena comida",
        "stars": 10
    }
    response = requests.post(url=f"{URL}/", json=review_invalida, headers=auth_headers)
    assert response.status_code == 400

def test_create_review_body_vacio():
    auth_headers = get_user_headers()
    response = requests.post(url=f"{URL}/", json={}, headers=auth_headers)
    assert response.status_code == 400

def test_create_review_duplicada_devuelve_409():
    auth_headers = get_user_headers()

    nueva_review = {
        "reservation_id": RESERVATION_ID,
        "description": "Primera reseña",
        "stars": 5
    }
    response = requests.post(url=f"{URL}/", json=nueva_review, headers=auth_headers)
    assert response.status_code == 201
    review_id = response.json()["id"]

    # Intentar crear otra reseña para la misma reserva
    response = requests.post(url=f"{URL}/", json=nueva_review, headers=auth_headers)
    assert response.status_code == 409

    # Limpiar
    requests.delete(url=f"{URL}/{review_id}", headers=auth_headers)

def test_delete_review_ajena_devuelve_404():
    auth_headers = get_user_headers()

    nueva_review = {
        "reservation_id": RESERVATION_ID,
        "description": "Test reseña ajena",
        "stars": 4
    }
    response = requests.post(url=f"{URL}/", json=nueva_review, headers=auth_headers)
    assert response.status_code == 201
    review_id = response.json()["id"]

    # Registrar otro usuario e intentar borrar la reseña ajena
    otro_usuario = {
        "name": "otro test",
        "email": "otrotest_reviews@test.com",
        "password": "otropass123"
    }
    requests.post(url="http://127.0.0.1:15000/public/users/", json=otro_usuario, headers=HEADERS)
    otro_token = get_token("otrotest_reviews@test.com", "otropass123")
    otro_headers = {**HEADERS, "Authorization": f"Bearer {otro_token}"}

    response = requests.delete(url=f"{URL}/{review_id}", headers=otro_headers)
    assert response.status_code == 404

    # Limpiar
    requests.delete(url=f"{URL}/{review_id}", headers=auth_headers)
