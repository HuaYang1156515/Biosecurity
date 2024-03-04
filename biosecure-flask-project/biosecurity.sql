CREATE DATABASE IF NOT EXISTS biosecurity;
USE biosecurity;

-- Roles Table
CREATE TABLE IF NOT EXISTS roles (
    role_id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(255) UNIQUE NOT NULL
);

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role_id INT,
    FOREIGN KEY (role_id) REFERENCES roles(role_id)
);

-- Mariners Table
CREATE TABLE IF NOT EXISTS mariners (
    mariner_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Staff/Admin Table (assuming staff and admins are also users)
-- This could be represented by roles in the users table or separated if more information is needed

-- Ocean Pest Table
CREATE TABLE IF NOT EXISTS ocean_pest (
    pest_id INT AUTO_INCREMENT PRIMARY KEY,
    common_name VARCHAR(255) NOT NULL,
    scientific_name VARCHAR(255),
    is_present_in_nz BOOLEAN,
    description TEXT,
    threats TEXT,
    location TEXT,
    primary_image_url VARCHAR(255)
);

-- Optionally, create a table for images if multiple images per pest are needed
CREATE TABLE IF NOT EXISTS ocean_pest_images (
    image_id INT AUTO_INCREMENT PRIMARY KEY,
    pest_id INT,
    image_url VARCHAR(255) NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (pest_id) REFERENCES ocean_pest(pest_id)
);

-- Insert roles (example)
INSERT INTO roles (role_name) VALUES ('Mariner'), ('Staff'), ('Admin');
