CREATE DATABASE IF NOT EXISTS restaurant;
USE restaurant;

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
    category_id INT,
    name VARCHAR(100) UNIQUE NOT NULL,
    description VARCHAR(500),
    price DECIMAL(10,2) NOT NULL,
    available BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (category_id) REFERENCES menu_categories(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS restaurant_tables (
    id INT AUTO_INCREMENT PRIMARY KEY,
    table_number INT NOT NULL UNIQUE,
    capacity INT NOT NULL,
    status_table ENUM ('Available', 'Occupied', 'Reserved') NOT NULL,
    price INT DEFAULT 0,
);

CREATE TABLE IF NOT EXISTS tables_menus (
    id INT AUTO_INCREMENT PRIMARY KEY,
    table_id INT,
    menu_id INT,
    quantity INT DEFAULT 1,
    FOREIGN KEY (table_id) REFERENCES restaurant_tables(id),
    FOREIGN KEY (menu_id) REFERENCES menu_items(id)
);
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    table_id INT,
    order_datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM ('Pending', 'In Preparation', 'Delivered', 'Paid') NOT NULL,
    total DECIMAL(10, 2),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (table_id) REFERENCES restaurant_tables(id),
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
    status_table ENUM ('Available', 'Occupied', 'Reserved') NOT NULL,
    status_reservation ENUM ('Pending', 'Confirmed', 'Cancelled', 'Arrived') NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (table_id) REFERENCES restaurant_tables(id),

);

CREATE TABLE IF NOT EXISTS deliverys (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    delivery_address VARCHAR(255),
    delivery_datetime DATETIME,
    status_deliverys ENUM ('Pending', 'In Transit', 'Delivered', 'Cancelled') NOT NULL, 
    FOREIGN KEY (order_id) REFERENCES orders(id)
);

INSERT IGNORE INTO status_deliverys (name) VALUES ('Pending'), ('In Transit'), ('Delivered'), ('Cancelled');
INSERT IGNORE INTO status_restaurant_tables (name) VALUES ('Available'), ('Occupied'), ('Reserved');
INSERT IGNORE INTO menu_categories (name) VALUES ('Drinks'), ('Burgers'), ('Pasta');

INSERT IGNORE INTO restaurant_tables (table_number, capacity, price, status_table) VALUES (1, 4, 100, 'Available');
INSERT IGNORE INTO restaurant_tables (table_number, capacity, price, status_table) VALUES (2, 8, 500, 'Available');
INSERT IGNORE INTO restaurant_tables (table_number, capacity, price, status_table) VALUES (3, 12, 1500, 'Available');
INSERT IGNORE INTO restaurant_tables (table_number, capacity, price, status_table) VALUES (4, 16, 3200, 'Available');

INSERT IGNORE INTO menu_items (category_id, name, description, price, available) 
VALUES (1, 'Jugo de frutas', 'Jugo elaborado con frutas exoticas higo, durazno y mas', 30, TRUE);

INSERT IGNORE INTO menu_items (category_id, name, description, price, available) 
VALUES (1, 'Chicha Morada', 'Bebida exquisita a base de maiz morado', 30, TRUE);

INSERT IGNORE INTO users (email, password, category) 
VALUES ('admin@restaurant.com', 'password_hash_seguro', 'admin');

INSERT IGNORE INTO orders (user_id, table_id, status, total)
VALUES (1, 1, 'In Preparation', 100);
INSERT IGNORE INTO orders (user_id, table_id, status, total)
VALUES (1, 2, 'In Preparation', 150);

INSERT IGNORE INTO tables_menus (table_id, menu_id, quantity) 
VALUES (1, 1, 3);
INSERT IGNORE INTO tables_menus (table_id, menu_id, quantity) 
VALUES (2, 2, 2);
INSERT IGNORE INTO tables_menus (table_id, menu_id, quantity) 
VALUES (1, 2, 2);
INSERT IGNORE INTO tables_menus (table_id, menu_id, quantity) 
VALUES (2, 1, 3);