CREATE DATABASE IF NOT EXISTS restaurant;
USE restaurant;

CREATE TABLE IF NOT EXISTS menu_categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL,
    category VARCHAR(100) NOT NULL, 
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP 
);

CREATE TABLE IF NOT EXISTS menu_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    available BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (category_id) REFERENCES menu_categories(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS status_tables (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS status_orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS restaurant_tables (
    id INT AUTO_INCREMENT PRIMARY KEY,
    table_number INT NOT NULL UNIQUE,
    capacity INT NOT NULL,
    status_table_id INT, 
    price INT DEFAULT 0,
    FOREIGN KEY (status_table_id) REFERENCES status_tables(id)
);

CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    table_id INT,
    order_datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
    status_id INT,
    total DECIMAL(10, 2),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (table_id) REFERENCES restaurant_tables(id),
    FOREIGN KEY (status_id) REFERENCES status_orders(id)
);

CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    menu_item_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    unit_price DECIMAL(10,2) NOT NULL,
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

INSERT IGNORE INTO status_orders (name) VALUES ('Pending'), ('In Preparation'), ('Delivered'), ('Paid');
INSERT IGNORE INTO status_tables (name) VALUES ('Available'), ('Occupied'), ('Reserved');
INSERT IGNORE INTO menu_categories (name) VALUES ('Drinks'), ('Burgers'), ('Pasta');

INSERT IGNORE INTO restaurant_tables (table_number, capacity, price, status_id) VALUES (1, 4, 100, 1);
INSERT IGNORE INTO restaurant_tables (table_number, capacity, price, status_id) VALUES (2, 8, 500, 1);
INSERT IGNORE INTO restaurant_tables (table_number, capacity, price, status_id) VALUES (3, 12, 1500, 1);
INSERT IGNORE INTO restaurant_tables (table_number, capacity, price, status_id) VALUES (4, 16, 3200, 1);

INSERT IGNORE INTO users (email, password, category) 
VALUES ('admin@restaurant.com', 'password_hash_seguro', 'admin');