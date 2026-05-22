import requests
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0',
    'Content-Type': "application/json"
}
URL = 'http://localhost:5000/public/orders'
# 200
def test_create_order():
    user_id = 2

    order = {
        "tables_menus": {
            1: [[1, 1], [2, 2], [3, 3]],
            2: [[1, 1], [2, 2], [3, 3]]
        }
    }
    response = requests.post(url=f"{URL}/{str(user_id)}", json=order, headers=HEADERS)
    assert response.status_code == 201
    
    # print(f"Status Code: {str(response.status_code)}")
    order_id = response.json()["id"]

    response = requests.delete(url=f"{URL}/{str(user_id)}/{str(order_id)}", headers=HEADERS)
   
    assert response.status_code == 200
