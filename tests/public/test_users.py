import requests

URL = "http://127.0.0.1:5000/public/users"
HEADERS = {
    'User-Agent': 'hhh',
    'Content-Type': "application/json"
}

def test_create_update_delete_user():
    user = {
        "name": "Jhon Doe",
        "email": "jhondoe@gmail.com",
        "password": "Password1234"
    }
    response = requests.post(url=f"{URL}", json=user, headers=HEADERS)
    
    assert response.status_code == 201
    id_user = response.json()["id"]
    update_user = {
        "name": "jhon",
        "password": "nueva_password"
    }
    response = requests.put(url=f"{URL}/{id_user}", json=update_user, headers=HEADERS)
    assert response.status_code == 204

    response = requests.get(url=f"{URL}/{id_user}", headers=HEADERS)
    assert response.status_code == 200
    
    get_user = response.json()
    assert get_user["name"] == update_user["name"]

    response = requests.delete(url=f"{URL}/{id_user}", headers=HEADERS)
    assert response.status_code == 200

