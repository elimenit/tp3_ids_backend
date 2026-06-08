import requests

URL = "http://127.0.0.1:5000/public/reviews"
HEADERS = {
    'User-Agent': 'test',
    'Content-Type': "application/json"
}

# Asumir que en la BD ya existe un usuario con id=2 y una reserva con id=1
USER_ID = 2
RESERVATION_ID = 1

def test_create_get_update_delete_review():
    # Crear reseña
    nueva_review = {
        "user_id": USER_ID,
        "reservation_id": RESERVATION_ID,
        "description": "Muy buena comida",
        "stars": 5
    }
    response = requests.post(url=f"{URL}/", json=nueva_review, headers=HEADERS)
    assert response.status_code == 201
    review_id = response.json()["id"]

    # Obtener la reseña creada
    response = requests.get(url=f"{URL}/{review_id}", headers=HEADERS)
    assert response.status_code == 200
    review = response.json()
    assert review["description"] == nueva_review["description"]
    assert review["stars"] == nueva_review["stars"]

    # Actualizar la reseña
    review_actualizada = {
        "user_id": USER_ID,
        "description": "Estuvo bien pero podria mejorar",
        "stars": 3
    }
    response = requests.put(url=f"{URL}/{review_id}", json=review_actualizada, headers=HEADERS)
    assert response.status_code == 200

    # Verificar que se actualizó
    response = requests.get(url=f"{URL}/{review_id}", headers=HEADERS)
    assert response.status_code == 200
    review = response.json()
    assert review["description"] == review_actualizada["description"]
    assert review["stars"] == review_actualizada["stars"]

    # Eliminar la reseña
    response = requests.delete(url=f"{URL}/{review_id}", json={"user_id": USER_ID}, headers=HEADERS)
    assert response.status_code == 200

    # Verificar que ya no existe
    response = requests.get(url=f"{URL}/{review_id}", headers=HEADERS)
    assert response.status_code == 404

def test_get_all_reviews():
    response = requests.get(url=f"{URL}/", headers=HEADERS)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_review_campos_invalidos():
    # Stars fuera de rango
    review_invalida = {
        "user_id": USER_ID,
        "reservation_id": RESERVATION_ID,
        "description": "Buena comida",
        "stars": 10
    }
    response = requests.post(url=f"{URL}/", json=review_invalida, headers=HEADERS)
    assert response.status_code == 400

def test_create_review_body_vacio():
    response = requests.post(url=f"{URL}/", json={}, headers=HEADERS)
    assert response.status_code == 400

def test_delete_review_ajena():
    # Crear reseña con USER_ID
    nueva_review = {
        "user_id": USER_ID,
        "reservation_id": RESERVATION_ID,
        "description": "Test reseña ajena",
        "stars": 4
    }
    response = requests.post(url=f"{URL}/", json=nueva_review, headers=HEADERS)
    assert response.status_code == 201
    review_id = response.json()["id"]

    # Intentar borrarla con otro user_id
    response = requests.delete(url=f"{URL}/{review_id}", json={"user_id": 9999}, headers=HEADERS)
    assert response.status_code == 404

    # Limpiar: borrar con el user correcto
    requests.delete(url=f"{URL}/{review_id}", json={"user_id": USER_ID}, headers=HEADERS)
