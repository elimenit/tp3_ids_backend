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
