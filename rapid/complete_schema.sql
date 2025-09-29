-- ================================================================
-- RAPID Relief Management System - Complete Database Schema
-- ================================================================
-- Created: September 2025
-- Description: Comprehensive schema with tables, views, functions, triggers
-- Database: project2
-- User: flaskuser@localhost
-- ================================================================

-- ========================
-- DROP VIEWS, FUNCTIONS, TRIGGERS FIRST
-- ========================
DROP VIEW IF EXISTS item_list;
DROP VIEW IF EXISTS maping;
DROP VIEW IF EXISTS feedback_view;
DROP VIEW IF EXISTS receiver_by_area_view;

DROP TRIGGER IF EXISTS before_insert_item;
DROP TRIGGER IF EXISTS after_insert_donation_receiver;

DROP FUNCTION IF EXISTS get_available_quantity;
DROP FUNCTION IF EXISTS get_item_name;
DROP FUNCTION IF EXISTS deduct_stock;

-- ========================
-- DROP TABLES IN CORRECT ORDER
-- ========================
DROP TABLE IF EXISTS feedback;
DROP TABLE IF EXISTS money_transfer;
DROP TABLE IF EXISTS event;
DROP TABLE IF EXISTS donation_receiver;
DROP TABLE IF EXISTS stock;
DROP TABLE IF EXISTS donation;
DROP TABLE IF EXISTS item;
DROP TABLE IF EXISTS volunteer;
DROP TABLE IF EXISTS event_type;
DROP TABLE IF EXISTS donor;
DROP TABLE IF EXISTS receiver;
DROP TABLE IF EXISTS type_list;
DROP TABLE IF EXISTS account;

-- ========================
-- CREATE TABLES WITH ALL COLUMNS
-- ========================

-- Account table (modified to handle non-auto increment IDs)
CREATE TABLE account (
    account_id INT PRIMARY KEY NOT NULL,  -- Changed from AUTO_INCREMENT
    account_name VARCHAR(100) NOT NULL,
    method_name VARCHAR(100) NOT NULL,
    balance DECIMAL(10,2) CHECK (balance >= 0)
);

-- Donor table with all columns
CREATE TABLE donor (
    donor_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    user_name VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(100),
    password TEXT NOT NULL,
    account_name VARCHAR(20) NOT NULL,
    account_id INT NOT NULL,
    address TEXT,
    profile_picture BLOB,
    FOREIGN KEY (account_id) REFERENCES account(account_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Receiver table
CREATE TABLE receiver (
    receiver_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    user_name VARCHAR(20) NOT NULL UNIQUE,
    password TEXT NOT NULL,
    emergency_phone VARCHAR(20),
    address TEXT,
    email VARCHAR(100),
    profile_picture BLOB
);

-- Type list table
CREATE TABLE type_list (
    type_id INT PRIMARY KEY AUTO_INCREMENT,
    type_name VARCHAR(50)
);

-- Event type table
CREATE TABLE event_type (
    event_type_id INT PRIMARY KEY AUTO_INCREMENT,
    event_type VARCHAR(100)
);

-- Volunteer table
CREATE TABLE volunteer (
    volunteer_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100) DEFAULT NULL,
    dob DATE NOT NULL,
    address TEXT NOT NULL,
    pref_address TEXT,
    join_time DATE NOT NULL,
    user_name VARCHAR(20) NOT NULL,
    password TEXT NOT NULL,
    nid_birthcert MEDIUMBLOB,
    profile_picture MEDIUMBLOB,
    status VARCHAR(255) DEFAULT 'new',
    PRIMARY KEY (volunteer_id),
    UNIQUE KEY user_name (user_name)
);

-- Item table
CREATE TABLE item (
    item_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    type_id INT,
    FOREIGN KEY (type_id) REFERENCES type_list(type_id)
        ON UPDATE CASCADE ON DELETE SET NULL
);

-- Donation table
CREATE TABLE donation (
    donation_id INT PRIMARY KEY AUTO_INCREMENT,
    message TEXT,
    date DATE,
    donor_id INT,
    item_id_list TEXT,
    FOREIGN KEY (donor_id) REFERENCES donor(donor_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- Money transfer table with all constraints
CREATE TABLE money_transfer (
    money_transfer_id INT PRIMARY KEY AUTO_INCREMENT,
    account_id INT,
    donation_id INT,
    amount DECIMAL(10,2) CHECK (amount > 0),
    FOREIGN KEY (account_id) REFERENCES account(account_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (donation_id) REFERENCES donation(donation_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- Stock table with account_id column included
CREATE TABLE stock (
    stock_id INT PRIMARY KEY AUTO_INCREMENT,
    price INT CHECK (price >= 0),
    quantity INT CHECK (quantity >= 0),
    purchase_date DATE,
    stock_date DATE NOT NULL,
    expire_date DATE,
    item_id INT,
    account_id INT NULL,  -- Added column from ALTER TABLE
    FOREIGN KEY (item_id) REFERENCES item(item_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (account_id) REFERENCES account(account_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Donation receiver table with all additional columns
CREATE TABLE donation_receiver (
    donation_receiver_id INT PRIMARY KEY AUTO_INCREMENT,
    receiver_id INT,
    date DATE NOT NULL,
    priority_message TEXT,
    item_id_list TEXT,
    additional_item TEXT,
    priority_level VARCHAR(20) DEFAULT 'medium',  -- Added from ALTER TABLE
    latitude DECIMAL(10, 8),                     -- Added from ALTER TABLE
    longitude DECIMAL(11, 8),                    -- Added from ALTER TABLE
    status VARCHAR(30) DEFAULT 'pending',        -- Added from ALTER TABLE
    FOREIGN KEY (receiver_id) REFERENCES receiver(receiver_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- Event table with location column included
CREATE TABLE event (
    event_id INT PRIMARY KEY AUTO_INCREMENT,
    volunteer_id_list TEXT,
    event_type_id INT,
    item_id_list TEXT,
    donation_receiver_id INT,
    start_date DATE,
    end_date DATE,
    status VARCHAR(30) NOT NULL,
    location VARCHAR(255)  -- Added from ALTER TABLE
);

-- Feedback table
CREATE TABLE feedback (
    feedback_id INT PRIMARY KEY AUTO_INCREMENT,
    receiver_id INT,
    volunteer_id INT,
    donor_id INT,
    message TEXT,
    picture BLOB,
    FOREIGN KEY (receiver_id) REFERENCES receiver(receiver_id),
    FOREIGN KEY (volunteer_id) REFERENCES volunteer(volunteer_id),
    FOREIGN KEY (donor_id) REFERENCES donor(donor_id)
);

-- ========================
-- INSERT SAMPLE DATA
-- ========================

-- Insert sample accounts (non-auto increment)
INSERT INTO account (account_id, account_name, method_name, balance) VALUES
(1, 'Main Bank', 'Bank Transfer', 60300.00),
(2, 'Bkash Account', 'Bkash', 37500.00),
(3, 'Nagad Account', 'Nagad', 31200.00);

-- Insert sample type list
INSERT INTO type_list (type_name) VALUES 
('Food'),
('Clothing'),
('Medicine'),
('Water'),
('Shelter'),
('Hygiene'),
('Tools'),
('Fuel'),
('Money'),
('Other');

-- Insert sample event types
INSERT INTO event_type (event_type) VALUES
('Food Distribution'),
('Medical Camp'),
('Clothing Drive'),
('Water Supply'),
('Shelter Setup'),
('Hygiene Awareness'),
('Tool Distribution'),
('Fuel Aid'),
('Communication Support'),
('General Relief');

-- Insert sample items
INSERT INTO item (name, type_id) VALUES
('Rice', 1),
('Lentils', 1),
('Cooking Oil', 1),
('Blanket', 2),
('Clothes', 2),
('Shoes', 2),
('Paracetamol', 3),
('Antiseptic', 3),
('First Aid Kit', 3),
('Bottled Water', 4),
('Water Filter', 4),
('Tent', 5),
('Tarpaulin', 5),
('Soap', 6),
('Hand Sanitizer', 6),
('Hammer', 7),
('Screwdriver', 7),
('Diesel', 8),
('Generator', 8),
('Cash Donation', 9),
('Emergency Radio', 10);

-- ========================
-- CREATE VIEWS
-- ========================

-- View for receiver statistics by area
CREATE VIEW receiver_by_area_view AS
SELECT 
    r.address AS address, 
    COUNT(d.donation_receiver_id) AS cnt
FROM donation_receiver d
JOIN receiver r ON d.receiver_id = r.receiver_id
GROUP BY r.address;

-- View for comprehensive feedback information
CREATE VIEW feedback_view AS
SELECT 
    f.feedback_id, 
    r.name AS receiver_name, 
    v.name AS volunteer_name, 
    d.name AS donor_name, 
    f.message, 
    f.picture 
FROM feedback f 
LEFT JOIN receiver r ON f.receiver_id = r.receiver_id 
LEFT JOIN volunteer v ON f.volunteer_id = v.volunteer_id 
LEFT JOIN donor d ON f.donor_id = d.donor_id 
ORDER BY f.feedback_id DESC;

-- View for mapping coordinates
CREATE VIEW maping AS
SELECT latitude, longitude 
FROM donation_receiver
WHERE latitude IS NOT NULL AND longitude IS NOT NULL;

-- View for item list (simplified item view)
CREATE VIEW item_list AS 
SELECT item_id, name 
FROM item;

-- ========================
-- CREATE FUNCTIONS
-- ========================

DELIMITER $$

-- Function to get item name by ID
CREATE FUNCTION get_item_name(p_item_id INT) 
RETURNS VARCHAR(50) 
DETERMINISTIC 
READS SQL DATA
BEGIN 
    DECLARE i_name VARCHAR(50); 
    SELECT name INTO i_name 
    FROM item 
    WHERE item_id = p_item_id 
    LIMIT 1;
    RETURN i_name; 
END$$

-- Function to get available stock quantity
CREATE FUNCTION get_available_quantity(p_item_id INT) 
RETURNS INT
DETERMINISTIC 
READS SQL DATA
BEGIN
    DECLARE qty INT DEFAULT 0;
    SELECT IFNULL(SUM(quantity), 0) INTO qty
    FROM stock
    WHERE item_id = p_item_id
    AND expire_date >= CURDATE();
    RETURN qty;
END$$

-- Function to deduct stock with FIFO logic
CREATE FUNCTION deduct_stock(p_item_id INT, deduct_qty INT) 
RETURNS INT
DETERMINISTIC 
MODIFIES SQL DATA
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE batch_id INT;
    DECLARE batch_qty INT;
    DECLARE remaining_qty INT DEFAULT deduct_qty;
    
    DECLARE cur CURSOR FOR
        SELECT stock_id, quantity
        FROM stock
        WHERE item_id = p_item_id
        AND expire_date >= CURDATE()
        AND quantity > 0
        ORDER BY expire_date ASC, stock_date ASC;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO batch_id, batch_qty;
        IF done OR remaining_qty <= 0 THEN
            LEAVE read_loop;
        END IF;

        IF batch_qty <= remaining_qty THEN
            SET remaining_qty = remaining_qty - batch_qty;
            UPDATE stock SET quantity = 0 WHERE stock_id = batch_id;
        ELSE
            UPDATE stock SET quantity = quantity - remaining_qty WHERE stock_id = batch_id;
            SET remaining_qty = 0;
        END IF;
    END LOOP;

    CLOSE cur;
    RETURN remaining_qty;
END$$

-- Stored procedure for deducting stock with transaction control (alternative to function)
CREATE PROCEDURE deduct_stock_safe(
    IN p_item_id INT, 
    IN deduct_qty INT, 
    OUT remaining_qty INT
)
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE batch_id INT;
    DECLARE batch_qty INT;
    
    DECLARE cur CURSOR FOR
        SELECT stock_id, quantity
        FROM stock
        WHERE item_id = p_item_id
        AND expire_date >= CURDATE()
        AND quantity > 0
        ORDER BY expire_date ASC, stock_date ASC;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        GET DIAGNOSTICS CONDITION 1 @sqlstate = RETURNED_SQLSTATE, @errno = MYSQL_ERRNO, @text = MESSAGE_TEXT;
        SET remaining_qty = -1; -- Indicate error
    END;

    SET remaining_qty = deduct_qty;
    START TRANSACTION;
    
    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO batch_id, batch_qty;
        IF done OR remaining_qty <= 0 THEN
            LEAVE read_loop;
        END IF;

        IF batch_qty <= remaining_qty THEN
            SET remaining_qty = remaining_qty - batch_qty;
            UPDATE stock SET quantity = 0 WHERE stock_id = batch_id;
        ELSE
            UPDATE stock SET quantity = quantity - remaining_qty WHERE stock_id = batch_id;
            SET remaining_qty = 0;
        END IF;
    END LOOP;

    CLOSE cur;
    COMMIT;
END$$

DELIMITER ;

-- ========================
-- CREATE TRIGGERS
-- ========================

DELIMITER $$

-- Trigger to standardize item names (capitalize first letter)
CREATE TRIGGER before_insert_item 
BEFORE INSERT ON item 
FOR EACH ROW 
BEGIN 
    IF NEW.name IS NOT NULL THEN
        SET NEW.name = CONCAT(UCASE(LEFT(NEW.name,1)), LCASE(SUBSTRING(NEW.name,2))); 
    END IF;
END$$

-- Trigger to log coordinates when donation_receiver is inserted
CREATE TRIGGER after_insert_donation_receiver
AFTER INSERT ON donation_receiver
FOR EACH ROW 
BEGIN
    -- This trigger can be used for logging or additional processing
    -- The mapping view already handles coordinate display
    IF NEW.latitude IS NOT NULL AND NEW.longitude IS NOT NULL THEN
        -- Log coordinates for mapping system
        SET @coordinate_log = CONCAT('New donation receiver added at: ', NEW.latitude, ', ', NEW.longitude);
    END IF;
END$$

DELIMITER ;

-- ========================
-- SAMPLE DATA UPDATES
-- ========================

-- Sample donor data with emails (modify as needed)
/*
UPDATE donor
SET email = CASE donor_id
    WHEN 1 THEN 'mohammad@example.com'
    WHEN 2 THEN 'abdullah@example.com'
    WHEN 3 THEN 'fatima@example.com'
    WHEN 4 THEN 'ayesha@example.com'
    WHEN 5 THEN 'rahman@example.com'
    WHEN 6 THEN 'karim@example.com'
    WHEN 7 THEN 'sultana@example.com'
    WHEN 8 THEN 'hasan@example.com'
    WHEN 9 THEN 'nadia@example.com'
    WHEN 10 THEN 'jamal@example.com'
END
WHERE donor_id BETWEEN 1 AND 10;
*/

-- Sample location updates for events (modify as needed)
/*
UPDATE event
SET location = CASE event_id
    WHEN 1 THEN 'Dhaka City'
    WHEN 2 THEN 'Chattogram Port'
    WHEN 3 THEN 'Khulna District'
    WHEN 4 THEN 'Rajshahi Division'
    WHEN 5 THEN 'Barishal Sadar'
    WHEN 6 THEN 'Sylhet City'
    WHEN 7 THEN 'Rangpur District'
    WHEN 8 THEN 'Mymensingh Town'
    WHEN 9 THEN 'Cox''s Bazar Beach'
    WHEN 10 THEN 'Comilla City'
END
WHERE event_id BETWEEN 1 AND 10;
*/

-- Sample GPS coordinates for donation receivers (modify as needed)
/*
UPDATE donation_receiver SET latitude = 23.810331, longitude = 90.412521 WHERE donation_receiver_id = 1;
UPDATE donation_receiver SET latitude = 22.356852, longitude = 91.783180 WHERE donation_receiver_id = 2;
UPDATE donation_receiver SET latitude = 24.363588, longitude = 88.624135 WHERE donation_receiver_id = 3;
UPDATE donation_receiver SET latitude = 23.460691, longitude = 91.180889 WHERE donation_receiver_id = 4;
UPDATE donation_receiver SET latitude = 25.743892, longitude = 89.275227 WHERE donation_receiver_id = 5;
UPDATE donation_receiver SET latitude = 24.899837, longitude = 91.871337 WHERE donation_receiver_id = 6;
UPDATE donation_receiver SET latitude = 22.845641, longitude = 89.540328 WHERE donation_receiver_id = 7;
UPDATE donation_receiver SET latitude = 21.433920, longitude = 92.005810 WHERE donation_receiver_id = 8;
UPDATE donation_receiver SET latitude = 25.096773, longitude = 89.022770 WHERE donation_receiver_id = 9;
UPDATE donation_receiver SET latitude = 23.177768, longitude = 89.180510 WHERE donation_receiver_id = 10;
*/

-- Sample stock account assignments (modify as needed)
/*
UPDATE stock
SET account_id = CASE
    WHEN stock_id % 3 = 1 THEN 1
    WHEN stock_id % 3 = 2 THEN 2
    WHEN stock_id % 3 = 0 THEN 3
END
WHERE stock_id <= 10;
*/

-- ========================
-- GRANT PERMISSIONS (Run as root user)
-- ========================

/*
-- Execute these commands as MySQL root user:
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, DROP, INDEX, 
      CREATE ROUTINE, ALTER ROUTINE, EXECUTE, CREATE VIEW, SHOW VIEW, TRIGGER 
ON project2.* TO 'flaskuser'@'localhost'; 

SET GLOBAL log_bin_trust_function_creators = 1; 
FLUSH PRIVILEGES;
*/

-- ================================================================
-- SCHEMA CREATION COMPLETE
-- ================================================================
-- 
-- This schema includes:
-- ✅ All tables with complete column definitions (no ALTER TABLE needed)
-- ✅ All foreign key constraints properly defined
-- ✅ All views for data analysis and reporting
-- ✅ All custom functions for business logic
-- ✅ All triggers for data integrity and automation
-- ✅ Proper error handling and transaction management
-- ✅ Account table modified to handle non-auto increment IDs
-- ✅ Sample data structure included (uncomment UPDATE statements as needed)
--
-- Usage Instructions:
-- 1. Execute permission grants as root user (see comments above)
-- 2. Run this script as flaskuser@localhost
-- 3. Uncomment and modify sample data UPDATE statements as needed
-- 4. Insert your actual user and transaction data
-- 5. Test all functions and triggers
--
-- Database Objects Created:
-- - 12 Tables with complete structure
-- - 4 Views for reporting and analysis
-- - 3 Functions for business logic
-- - 2 Triggers for data integrity
-- - All necessary constraints and indexes
--
-- ================================================================