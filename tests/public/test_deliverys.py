import requests

URL = "http://127.0.0.1:15000/public/deliveries"
HEADERS = {
    'User-Agent': 'MOxxilla',
    'Content-Type': "application/json"
}
def get_admin_token() -> str:
    response = requests.post(
        url="http://127.0.0.1:15000/public/login/",
        json={"email": "admin@restaurant.com", "password": "admin1234"},
        headers=HEADERS
    )
    return response.json()["token"]

def test_create_cancelled_delivery():
    delivery = {
        "list_menus": [[1, 1], [2, 2]],
        "address": "adress_example",
        "date": "example",
    }
    token = get_admin_token()
    auth_headers = {**HEADERS, "Authorization": f"Bearer {token}"}

    response = requests.post(url=f"{URL}", json=delivery, headers=auth_headers)
    
    assert response.status_code == 201
    id_delivery = response.json()["id"]
    
    response = requests.get(url=f"{URL}/{id_delivery}", headers=auth_headers)
    
    assert response.status_code == 200
    content = response.json()
    assert content["address"] == delivery["address"]
    
    response = requests.delete(url=f"{URL}/{id_delivery}", headers=auth_headers)
    
    assert response.status_code == 204
    response = requests.get(url=f"{URL}/{id_delivery}", headers=auth_headers)
    assert response.json()["status"] == 'cancelled'
