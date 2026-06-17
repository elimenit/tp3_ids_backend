import requests

URL = "http://localhost:15000"
HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "cargar_datos/1.0"
}

ADMIN_EMAIL = "admin@restaurant.com"
ADMIN_PASSWORD = "admin1234"

def registrar_admin():
    r = requests.post(url=f"{URL}/public/users/", json={
        "name": "admin",
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD
    }, headers=HEADERS)
    if r.status_code == 201:
        print("  Admin registrado")
    else:
        print(f"  Admin ya existe o error: {r.status_code}")

def promover_admin():
    from database.db import get_connection
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET category = 'admin' WHERE email = %s", (ADMIN_EMAIL,))
    conn.commit()
    cursor.close()
    conn.close()
    print("  Admin promovido a categoria 'admin'")

def login() -> str:
    r = requests.post(url=f"{URL}/public/login/", json={
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD
    }, headers=HEADERS)
    assert r.status_code == 200, f"Login fallido: {r.content}"
    token = r.json()["token"]
    HEADERS["Authorization"] = f"Bearer {token}"
    print("  Login exitoso")
    return token

def agregar_mesas():
    mesas = [
        {"table_number": 1, "capacity": 4, "status": "available", "price": 0},
        {"table_number": 2, "capacity": 4, "status": "available", "price": 0},
        {"table_number": 3, "capacity": 6, "status": "available", "price": 10},
        {"table_number": 4, "capacity": 10, "status": "available", "price": 100},
    ]
    print("Agregando mesas...")
    for mesa in mesas:
        r = requests.post(url=f"{URL}/public/tables/", json=mesa, headers=HEADERS)
        print(f"  Mesa {mesa['table_number']}: {r.status_code}")

def agregar_menus():
    menus = [
        {"category": "bebidas",      "name": "Jugo de naranja",     "description": "Jugo de naranja exprimido",          "price": 1500,  "image_url": "https://pasteleriasanantonio.com/carta-digital/wp-content/uploads/2024/09/lucuma.png"},
        {"category": "bebidas",      "name": "Pepsi",               "description": "Pepsi 500ml",                        "price": 2000,  "image_url": "https://www.pepsi.co.za/wp-content/uploads/2024/08/Pepsi-Original-500ml.png"},
        {"category": "hamburguesas", "name": "Hamburguesa clásica", "description": "Hamburguesa con lechuga y tomate",   "price": 15000, "image_url": "https://i.pinimg.com/736x/2c/25/3c/2c253c6c7fd3a4d4f54c7821aa931bbe.jpg"},
        {"category": "hamburguesas", "name": "Burger BBQ",          "description": "Burger con salsa BBQ y cheddar",     "price": 18000, "image_url": "https://tienda.customculinary.mx/cdn/shop/articles/burger-cheddar-baconn_copy.jpg?v=1673410421&width=3543"},
        {"category": "pastas",       "name": "Canelones caseros",   "description": "Canelones rellenos de carne",        "price": 20000, "image_url": "https://www.miguelvergara.com/actualidad/wp-content/uploads/2024/01/canelones-de-carne-1200x860.jpg"},
        {"category": "pastas",       "name": "Spaghetti bolognesa", "description": "Spaghetti con salsa de carne",       "price": 17000, "image_url": "https://cielitorosado.com/wp-content/uploads/2022/07/ESPAGUETIS-EN-SALSA-DE-CARNE-Y-SALCHICHITAS-sm.jpg"},
        {"category": "sopas",        "name": "Caldo de pollo",      "description": "Caldo casero con verduras y pollo",  "price": 7500,  "image_url": "https://static.bainet.es/clip/f8fb8a70-9b61-4a54-ab9c-b71f46493f12_source-aspect-ratio_1600w_0.jpg"},
        {"category": "postres",      "name": "Tiramisú",            "description": "Tiramisú tradicional italiano",      "price": 9000,  "image_url": "https://cdn.blog.paulinacocina.net/wp-content/uploads/2020/01/receta-de-tiramisu-facil-y-economico-1740483918.jpg"},
        {"category": "postres",      "name": "Brownie con helado",  "description": "Brownie de chocolate con helado",    "price": 10000, "image_url": "https://web-app-prod-01.nyc3.cdn.digitaloceanspaces.com/ryf_media/s6OkbzGRD8quFTZGdkSHTpoHpGoSSGtuHeTVY7OS.jpg"},
    ]
    print("Agregando menús...")
    for menu in menus:
        r = requests.post(url=f"{URL}/admin/menus/", json=menu, headers=HEADERS)
        print(f"  Menú {menu['name']}: {r.status_code}")

def agregar_usuarios():
    usuarios = [
        {"name": "test",   "email": "test1@restaurant.com", "password": "pass1234"},
        {"name": "maria",  "email": "test2@restaurant.com", "password": "pass1234"},
        {"name": "carlos", "email": "test3@restaurant.com", "password": "pass1234"},
    ]
    print("Agregando usuarios...")
    for usuario in usuarios:
        r = requests.post(url=f"{URL}/public/users/", json=usuario, headers=HEADERS)
        print(f"  Usuario {usuario['name']}: {r.status_code}")

def agregar_reservas_y_resenas():
    usuarios_resenas = [
        {"email": "test1@restaurant.com",  "password": "pass1234", "table_id": 1, "fecha": "2026-06-01", "hora": "20", "description": "Excelente atención y muy buena comida. Volveré sin dudas.", "stars": 5},
        {"email": "test2@restaurant.com",  "password": "pass1234", "table_id": 2, "fecha": "2026-06-03", "hora": "21", "description": "La comida estuvo bien pero esperaba algo mejor por el precio.", "stars": 3},
        {"email": "test3@restaurant.com",  "password": "pass1234", "table_id": 3, "fecha": "2026-06-05", "hora": "20", "description": "Buena experiencia en general, aunque el servicio tardó un poco.", "stars": 4},
    ]

    print("Agregando reservas y reseñas...")
    from database.db import get_connection

    for datos in usuarios_resenas:
        # Login con el usuario
        headers_usuario = {"Content-Type": "application/json"}
        r = requests.post(url=f"{URL}/public/login/", json={"email": datos["email"], "password": datos["password"]}, headers=headers_usuario)
        if r.status_code != 200:
            print(f"  Login fallido para {datos['email']}: {r.status_code}")
            continue
        token_usuario = r.json()["token"]
        headers_usuario["Authorization"] = f"Bearer {token_usuario}"

        # Crear reserva
        r = requests.post(url=f"{URL}/public/reservations/", json={
            "table_id": datos["table_id"],
            "fecha": datos["fecha"],
            "hora": datos["hora"]
        }, headers=headers_usuario)

        if r.status_code != 201:
            print(f"  Reserva fallida para {datos['email']}: {r.status_code} {r.content}")
            continue

        reserva_id = r.json()["reserva_id"]
        print(f"  Reserva creada (id={reserva_id}) para {datos['email']}")

        # Cambiar estado a Arrived directo en BD
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE reservations SET status_reservation = 'Arrived' WHERE id = %s", (reserva_id,))
        conn.commit()
        cursor.close()
        conn.close()

        # Crear reseña
        r = requests.post(url=f"{URL}/public/reviews/", json={
            "reservation_id": reserva_id,
            "description": datos["description"],
            "stars": datos["stars"]
        }, headers=headers_usuario)
        print(f"  Reseña ({datos['stars']}★) para {datos['email']}: {r.status_code}")

def probar_admin_reservaciones():
    print("Probando endpoints admin de reservaciones...")

    # Listar todas las reservas
    r = requests.get(url=f"{URL}/admin/reservations/", headers=HEADERS)
    print(f"  GET /admin/reservations/: {r.status_code}")
    if r.status_code != 200 or not r.json():
        print("  No hay reservas para probar el resto, salteando.")
        return

    reserva_id = r.json()[0]["id"]
    print(f"  Usando reserva id={reserva_id} para las pruebas")

    # Ver una reserva específica
    r = requests.get(url=f"{URL}/admin/reservations/{reserva_id}", headers=HEADERS)
    print(f"  GET /admin/reservations/{reserva_id}: {r.status_code}")

    # Cambiar estado a Confirmed
    r = requests.post(url=f"{URL}/admin/reservations/{reserva_id}/estado",
        json={"status_reservation": "Confirmed"}, headers=HEADERS)
    print(f"  POST estado=Confirmed: {r.status_code} — {r.json()}")

    # Cambiar estado a Arrived
    r = requests.post(url=f"{URL}/admin/reservations/{reserva_id}/estado",
        json={"status_reservation": "Arrived"}, headers=HEADERS)
    print(f"  POST estado=Arrived: {r.status_code} — {r.json()}")

    # Crear una reserva nueva para probar el DELETE
    headers_usuario = {"Content-Type": "application/json"}
    r = requests.post(url=f"{URL}/public/login/",
        json={"email": "test1@restaurant.com", "password": "pass1234"},
        headers=headers_usuario)
    if r.status_code == 200:
        headers_usuario["Authorization"] = f"Bearer {r.json()['token']}"
        r = requests.post(url=f"{URL}/public/reservations/",
            json={"table_id": 4, "fecha": "2026-12-01", "hora": "20"},
            headers=headers_usuario)
        if r.status_code == 201:
            nueva_id = r.json()["reserva_id"]
            r = requests.delete(url=f"{URL}/admin/reservations/{nueva_id}", headers=HEADERS)
            print(f"  DELETE /admin/reservations/{nueva_id}: {r.status_code} — {r.json()}")

def main():
    print("=== Cargando datos de prueba ===")

    print("Creando usuario admin...")
    registrar_admin()
    promover_admin()

    print("Logueando como admin...")
    login()

    agregar_mesas()
    agregar_menus()
    agregar_usuarios()
    agregar_reservas_y_resenas()
    probar_admin_reservaciones()

    print("=== Datos cargados correctamente ===")

if __name__ == '__main__':
    main()
