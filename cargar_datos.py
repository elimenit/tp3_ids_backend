import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Content-Type": "application/json",
    "Dnt": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Priority": "u=0, i",
}
URL = "http://localhost:15000"

def crear_usuario():
    user = {
        "name": 'admin',
        "email": "admin@restaurant.com",
        "password": "restaurant"
    }
    r = requests.post(url=f"{URL}/public/users/", json=user, headers=HEADERS, timeout=5)
    print(r.content)
    assert r.status_code == 201
    HEADERS["Authorization"] = f"Bearer {r.json()['token']}"
    return r.json()["token"]

def crear_deliveries():
    delivery = {
        "list_menus": [[1, 1], [2, 2]],
        "address": "adress_example",
        "date": "example"
    }
    r = requests.post(url=f"{URL}/public/deliveries/", json=delivery, headers=HEADERS, timeout=5)
    print(r.content)
    assert r.status_code == 201

def agregar_mesas():
    mesas = [(1, 4, 'available', 0), (2, 4, 'available', 0), (3, 6, 'available', 10), (4, 10, 'available', 100)]
    model_request = {}
    print("Agegando mesas")
    for mesa in mesas:
        model_request["table_number"] = mesa[0]
        model_request["capacity"] = mesa[1]
        model_request["status"] = mesa[2]
        model_request["price"] = mesa[3]
        r = requests.post(url=f"{URL}/public/tables", headers=HEADERS, json=model_request, timeout=5)
        print(r.content)
        assert r.status_code == 201

def agregar_menus():
    menus = [('drinks', 'jugo', 'pera', 15, 1), ('burgers', 'sandwich', 'ss', 15, 1), ('pasta', 'canelones', 'pera', 15, 1)]
    model_menu = {
        "name": "",
        "category": "",
        "description": "",
        "price": "",
        "available": ""
    }
    print("agregando menus")
    for menu in menus:
        model_menu["category"] = menu[0]
        model_menu["name"] = menu[1]
        model_menu["description"] = menu[2]
        model_menu["price"] = menu[3]
        model_menu["available"] = menu[4]

        r = requests.post(url=f"{URL}/public/menus", json=model_menu, headers=HEADERS, timeout=5)
        print(r.content)
        assert r.status_code == 201

def test_main():
    token: str = crear_usuario()
    agregar_mesas()
    agregar_menus()
    crear_deliveries()

if __name__ == '__main__':
    test_main()
    