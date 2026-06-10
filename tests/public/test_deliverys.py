import requests

URL = "http://127.0.0.1:15000/public/deliveries"
HEADERS = {
    'User-Agent': 'MOxxilla',
    'Content-Type': "application/json"
}
USER_ID = 2

def test_create_cancelled_delivery():
    delivery = {
        "list_menus": [[1, 1], [2, 2]],
        "address": "adress_example",
        "date": "example",
    }
    response = requests.post(url=f"{URL}/{USER_ID}", json=delivery, headers=HEADERS)
    
    assert response.status_code == 201
    id_delivery = response.json()["id"]
    
    response = requests.get(url=f"{URL}/{USER_ID}/{id_delivery}", headers=HEADERS)
    
    assert response.status_code == 200
    content = response.json()
    assert content["address"] == delivery["address"]
    
    response = requests.delete(url=f"{URL}/{USER_ID}/{id_delivery}", headers=HEADERS)
    
    assert response.status_code == 204
    response = requests.get(url=f"{URL}/{USER_ID}/{id_delivery}", headers=HEADERS)
    assert response.json()["status"] == 'cancelled'
