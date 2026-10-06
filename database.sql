CREATE DATABASE IF NOT EXISTS it_helpdesk;
USE it_helpdesk;

-- USER TABLE
CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(30) NOT NULL,
    department VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TECHNICIAN TABLE
CREATE TABLE IF NOT EXISTS technicians (
    technician_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    specialization VARCHAR(100),
    email VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- CATEGORY TABLE
CREATE TABLE IF NOT EXISTS categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT
);

-- ASSET TABLE
CREATE TABLE IF NOT EXISTS assets (
    asset_id INT PRIMARY KEY AUTO_INCREMENT,
    asset_tag VARCHAR(50) UNIQUE NOT NULL,
    type VARCHAR(50) NOT NULL,
    serial_no VARCHAR(100) UNIQUE,
    purchase_date DATE,
    warranty_end DATE,
    status VARCHAR(50) DEFAULT 'Available'
);

-- TICKET TABLE
CREATE TABLE IF NOT EXISTS tickets (
    ticket_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    asset_id INT,
    technician_id INT,
    category_id INT NOT NULL,
    status VARCHAR(50) DEFAULT 'Open',
    priority VARCHAR(30) DEFAULT 'Medium',
    description TEXT NOT NULL,
    resolution TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id) ON DELETE SET NULL,
    FOREIGN KEY (technician_id) REFERENCES technicians(technician_id) ON DELETE SET NULL,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE RESTRICT
);

-- SLA_POLICY TABLE
CREATE TABLE IF NOT EXISTS sla_policies (
    policy_id INT PRIMARY KEY AUTO_INCREMENT,
    priority VARCHAR(30) UNIQUE NOT NULL,
    response_hrs INT NOT NULL,
    resolution_hrs INT NOT NULL
);

-- OPTIONAL MAINTENANCE TABLE
CREATE TABLE IF NOT EXISTS maintenance (
    maintenance_id INT PRIMARY KEY AUTO_INCREMENT,
    asset_id INT NOT NULL,
    technician_id INT,
    problem TEXT,
    maintenance_date DATE,
    repair_cost DECIMAL(10,2),
    status VARCHAR(50),
    remarks TEXT,
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id) ON DELETE CASCADE,
    FOREIGN KEY (technician_id) REFERENCES technicians(technician_id) ON DELETE SET NULL
);

-- INSERT SAMPLE DATA
-- Passwords are: admin123, user123, tech123
INSERT INTO users (name, email, password, role, department) VALUES 
('Sohan',     'sohan@company.com',     'scrypt:32768:8:1$wUIptNiIDCTYP6XD$ece73c548ae39834f94f0e7558f475489f4d0ca759d7ba0b86db6f46c32aec325e9bbc6ff7df982a826748df0dc31078e0f95bab7423e3209a7d3b97a0b3e9e7', 'admin', 'IT'),
('Kiran',     'kiran@company.com',     'scrypt:32768:8:1$jBqlImWsBklGZb0y$fd59cd1cd3e92874d30cf16717a2818972abcde63ff811fc24119f9c6727edff470d24e547d0429cc427036e1dd6b37ec4e4a25164711ae71c16ff05f5d243f2', 'user', 'HR'),
('Ram',       'ram@company.com',       'scrypt:32768:8:1$jBqlImWsBklGZb0y$fd59cd1cd3e92874d30cf16717a2818972abcde63ff811fc24119f9c6727edff470d24e547d0429cc427036e1dd6b37ec4e4a25164711ae71c16ff05f5d243f2', 'user', 'Sales'),
('Rock',      'rock@company.com',      'scrypt:32768:8:1$jBqlImWsBklGZb0y$fd59cd1cd3e92874d30cf16717a2818972abcde63ff811fc24119f9c6727edff470d24e547d0429cc427036e1dd6b37ec4e4a25164711ae71c16ff05f5d243f2', 'user', 'Marketing'),
('Alsabur',   'alsabur@company.com',   'scrypt:32768:8:1$jBqlImWsBklGZb0y$fd59cd1cd3e92874d30cf16717a2818972abcde63ff811fc24119f9c6727edff470d24e547d0429cc427036e1dd6b37ec4e4a25164711ae71c16ff05f5d243f2', 'user', 'Finance'),
('Soumya',    'soumya@company.com',    'scrypt:32768:8:1$jBqlImWsBklGZb0y$fd59cd1cd3e92874d30cf16717a2818972abcde63ff811fc24119f9c6727edff470d24e547d0429cc427036e1dd6b37ec4e4a25164711ae71c16ff05f5d243f2', 'user', 'Operations'),
('Samyuktha', 'samyuktha@company.com', 'scrypt:32768:8:1$jBqlImWsBklGZb0y$fd59cd1cd3e92874d30cf16717a2818972abcde63ff811fc24119f9c6727edff470d24e547d0429cc427036e1dd6b37ec4e4a25164711ae71c16ff05f5d243f2', 'user', 'HR'),
('Abhinay',   'abhinay@company.com',   'scrypt:32768:8:1$jBqlImWsBklGZb0y$fd59cd1cd3e92874d30cf16717a2818972abcde63ff811fc24119f9c6727edff470d24e547d0429cc427036e1dd6b37ec4e4a25164711ae71c16ff05f5d243f2', 'user', 'Sales'),
('Tanush',    'tanush@company.com',    'scrypt:32768:8:1$jBqlImWsBklGZb0y$fd59cd1cd3e92874d30cf16717a2818972abcde63ff811fc24119f9c6727edff470d24e547d0429cc427036e1dd6b37ec4e4a25164711ae71c16ff05f5d243f2', 'user', 'IT'),
('Sriram',    'sriram@company.com',    'scrypt:32768:8:1$jBqlImWsBklGZb0y$fd59cd1cd3e92874d30cf16717a2818972abcde63ff811fc24119f9c6727edff470d24e547d0429cc427036e1dd6b37ec4e4a25164711ae71c16ff05f5d243f2', 'user', 'Research');


INSERT INTO technicians (name, specialization, email, password) VALUES 
('Tom Fixer', 'Hardware', 'technician@company.com', 'scrypt:32768:8:1$9ccnQ20CCbAOR4I2$f29e19da13298edad095e40d78feac20efc11d5b7315fd16dace9275fb4f6478c85c6f218c7f161cd4adf60f81f4933939337d2b64bf51a9ebe02ee0ee7f6c30'),
('Sarah Network', 'Network', 'sarah.n@company.com', 'scrypt:32768:8:1$9ccnQ20CCbAOR4I2$f29e19da13298edad095e40d78feac20efc11d5b7315fd16dace9275fb4f6478c85c6f218c7f161cd4adf60f81f4933939337d2b64bf51a9ebe02ee0ee7f6c30'),
('Mike Software', 'Software', 'mike.s@company.com', 'scrypt:32768:8:1$9ccnQ20CCbAOR4I2$f29e19da13298edad095e40d78feac20efc11d5b7315fd16dace9275fb4f6478c85c6f218c7f161cd4adf60f81f4933939337d2b64bf51a9ebe02ee0ee7f6c30'),
('Jenny Printer', 'Printer', 'jenny.p@company.com', 'scrypt:32768:8:1$9ccnQ20CCbAOR4I2$f29e19da13298edad095e40d78feac20efc11d5b7315fd16dace9275fb4f6478c85c6f218c7f161cd4adf60f81f4933939337d2b64bf51a9ebe02ee0ee7f6c30'),
('David Server', 'Server', 'david.s@company.com', 'scrypt:32768:8:1$9ccnQ20CCbAOR4I2$f29e19da13298edad095e40d78feac20efc11d5b7315fd16dace9275fb4f6478c85c6f218c7f161cd4adf60f81f4933939337d2b64bf51a9ebe02ee0ee7f6c30');

INSERT INTO categories (name, description) VALUES 
('Hardware', 'Physical devices like monitors, keyboards, mice'),
('Software', 'Applications and operating systems'),
('Network', 'Internet, Wi-Fi, VPN connectivity'),
('Printer', 'Printers, scanners, copiers'),
('Email', 'Email access and configuration'),
('Other', 'Any other IT related issues');

INSERT INTO assets (asset_tag, type, serial_no, purchase_date, warranty_end, status) VALUES 
('AST-LP-001', 'Laptop', 'SN-LP1001', '2022-01-15', '2025-01-15', 'Assigned'),
('AST-LP-002', 'Laptop', 'SN-LP1002', '2022-03-10', '2025-03-10', 'Available'),
('AST-DT-001', 'Desktop', 'SN-DT2001', '2021-06-20', '2024-06-20', 'Assigned'),
('AST-PR-001', 'Printer', 'SN-PR3001', '2023-02-05', '2026-02-05', 'Available'),
('AST-MO-001', 'Monitor', 'SN-MO4001', '2022-11-12', '2025-11-12', 'Assigned'),
('AST-MO-002', 'Monitor', 'SN-MO4002', '2022-11-12', '2025-11-12', 'Maintenance'),
('AST-NW-001', 'Router', 'SN-NW5001', '2020-05-15', '2023-05-15', 'Retired'),
('AST-LP-003', 'Laptop', 'SN-LP1003', '2023-08-22', '2026-08-22', 'Assigned'),
('AST-LP-004', 'Laptop', 'SN-LP1004', '2023-08-22', '2026-08-22', 'Available'),
('AST-DT-002', 'Desktop', 'SN-DT2002', '2021-06-20', '2024-06-20', 'Assigned');

INSERT INTO sla_policies (priority, response_hrs, resolution_hrs) VALUES 
('High', 1, 4),
('Medium', 4, 12),
('Low', 8, 24);

INSERT INTO tickets (user_id, asset_id, technician_id, category_id, status, priority, description, resolution) VALUES 
(2, 1, 1, 1, 'Resolved', 'Medium', 'Laptop screen is flickering.', 'Replaced screen cable.'),
(3, NULL, 2, 3, 'In Progress', 'High', 'Cannot connect to office Wi-Fi.', NULL),
(4, 4, 4, 4, 'Open', 'Low', 'Printer is out of toner.', NULL),
(5, NULL, 3, 2, 'Closed', 'Medium', 'Need MS Office installed.', 'Installed and activated Office 365.'),
(6, 3, 1, 1, 'Open', 'High', 'Desktop won\'t turn on.', NULL),
(7, NULL, 5, 5, 'Resolved', 'High', 'Email password reset requested.', 'Password reset link sent.'),
(8, 5, 1, 1, 'In Progress', 'Medium', 'Monitor has dead pixels.', NULL),
(9, NULL, 2, 3, 'Open', 'Medium', 'VPN access is very slow.', NULL),
(10, 8, 3, 2, 'Closed', 'Low', 'Update required for accounting software.', 'Updated to latest version.'),
(2, NULL, NULL, 6, 'Open', 'Low', 'Need a new mouse pad.', NULL);
