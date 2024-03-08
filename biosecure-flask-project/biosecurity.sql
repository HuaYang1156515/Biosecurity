CREATE TABLE IF NOT EXISTS roles (
    role_id INT AUTO_INCREMENT PRIMARY KEY,
    role_name ENUM('mariner', 'staff', 'admin') UNIQUE NOT NULL,
    description TEXT
);
