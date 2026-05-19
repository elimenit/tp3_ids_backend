import requests
HEADERS = {
    'User-Agent': 'hhh',
    'Content-Type': "application/json"
}
URL = 'http://localhost:5000/public/orders'

def test_list_orders():
    response = requests.get(url=f"{URL}", headers=HEADERS)
    assert response.status_code == 200
    assert isinstance(response.json(), (list))

def test_create_order():
    order = {
        ""
    }
    #response = requests.post()