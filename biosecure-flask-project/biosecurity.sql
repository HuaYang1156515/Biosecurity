INSERT INTO users (username, password, first_name, last_name, email, phone_number, date_joined, status, role) VALUES
('mariner1', '{hashed_password}', 'John', 'Doe', 'johndoe@example.com', '123456789', CURDATE(), 'active', 'mariner'),
('staff1', '{hashed_password}', 'Jane', 'Smith', 'janesmith@example.com', '987654321', CURDATE(), 'active', 'staff'),
('admin', '{hashed_password}', 'Admin', 'User', 'adminuser@example.com', '192837465', CURDATE(), 'active', 'admin');
