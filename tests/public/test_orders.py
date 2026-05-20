import requests
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0',
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