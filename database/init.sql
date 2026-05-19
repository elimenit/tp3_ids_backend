CREATE DATABASE IF NOT EXISTS restaurant;
USE restaurant;

CREATE TABLE IF NOT EXISTS menu_categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL,
    category VARCHAR(100) DEFAULT 'normal', 
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP 
);

CREATE TABLE IF NOT EXISTS menu_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT UNIQUE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    available BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (category_id) REFERENCES menu_categories(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS status_restaurant_tables (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS status_orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);
CREATE TABLE IF NOT EXISTS status_reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS status_deliverys (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS restaurant_tables (
    id INT AUTO_INCREMENT PRIMARY KEY,
    table_number INT NOT NULL UNIQUE,
    capacity INT NOT NULL,
    status_table_id INT, 
    price INT DEFAULT 0,
    FOREIGN KEY (status_table_id) REFERENCES status_restaurant_tables(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    table_id INT UNIQUE,
    order_datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
    status_id INT,
    total DECIMAL(10, 2),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (table_id) REFERENCES restaurant_tables(id),
    FOREIGN KEY (status_id) REFERENCES status_orders(id)
);

CREATE TABLE IF NOT EXISTS order_menus (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT UNIQUE,
    menu_item_id INT,
    quantity INT NOT NULL DEFAULT 1,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
);

CREATE TABLE IF NOT EXISTS payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL, 
    amount DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(100) NOT NULL, 
    paid_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);

CREATE TABLE IF NOT EXISTS reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    description VARCHAR(300),
    stars INT DEFAULT 5, 
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    table_id INT,
    reservation_datetime DATETIME,
    status_table_id INT, 
    status_reservation_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (table_id) REFERENCES restaurant_tables(id),
    FOREIGN KEY (status_table_id) REFERENCES status_restaurant_tables(id),
    FOREIGN KEY (status_reservation_id) REFERENCES status_reservations(id)
);

CREATE TABLE IF NOT EXISTS deliverys (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    delivery_address VARCHAR(255),
    delivery_datetime DATETIME,
    status_orders_id INT, 
    status_deliverys_id INT, 
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (status_orders_id) REFERENCES status_orders(id),
    FOREIGN KEY (status_deliverys_id) REFERENCES status_deliverys(id)
);

INSERT IGNORE INTO status_orders (name) VALUES ('Pending'), ('In Preparation'), ('Delivered'), ('Paid');
INSERT IGNORE INTO status_reservations (name) VALUES ('Pending'), ('Confirmed'), ('Cancelled'), ('Arrived');
INSERT IGNORE INTO status_deliverys (name) VALUES ('Pending'), ('In Transit'), ('Delivered'), ('Cancelled');
INSERT IGNORE INTO status_restaurant_tables (name) VALUES ('Available'), ('Occupied'), ('Reserved');
INSERT IGNORE INTO menu_categories (name) VALUES ('Drinks'), ('Burgers'), ('Pasta');

INSERT IGNORE INTO restaurant_tables (table_number, capacity, price, status_table_id) VALUES (1, 4, 100, 1);
INSERT IGNORE INTO restaurant_tables (table_number, capacity, price, status_table_id) VALUES (2, 8, 500, 1);
INSERT IGNORE INTO restaurant_tables (table_number, capacity, price, status_table_id) VALUES (3, 12, 1500, 1);
INSERT IGNORE INTO restaurant_tables (table_number, capacity, price, status_table_id) VALUES (4, 16, 3200, 1);

INSERT IGNORE INTO menu_items (category_id, name, description, price, available) 
VALUES (1, 'Jugo de frutas', 'Jugo elaborado con frutas exoticas higo, durazno y mas', 30, TRUE);

INSERT IGNORE INTO menu_items (category_id, name, description, price, available) 
VALUES (1, 'Chicha Morada', 'Bebida exquisita a base de maiz morado', 30, TRUE);

INSERT IGNORE INTO users (email, password, category) 
VALUES ('admin@restaurant.com', 'password_hash_seguro', 'admin');

INSERT IGNORE INTO orders (user_id, table_id, status_id, total)
VALUES (1, 1, 2, 100);
INSERT IGNORE INTO orders (user_id, table_id, status_id, total)
VALUES (1, 2, 2, 150);
INSERT IGNORE INTO order_menus (order_id, menu_item_id, quantity)
VALUES (1, 1, 3);

INSERT IGNORE INTO order_menus (order_id, menu_item_id, quantity)
VALUES (2, 2, 5);