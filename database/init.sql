CREATE DATABASE IF NOT EXISTS restaurant;
USE restaurant;


CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL,
    category ENUM ('normal', 'client', 'employee', 'admin', 'root', 'system') DEFAULT 'normal',
    status ENUM ('active', 'inactive') DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE menus (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category ENUM ('drinks', 'burgers', 'pasta', 'soup'),
    name VARCHAR(100) UNIQUE NOT NULL,
    description VARCHAR(500),
    price DECIMAL(10,2) NOT NULL,
    available BOOLEAN DEFAULT TRUE,
    image_url VARCHAR(500)
);

CREATE TABLE restaurant_tables (
    id INT AUTO_INCREMENT PRIMARY KEY,
    table_number INT NOT NULL UNIQUE,
    capacity INT NOT NULL,
    status ENUM ('available', 'occupied', 'reserved'),
    price INT DEFAULT 0
);

CREATE TABLE reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    table_id INT,
    reservation_datetime DATETIME,
    status_reservation ENUM ('Pending', 'Confirmed', 'Cancelled', 'Arrived'),
    qr_token VARCHAR(100) UNIQUE,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (table_id) REFERENCES restaurant_tables(id)
);

CREATE TABLE reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    reservation_id INT NOT NULL,
    description VARCHAR(300) NOT NULL,
    stars INT NOT NULL CHECK (stars >= 1 AND stars <= 5),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (reservation_id) REFERENCES reservations(id) ON DELETE CASCADE
);

CREATE TABLE deliveries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    address VARCHAR(255) DEFAULT 'addres_example',
    delivery_datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM ('pending', 'transit', 'delivered', 'cancelled'),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE deliveries_menus (
    delivery_id INT,
    menu_id INT,
    quantity INT DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    qr_code INT DEFAULT 1,
    FOREIGN KEY (delivery_id) REFERENCES deliveries(id) ON DELETE CASCADE,
    FOREIGN KEY (menu_id) REFERENCES menus(id) ON DELETE CASCADE
);


-- id=1  admin@restaurant.com  / admin1234
-- id=2  test1@restaurant.com  / pass1234
-- id=3  test2@restaurant.com  / pass1234
-- id=4  test3@restaurant.com  / pass1234
INSERT INTO users (name, email, password, category)
VALUES
    ('admin',  'admin@restaurant.com', '$2b$12$tE5R1vw2LBQVs.9hCs0ZseTUl61JKmN2CoQsMOmUtV.R9BSii.Y46', 'admin'),
    ('test',   'test1@restaurant.com', '$2b$12$6Ry74/UngMeN1LFgqbxAvOLopKkTrt7vcdjw1.AsVHF3q5eCDycqa', 'normal'),
    ('maria',  'test2@restaurant.com', '$2b$12$6Ry74/UngMeN1LFgqbxAvOLopKkTrt7vcdjw1.AsVHF3q5eCDycqa', 'normal'),
    ('carlos', 'test3@restaurant.com', '$2b$12$CtDzCfxZnDA6fyfzb6MOpuy5kkNlQA5q7J2BIaTaAYTi.e8cpgfS.', 'normal');

INSERT INTO restaurant_tables (table_number, capacity, status, price)
VALUES (1, 4, 'available', 0), (2, 4, 'available', 0), (3, 6, 'available', 10), (4, 10, 'available', 100);

INSERT INTO menus (category, name, description, price, available)
VALUES ('drinks', 'jugo', 'pera', 15, 1), ('burgers', 'sandwich', 'ss', 15, 1), ('pasta', 'canelones', 'pera', 15, 1);


-- Reservas con status Arrived para poder crear reseñas
INSERT INTO reservations (user_id, table_id, reservation_datetime, status_reservation)
VALUES
    (2, 1, '2026-06-01 20:00:00', 'Arrived'),
    (3, 2, '2026-06-03 21:00:00', 'Arrived'),
    (4, 3, '2026-06-05 20:30:00', 'Arrived');


INSERT INTO reviews (user_id, reservation_id, description, stars)
VALUES
    (2, 1, 'Excelente atención y muy buena comida. Volveré sin dudas.', 5),
    (3, 2, 'La comida estuvo bien pero esperaba algo mejor por el precio.', 3),
    (4, 3, 'Buena experiencia en general, aunque el servicio tardó un poco.', 4);


INSERT INTO deliveries (user_id, address, status)
VALUES (2, 'direccion', 'pending'), (2, 'otra_address', 'pending');

INSERT INTO deliveries_menus (delivery_id, menu_id, quantity, qr_code)
VALUES (1, 1, 2, 1), (1, 2, 1, 1), (2, 3, 10, 1);
