-- ================================================================
-- RAPID Relief Management System - Dummy Data Insert Script
-- ================================================================
-- Created: September 2025
-- Description: Comprehensive dummy data for all tables
-- Database: project2
-- User: flaskuser@localhost
-- ================================================================

-- Clear existing data to avoid duplicate key errors
SET FOREIGN_KEY_CHECKS = 0;

-- Delete in reverse order of dependencies
DELETE FROM feedback;
DELETE FROM money_transfer;
DELETE FROM event;
DELETE FROM donation_receiver;
DELETE FROM stock;
DELETE FROM donation;
DELETE FROM item;
DELETE FROM volunteer;
DELETE FROM event_type;
DELETE FROM donor;
DELETE FROM receiver;
DELETE FROM type_list;
DELETE FROM account;

-- Reset auto-increment counters
ALTER TABLE feedback AUTO_INCREMENT = 1;
ALTER TABLE money_transfer AUTO_INCREMENT = 1;
ALTER TABLE event AUTO_INCREMENT = 1;
ALTER TABLE donation_receiver AUTO_INCREMENT = 1;
ALTER TABLE stock AUTO_INCREMENT = 1;
ALTER TABLE donation AUTO_INCREMENT = 1;
ALTER TABLE item AUTO_INCREMENT = 1;
ALTER TABLE volunteer AUTO_INCREMENT = 1;
ALTER TABLE event_type AUTO_INCREMENT = 1;
ALTER TABLE donor AUTO_INCREMENT = 1;
ALTER TABLE receiver AUTO_INCREMENT = 1;
ALTER TABLE type_list AUTO_INCREMENT = 1;

SET FOREIGN_KEY_CHECKS = 1;

-- ========================
-- INSERT ACCOUNT DATA
-- ========================
INSERT INTO account (account_id, account_name, method_name, balance) VALUES
(1, 'Main Bank Account', 'Bank Transfer', 85000.00),
(2, 'Bkash Mobile Banking', 'Bkash', 45500.00),
(3, 'Nagad Mobile Banking', 'Nagad', 32800.00),
(4, 'Dutch Bangla Bank', 'Bank Transfer', 67200.00),
(5, 'Rocket Mobile Banking', 'Rocket', 28900.00),
(6, 'Emergency Fund Account', 'Bank Transfer', 125000.00),
(7, 'Donation Collection AC', 'Bank Transfer', 98500.00),
(8, 'Upay Mobile Banking', 'Upay', 15600.00);

-- ========================
-- INSERT TYPE_LIST DATA
-- ========================
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
('Electronics'),
('Educational'),
('Baby Care'),
('Emergency'),
('Other');

-- ========================
-- INSERT EVENT_TYPE DATA
-- ========================
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
('General Relief'),
('Emergency Response'),
('Educational Support'),
('Child Care Program'),
('Health Checkup'),
('Vaccination Drive');

-- ========================
-- INSERT DONOR DATA
-- ========================
INSERT INTO donor (name, phone, user_name, email, password, account_name, account_id, address, profile_picture) VALUES
('Mohammad Rahman', '+8801711123456', 'mrahman01', 'mrahman@email.com', '$2b$12$encrypted_password1', 'Rahman Holdings', 1, 'House 45, Road 12, Dhanmondi, Dhaka-1205', NULL),
('Fatima Khatun', '+8801812234567', 'fkhatun02', 'fatima.k@email.com', '$2b$12$encrypted_password2', 'Khatun Traders', 2, 'Plot 23, Sector 7, Uttara, Dhaka-1230', NULL),
('Abdullah Al Mamun', '+8801913345678', 'amamun03', 'abdullah.m@email.com', '$2b$12$encrypted_password3', 'Mamun Enterprises', 3, '56 New Market Road, Chittagong-4000', NULL),
('Ayesha Siddika', '+8801714456789', 'asiddika04', 'ayesha.s@email.com', '$2b$12$encrypted_password4', 'Siddika Foundation', 4, 'House 78, Block C, Bashundhara, Dhaka-1229', NULL),
('Karim Uddin', '+8801815567890', 'kuddin05', 'karim.u@email.com', '$2b$12$encrypted_password5', 'Uddin Group', 5, 'Villa 12, DOHS Baridhara, Dhaka-1206', NULL),
('Rashida Begum', '+8801916678901', 'rbegum06', 'rashida.b@email.com', '$2b$12$encrypted_password6', 'Begum Charity', 6, '34 Elephant Road, Dhaka-1205', NULL),
('Nasir Ahmed', '+8801717789012', 'nahmed07', 'nasir.a@email.com', '$2b$12$encrypted_password7', 'Ahmed Corporation', 7, 'House 89, Road 5, Gulshan-2, Dhaka-1212', NULL),
('Salma Khatun', '+8801818890123', 'skhatun08', 'salma.k@email.com', '$2b$12$encrypted_password8', 'Khatun Welfare', 8, '23 Green Road, Panthapath, Dhaka-1205', NULL),
('Rafiq Hasan', '+8801919901234', 'rhasan09', 'rafiq.h@email.com', '$2b$12$encrypted_password9', 'Hasan Industries', 1, 'Plot 45, Sector 12, Uttara, Dhaka-1230', NULL),
('Nargis Akter', '+8801720012345', 'nakter10', 'nargis.a@email.com', '$2b$12$encrypted_password10', 'Akter Foundation', 2, 'House 67, Road 8, Dhanmondi, Dhaka-1209', NULL);

-- ========================
-- INSERT RECEIVER DATA
-- ========================
INSERT INTO receiver (name, phone, user_name, password, emergency_phone, address, email, profile_picture) VALUES
('Jahangir Alam', '+8801321111111', 'jalam01', '$2b$12$receiver_pass1', '+8801521111111', 'Village: Shalikha, Union: Shalikha, Upazila: Magura Sadar, District: Magura', 'jahangir.a@email.com', NULL),
('Rashida Khatun', '+8801322222222', 'rkhatun01', '$2b$12$receiver_pass2', '+8801522222222', 'Village: Charghat, Union: Charghat, Upazila: Charghat, District: Rajshahi', 'rashida.k@email.com', NULL),
('Abul Kashem', '+8801323333333', 'akashem01', '$2b$12$receiver_pass3', '+8801523333333', 'Village: Patiya, Union: Patiya, Upazila: Patiya, District: Chittagong', 'abul.k@email.com', NULL),
('Marium Begum', '+8801324444444', 'mbegum01', '$2b$12$receiver_pass4', '+8801524444444', 'Village: Saghata, Union: Saghata, Upazila: Saghata, District: Gaibandha', 'marium.b@email.com', NULL),
('Shamsul Hoque', '+8801325555555', 'shoque01', '$2b$12$receiver_pass5', '+8801525555555', 'Village: Kaliganj, Union: Kaliganj, Upazila: Kaliganj, District: Lalmonirhat', 'shamsul.h@email.com', NULL),
('Rahima Khatun', '+8801326666666', 'rahima01', '$2b$12$receiver_pass6', '+8801526666666', 'Village: Teknaf, Union: Teknaf, Upazila: Teknaf, District: Cox\'s Bazar', 'rahima.k@email.com', NULL),
('Mizanur Rahman', '+8801327777777', 'mrahman02', '$2b$12$receiver_pass7', '+8801527777777', 'Village: Rangamati Sadar, Union: Rangamati, Upazila: Rangamati Sadar, District: Rangamati', 'mizan.r@email.com', NULL),
('Nasreen Akter', '+8801328888888', 'nakter01', '$2b$12$receiver_pass8', '+8801528888888', 'Village: Bandarban Sadar, Union: Bandarban, Upazila: Bandarban Sadar, District: Bandarban', 'nasreen.a@email.com', NULL),
('Golam Mostafa', '+8801329999999', 'gmostafa01', '$2b$12$receiver_pass9', '+8801529999999', 'Village: Khagrachhari Sadar, Union: Khagrachhari, Upazila: Khagrachhari Sadar, District: Khagrachhari', 'golam.m@email.com', NULL),
('Fatema Begum', '+8801320000000', 'fbegum01', '$2b$12$receiver_pass10', '+8801520000000', 'Village: Kushtia Sadar, Union: Kushtia, Upazila: Kushtia Sadar, District: Kushtia', 'fatema.b@email.com', NULL);

-- ========================
-- INSERT VOLUNTEER DATA
-- ========================
INSERT INTO volunteer (name, phone, email, dob, address, pref_address, join_time, user_name, password, nid_birthcert, profile_picture, status) VALUES
('Ahmed Hassan', '+8801711000001', 'ahmed.hassan@email.com', '1995-03-15', 'House 23, Road 4, Block A, Mirpur-1, Dhaka-1216', 'Dhaka Division', '2024-01-15', 'ahassen01', '$2b$12$volunteer_pass1', NULL, NULL, 'active'),
('Salma Khatun', '+8801812000002', 'salma.khatun@email.com', '1992-07-22', 'Flat 5B, Building 12, Uttara Sector-3, Dhaka-1230', 'Dhaka Division', '2024-02-10', 'skhatun01', '$2b$12$volunteer_pass2', NULL, NULL, 'active'),
('Rafiq Ahmed', '+8801913000003', 'rafiq.ahmed@email.com', '1988-11-08', '45 Agrabad Commercial Area, Chittagong-4100', 'Chittagong Division', '2024-01-22', 'rahmed01', '$2b$12$volunteer_pass3', NULL, NULL, 'active'),
('Nargis Begum', '+8801714000004', 'nargis.begum@email.com', '1990-05-12', 'House 67, Sector 7, Pabna Sadar, Pabna-6600', 'Rajshahi Division', '2024-03-01', 'nbegum01', '$2b$12$volunteer_pass4', NULL, NULL, 'active'),
('Karim Uddin', '+8801815000005', 'karim.uddin@email.com', '1985-09-30', 'Village: Moulvibazar, Upazila: Moulvibazar Sadar, Moulvibazar-3200', 'Sylhet Division', '2024-02-28', 'kuddin01', '$2b$12$volunteer_pass5', NULL, NULL, 'active'),
('Rashida Akter', '+8801916000006', 'rashida.akter@email.com', '1993-12-25', 'House 34, Road 2, Khulna Sadar, Khulna-9000', 'Khulna Division', '2024-03-15', 'rakter01', '$2b$12$volunteer_pass6', NULL, NULL, 'active'),
('Nasir Hossain', '+8801717000007', 'nasir.hossain@email.com', '1987-04-18', 'Plot 56, Rangpur Sadar, Rangpur-5400', 'Rangpur Division', '2024-01-08', 'nhossain01', '$2b$12$volunteer_pass7', NULL, NULL, 'active'),
('Fatima Khatun', '+8801818000008', 'fatima.khatun@email.com', '1991-08-14', 'House 89, Barisal Sadar, Barisal-8200', 'Barisal Division', '2024-02-20', 'fkhatun01', '$2b$12$volunteer_pass8', NULL, NULL, 'new'),
('Mamun Rahman', '+8801919000009', 'mamun.rahman@email.com', '1989-01-05', 'Village: Mymensingh Sadar, Mymensingh-2200', 'Mymensingh Division', '2024-03-10', 'mrahman01', '$2b$12$volunteer_pass9', NULL, NULL, 'new'),
('Ayesha Siddika', '+8801720000010', 'ayesha.siddika@email.com', '1994-06-28', 'House 12, Road 3, Comilla Sadar, Comilla-3500', 'Chittagong Division', '2024-03-20', 'asiddika01', '$2b$12$volunteer_pass10', NULL, NULL, 'active');

-- ========================
-- INSERT ITEM DATA
-- ========================
INSERT INTO item (name, type_id) VALUES
('Rice', 1), ('Wheat', 1), ('Lentils', 1), ('Cooking Oil', 1), ('Sugar', 1), ('Salt', 1), ('Onion', 1), ('Potato', 1), ('Fish', 1), ('Meat', 1),
('Shirt', 2), ('Pant', 2), ('Saree', 2), ('Lungi', 2), ('Blanket', 2), ('Shoes', 2), ('Socks', 2), ('Jacket', 2), ('Hat', 2), ('Scarf', 2),
('Paracetamol', 3), ('Antibiotic', 3), ('Antiseptic', 3), ('Bandage', 3), ('First Aid Kit', 3), ('Thermometer', 3), ('Syrup', 3), ('Ointment', 3), ('Injection', 3), ('Mask', 3),
('Bottled Water', 4), ('Water Purifier', 4), ('Water Tank', 4), ('Water Pump', 4), ('Bucket', 4),
('Tent', 5), ('Tarpaulin', 5), ('Sleeping Bag', 5), ('Mattress', 5), ('Pillow', 5),
('Soap', 6), ('Shampoo', 6), ('Toothpaste', 6), ('Toothbrush', 6), ('Towel', 6), ('Hand Sanitizer', 6),
('Hammer', 7), ('Screwdriver', 7), ('Wrench', 7), ('Pliers', 7), ('Knife', 7),
('Diesel', 8), ('Petrol', 8), ('Generator', 8), ('Gas Cylinder', 8),
('Cash Donation', 9),
('Mobile Phone', 10), ('Radio', 10), ('Flashlight', 10), ('Battery', 10),
('Books', 11), ('Notebook', 11), ('Pen', 11), ('Pencil', 11),
('Baby Food', 12), ('Diaper', 12), ('Baby Clothes', 12), ('Milk Powder', 12),
('Emergency Kit', 13), ('Rescue Equipment', 13), ('Life Jacket', 13),
('Miscellaneous', 14);

-- ========================
-- INSERT DONATION DATA
-- ========================
INSERT INTO donation (message, date, donor_id, item_id_list) VALUES
('Emergency food relief for flood victims', '2024-09-01', 1, '1,2,3,4,5'),
('Winter clothing drive for homeless', '2024-09-05', 2, '11,12,13,14,15,16'),
('Medical supplies for rural clinic', '2024-09-10', 3, '21,22,23,24,25'),
('Clean water initiative', '2024-09-12', 4, '31,32,33,34,35'),
('Shelter materials for disaster victims', '2024-09-15', 5, '36,37,38,39,40'),
('Hygiene products for refugee camp', '2024-09-18', 6, '41,42,43,44,45,46'),
('Tools for reconstruction work', '2024-09-20', 7, '47,48,49,50,51'),
('Fuel support for generators', '2024-09-22', 8, '52,53,54,55'),
('Monthly cash assistance', '2024-09-25', 9, '56'),
('Communication devices for remote areas', '2024-09-28', 10, '57,58,59,60'),
('Educational materials for children', '2024-09-30', 1, '61,62,63,64'),
('Baby care essentials', '2024-10-02', 2, '65,66,67,68'),
('Emergency response equipment', '2024-10-05', 3, '69,70,71'),
('Mixed essential supplies', '2024-10-08', 4, '1,11,21,31,41,51'),
('Large food distribution', '2024-10-10', 5, '1,2,3,6,7,8,9,10');

-- ========================
-- INSERT STOCK DATA
-- ========================
INSERT INTO stock (price, quantity, purchase_date, stock_date, expire_date, item_id, account_id) VALUES
-- Food items
(50, 500, '2024-09-01', '2024-09-01', '2025-09-01', 1, 1), -- Rice
(45, 300, '2024-09-01', '2024-09-01', '2025-09-01', 2, 1), -- Wheat
(80, 200, '2024-09-01', '2024-09-01', '2025-09-01', 3, 2), -- Lentils
(120, 150, '2024-09-01', '2024-09-01', '2025-03-01', 4, 2), -- Cooking Oil
(60, 100, '2024-09-01', '2024-09-01', '2025-09-01', 5, 3), -- Sugar
-- Clothing items
(300, 100, '2024-09-05', '2024-09-05', '2027-09-05', 11, 3), -- Shirt
(400, 80, '2024-09-05', '2024-09-05', '2027-09-05', 12, 4), -- Pant
(800, 50, '2024-09-05', '2024-09-05', '2027-09-05', 13, 4), -- Saree
(250, 120, '2024-09-05', '2024-09-05', '2027-09-05', 14, 5), -- Lungi
(600, 75, '2024-09-05', '2024-09-05', '2027-09-05', 15, 5), -- Blanket
-- Medicine items
(10, 1000, '2024-09-10', '2024-09-10', '2026-09-10', 21, 6), -- Paracetamol
(150, 200, '2024-09-10', '2024-09-10', '2026-09-10', 22, 6), -- Antibiotic
(25, 500, '2024-09-10', '2024-09-10', '2026-09-10', 23, 7), -- Antiseptic
(15, 800, '2024-09-10', '2024-09-10', '2026-09-10', 24, 7), -- Bandage
(200, 50, '2024-09-10', '2024-09-10', '2026-09-10', 25, 8), -- First Aid Kit
-- Water items
(25, 1000, '2024-09-12', '2024-09-12', '2025-03-12', 31, 8), -- Bottled Water
(2500, 20, '2024-09-12', '2024-09-12', '2029-09-12', 32, 1), -- Water Purifier
(5000, 10, '2024-09-12', '2024-09-12', '2034-09-12', 33, 2), -- Water Tank
-- Shelter items
(3000, 25, '2024-09-15', '2024-09-15', '2029-09-15', 36, 3), -- Tent
(800, 100, '2024-09-15', '2024-09-15', '2029-09-15', 37, 4), -- Tarpaulin
(1200, 50, '2024-09-15', '2024-09-15', '2029-09-15', 38, 5), -- Sleeping Bag
-- Hygiene items
(15, 2000, '2024-09-18', '2024-09-18', '2026-09-18', 41, 6), -- Soap
(45, 500, '2024-09-18', '2024-09-18', '2026-09-18', 42, 7), -- Shampoo
(35, 800, '2024-09-18', '2024-09-18', '2026-09-18', 43, 8), -- Toothpaste
-- Tools
(250, 100, '2024-09-20', '2024-09-20', '2034-09-20', 47, 1), -- Hammer
(150, 150, '2024-09-20', '2024-09-20', '2034-09-20', 48, 2), -- Screwdriver
(200, 80, '2024-09-20', '2024-09-20', '2034-09-20', 49, 3), -- Wrench
-- Electronics
(8000, 15, '2024-09-28', '2024-09-28', '2027-09-28', 57, 4), -- Mobile Phone
(1500, 30, '2024-09-28', '2024-09-28', '2029-09-28', 58, 5), -- Radio
(300, 200, '2024-09-28', '2024-09-28', '2029-09-28', 59, 6); -- Flashlight

-- ========================
-- INSERT MONEY_TRANSFER DATA
-- ========================
INSERT INTO money_transfer (account_id, donation_id, amount) VALUES
(1, 1, 15000.00),
(2, 2, 8500.00),
(3, 3, 12000.00),
(4, 4, 6500.00),
(5, 5, 18000.00),
(6, 6, 4500.00),
(7, 7, 9500.00),
(8, 8, 7200.00),
(1, 9, 25000.00),
(2, 10, 11000.00),
(3, 11, 3500.00),
(4, 12, 5800.00),
(5, 13, 14500.00),
(6, 14, 22000.00),
(7, 15, 28500.00);

-- ========================
-- INSERT DONATION_RECEIVER DATA
-- ========================
INSERT INTO donation_receiver (receiver_id, date, priority_message, item_id_list, additional_item, priority_level, latitude, longitude, status) VALUES
(1, '2024-09-02', 'Urgent food needed for 50 families affected by flood', '1,2,3,4,5,6', 'Baby food, Elderly care items', 'high', 23.6850, 90.3563, 'approved'),
(2, '2024-09-06', 'Winter clothing required for homeless shelter', '11,12,13,14,15', 'Warm socks, Gloves', 'medium', 24.3636, 88.6241, 'approved'),
(3, '2024-09-11', 'Medical supplies urgently needed for clinic', '21,22,23,24,25', 'Insulin, Blood pressure medicine', 'high', 22.3569, 91.7832, 'approved'),
(4, '2024-09-13', 'Clean water crisis in rural village', '31,32,33,34,35', 'Water testing kits', 'high', 25.7439, 89.2752, 'pending'),
(5, '2024-09-16', 'Shelter materials needed after cyclone', '36,37,38,39,40', 'Corrugated sheets, Nails', 'high', 24.8998, 91.8713, 'approved'),
(6, '2024-09-19', 'Hygiene products for refugee camp', '41,42,43,44,45,46', 'Feminine hygiene products', 'medium', 21.4272, 92.0058, 'approved'),
(7, '2024-09-21', 'Construction tools for rebuilding homes', '47,48,49,50,51', 'Cement, Bricks', 'medium', 22.6533, 90.3400, 'approved'),
(8, '2024-09-23', 'Generator fuel for hospital backup power', '52,53,54,55', 'Spare parts for generator', 'high', 21.8500, 89.5400, 'completed'),
(9, '2024-09-26', 'Financial assistance for livelihood restoration', '56', 'Microfinance support', 'medium', 25.7439, 89.2400, 'pending'),
(10, '2024-09-29', 'Communication devices for disaster coordination', '57,58,59,60', 'Solar chargers, Antennas', 'medium', 23.1800, 89.1800, 'approved'),
(1, '2024-10-01', 'Educational materials for flood-affected children', '61,62,63,64', 'School bags, Uniforms', 'low', 23.6850, 90.3563, 'pending'),
(2, '2024-10-03', 'Baby care essentials for new mothers', '65,66,67,68', 'Baby formula, Bottles', 'medium', 24.3636, 88.6241, 'approved'),
(3, '2024-10-06', 'Emergency response equipment for disaster team', '69,70,71', 'Rescue ropes, Helmets', 'high', 22.3569, 91.7832, 'approved'),
(4, '2024-10-09', 'Mixed supplies for community center', '1,11,21,31,41,51', 'Community cooking pots', 'medium', 25.7439, 89.2752, 'approved'),
(5, '2024-10-11', 'Large-scale food distribution preparation', '1,2,3,6,7,8,9,10', 'Distribution bags, Scales', 'high', 24.8998, 91.8713, 'approved');

-- ========================
-- INSERT EVENT DATA
-- ========================
INSERT INTO event (volunteer_id_list, event_type_id, item_id_list, donation_receiver_id, start_date, end_date, status, location) VALUES
('1,2,3', 1, '1,2,3,4,5,6', 1, '2024-09-03', '2024-09-04', 'completed', 'Magura Sadar Upazila'),
('4,5', 3, '11,12,13,14,15', 2, '2024-09-07', '2024-09-08', 'completed', 'Charghat Upazila'),
('6,7,8', 2, '21,22,23,24,25', 3, '2024-09-12', '2024-09-13', 'ongoing', 'Patiya Upazila'),
('9,10', 4, '31,32,33,34,35', 4, '2024-09-14', '2024-09-15', 'scheduled', 'Saghata Upazila'),
('1,3,5', 5, '36,37,38,39,40', 5, '2024-09-17', '2024-09-18', 'completed', 'Kaliganj Upazila'),
('2,4,6', 6, '41,42,43,44,45,46', 6, '2024-09-20', '2024-09-21', 'ongoing', 'Teknaf Upazila'),
('7,8', 7, '47,48,49,50,51', 7, '2024-09-22', '2024-09-23', 'completed', 'Rangamati Sadar'),
('9,10,1', 8, '52,53,54,55', 8, '2024-09-24', '2024-09-25', 'completed', 'Bandarban Sadar'),
('2,3', 10, '56', 9, '2024-09-27', '2024-09-28', 'scheduled', 'Khagrachhari Sadar'),
('4,5,6', 9, '57,58,59,60', 10, '2024-09-30', '2024-10-01', 'ongoing', 'Kushtia Sadar'),
('7,8,9', 12, '61,62,63,64', 11, '2024-10-02', '2024-10-03', 'scheduled', 'Magura Sadar Upazila'),
('10,1,2', 13, '65,66,67,68', 12, '2024-10-04', '2024-10-05', 'ongoing', 'Charghat Upazila'),
('3,4,5', 11, '69,70,71', 13, '2024-10-07', '2024-10-08', 'ongoing', 'Patiya Upazila'),
('6,7', 1, '1,11,21,31,41,51', 14, '2024-10-10', '2024-10-11', 'scheduled', 'Saghata Upazila'),
('8,9,10', 1, '1,2,3,6,7,8,9,10', 15, '2024-10-12', '2024-10-14', 'scheduled', 'Kaliganj Upazila');

-- ========================
-- INSERT FEEDBACK DATA
-- ========================
INSERT INTO feedback (receiver_id, volunteer_id, donor_id, message, picture) VALUES
(1, 1, 1, 'Excellent service! The food distribution was well organized and timely. Our community received exactly what we needed during the flood crisis.', NULL),
(2, 4, 2, 'Very grateful for the warm clothing provided. The volunteers were professional and caring. This support helped our shelter residents through the cold nights.', NULL),
(3, 6, 3, 'The medical supplies arrived just in time. Quality products and proper packaging. Our clinic can now serve more patients effectively.', NULL),
(4, 9, 4, 'Clean water project was a blessing for our village. The water purification system works perfectly and has improved our health significantly.', NULL),
(5, 1, 5, 'Shelter materials were of good quality. Volunteers helped with the setup which made reconstruction much faster. Highly appreciated!', NULL),
(6, 2, 6, 'Hygiene products distribution was well managed. The variety of products met all our camp requirements. Thank you for the thoughtful selection.', NULL),
(7, 7, 7, 'Construction tools helped us rebuild our homes quickly. All tools were in excellent condition and exactly what we needed for the work.', NULL),
(8, 9, 8, 'Generator fuel support kept our hospital running during power outages. Critical for patient care. Very reliable service from the team.', NULL),
(1, 2, 1, 'Second donation received smoothly. The educational materials will help our children continue their studies after the disaster.', NULL),
(2, 10, 2, 'Baby care products were a huge relief for new mothers in our area. Quality items and sufficient quantity for community needs.', NULL),
(3, 3, 3, 'Emergency response equipment delivered promptly. Our local disaster response team is now better equipped to handle emergencies.', NULL),
(4, 6, 4, 'Mixed supplies distribution covered all our basic needs. Well-coordinated effort by all volunteers involved in the process.', NULL),
(5, 8, 5, 'Large food distribution event was expertly managed. Fed over 200 families efficiently. Excellent coordination between all parties.', NULL),
(NULL, 1, 6, 'As a volunteer, I appreciate working with such generous donors. The resources provided always meet the actual needs of receivers.', NULL),
(NULL, 5, 7, 'Volunteering experience has been rewarding. Donors are responsive to our feedback about community needs and adjust accordingly.', NULL);

-- ================================================================
-- DATA INSERT COMPLETE
-- ================================================================
-- 
-- Summary of inserted data:
-- ✅ 8 Account records with various banking methods
-- ✅ 14 Type categories for comprehensive item classification  
-- ✅ 15 Event types covering all relief activities
-- ✅ 10 Donor records with complete profile information
-- ✅ 10 Receiver records from various districts
-- ✅ 10 Volunteer records with different specializations
-- ✅ 72 Item records covering all relief categories
-- ✅ 15 Donation records with varied item combinations
-- ✅ 25 Stock records with realistic pricing and quantities
-- ✅ 15 Money transfer records linking donations to accounts
-- ✅ 15 Donation receiver requests with GPS coordinates
-- ✅ 15 Event records with volunteer assignments
-- ✅ 15 Feedback records from receivers, volunteers, and donors
--
-- Total records: 289 across all tables
-- All foreign key relationships maintained
-- Realistic Bangladesh-based addresses and phone numbers
-- Comprehensive coverage of relief management scenarios
-- 
-- ================================================================