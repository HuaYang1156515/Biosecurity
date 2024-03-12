-- Roles Table
CREATE TABLE roles (
    role_id INT AUTO_INCREMENT PRIMARY KEY,
    role_name ENUM('mariner', 'staff', 'admin') NOT NULL UNIQUE
);

-- Insert Roles
INSERT INTO roles (role_name) VALUES ('mariner'), ('staff'), ('admin');

-- Users Table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL, -- Stored as a hash
    role_id INT NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20),
    status ENUM('active', 'inactive') NOT NULL,
    date_joined DATE NOT NULL,
    FOREIGN KEY (role_id) REFERENCES roles(role_id)
);

-- Mariner Profiles Table
CREATE TABLE mariner_profiles (
    mariner_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    mariner_id_number VARCHAR(20) NOT NULL UNIQUE,
    address TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Staff/Admin Profiles Table
CREATE TABLE staff_admin_profiles (
    staff_admin_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    staff_number VARCHAR(20) NOT NULL UNIQUE,
    work_phone VARCHAR(20),
    hire_date DATE NOT NULL,
    position VARCHAR(255),
    department VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Ocean Guide Table
CREATE TABLE ocean_guide (
    ocean_id INT AUTO_INCREMENT PRIMARY KEY,
    ocean_item_type ENUM('pest', 'disease') NOT NULL,
    present_in_NZ BOOLEAN NOT NULL,
    common_name VARCHAR(255) NOT NULL,
    scientific_name VARCHAR(255),
    key_characteristics TEXT,
    biology_description TEXT,
    threats TEXT,
    location TEXT,
    primary_image VARCHAR(255) -- Store the filename or URL of the primary image
);

-- Ocean Images Table
CREATE TABLE ocean_images (
    image_id INT AUTO_INCREMENT PRIMARY KEY,
    ocean_id INT NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    is_primary BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (ocean_id) REFERENCES ocean_guide(ocean_id)
);
