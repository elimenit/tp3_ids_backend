CREATE DATABASE IF NOT EXISTS restaurant;
USE restaurant;


CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL,
    category ENUM ('normal', 'client', 'employee', 'admin', 'root', 'system') DEFAULT 'normal', 
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP 
);

CREATE TABLE menus (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category ENUM ('drinks', 'burgers', 'pasta', 'soup'),
    name VARCHAR(100) UNIQUE NOT NULL,
    description VARCHAR(500),
    price DECIMAL(10,2) NOT NULL,
    available BOOLEAN DEFAULT TRUE
);

CREATE TABLE restaurant_tables (
    id INT AUTO_INCREMENT PRIMARY KEY,
    table_number INT NOT NULL UNIQUE,
    capacity INT NOT NULL,
    status ENUM ('available', 'occupied', 'reserved'), 
    price INT DEFAULT 0
);

CREATE TABLE reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    description VARCHAR(300),
    stars INT DEFAULT 5, 
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    table_id INT,
    reservation_datetime DATETIME,
    status_reservation ENUM ('Pending', 'Confirmed', 'Cancelled', 'Arrived'),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (table_id) REFERENCES restaurant_tables(id)
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

INSERT INTO users (name, email, password, category)
VALUES ('admin', 'admin@restaurant.com', 'password', 'admin'), ('test', 'test@gmail.com', 'pass', 'normal');

INSERT INTO restaurant_tables (table_number, capacity, status, price)
VALUES (1, 4, 'available', 0), (2, 4, 'available', 0), (3, 6, 'available', 10), (4, 10, 'available', 100);

INSERT INTO menus (category, name, description, price, available)
VALUES ('drinks', 'jugo', 'pera', 15, 1), ('burgers', 'sandwich', 'ss', 15, 1), ('pasta', 'canelones', 'pera', 15, 1);

INSERT INTO deliveries (user_id, address, status)
VALUES (2, 'direccion', 'pending'), (2, 'otra_address', 'pending');

INSERT INTO deliveries_menus (delivery_id, menu_id, quantity, qr_code)
VALUES (1, 1, 2, 1), (1, 2, 1, 1), (2, 3, 10, 1);