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
    }, headers=HEADERS, timeout=5)
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
    }, headers=HEADERS, timeout=5)
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
        r = requests.post(url=f"{URL}/public/tables/", json=mesa, headers=HEADERS, timeout=5)
        print(f"  Mesa {mesa['table_number']}: {r.status_code}")

def agregar_menus():
    menus = [
        {"category": "drinks",  "name": "Jugo",      "description": "Jugo de naranja",    "price": 1500, "image_url": "https://pasteleriasanantonio.com/carta-digital/wp-content/uploads/2024/09/lucuma.png"},
        {"category": "burgers", "name": "Hamburguesa",  "description": "hamburguesa completa",  "price": 15000, "image_url": "https://www.recetasnestle.com.ec/sites/default/files/srh_recipes/4e4293857c03d819e4ae51de1e86d66a.jpg"},
        {"category": "pasta",   "name": "Canelones", "description": "Canelones caseros", "price": 20000, "image_url": "www.miguelvergara.com/actualidad/wp-content/uploads/2024/01/canelones-de-carne-1200x860.jpg"},
    ]
    print("Agregando menús...")
    for menu in menus:
        r = requests.post(url=f"{URL}/admin/menus/", json=menu, headers=HEADERS, timeout=5)
        print(f"  Menú {menu['name']}: {r.status_code}")

def agregar_usuarios():
    usuarios = [
        {"name": "test",   "email": "test1@restaurant.com", "password": "pass1234"},
        {"name": "maria",  "email": "test2@restaurant.com", "password": "pass1234"},
        {"name": "carlos", "email": "test3@restaurant.com", "password": "pass1234"},
    ]
    print("Agregando usuarios...")
    for usuario in usuarios:
        r = requests.post(url=f"{URL}/public/users/", json=usuario, headers=HEADERS, timeout=5)
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
        r = requests.post(url=f"{URL}/public/login/", json={"email": datos["email"], "password": datos["password"]}, headers=headers_usuario, timeout=5)
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
        }, headers=headers_usuario, timeout=5)

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
        }, headers=headers_usuario, timeout=5)
        print(f"  Reseña ({datos['stars']}★) para {datos['email']}: {r.status_code}")

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

    print("=== Datos cargados correctamente ===")

if __name__ == '__main__':
    main()
