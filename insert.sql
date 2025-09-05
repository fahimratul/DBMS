-- Insert data into type_list
INSERT INTO type_list (type_name) VALUES ('Food');
INSERT INTO type_list (type_name) VALUES ('Clothing');
INSERT INTO type_list (type_name) VALUES ('Medicine');
INSERT INTO type_list (type_name) VALUES ('Water');
INSERT INTO type_list (type_name) VALUES ('Shelter');
INSERT INTO type_list (type_name) VALUES ('Hygiene');
INSERT INTO type_list (type_name) VALUES ('Tools');
INSERT INTO type_list (type_name) VALUES ('Fuel');
INSERT INTO type_list (type_name) VALUES ('Money');
INSERT INTO type_list (type_name) VALUES ('Other');

-- Insert data into account
INSERT INTO account (account_name, method_name, balance) VALUES ('Main Bank', 'Bank Transfer', 60300.00);
INSERT INTO account (account_name, method_name, balance) VALUES ('Bkash Account', 'Bkash', 37500.00);
INSERT INTO account (account_name, method_name, balance) VALUES ('Nagad Account', 'Nagad', 31200.00);



-- Insert data into event_type
INSERT INTO event_type (event_type) VALUES ('Food Distribution');
INSERT INTO event_type (event_type) VALUES ('Medical Camp');
INSERT INTO event_type (event_type) VALUES ('Clothing Drive');
INSERT INTO event_type (event_type) VALUES ('Water Supply');
INSERT INTO event_type (event_type) VALUES ('Shelter Setup');
INSERT INTO event_type (event_type) VALUES ('Hygiene Awareness');
INSERT INTO event_type (event_type) VALUES ('Tool Distribution');
INSERT INTO event_type (event_type) VALUES ('Fuel Aid');
INSERT INTO event_type (event_type) VALUES ('Communication Support');
INSERT INTO event_type (event_type) VALUES ('General Relief');

-- Insert data into item
INSERT INTO item (name, type_id) VALUES ('Rice', 1);
INSERT INTO item (name, type_id) VALUES ('Blanket', 2);
INSERT INTO item (name, type_id) VALUES ('Paracetamol', 3);
INSERT INTO item (name, type_id) VALUES ('Bottled Water', 4);
INSERT INTO item (name, type_id) VALUES ('Tent', 5);
INSERT INTO item (name, type_id) VALUES ('Hand Sanitizer', 6);
INSERT INTO item (name, type_id) VALUES ('Hammer', 7);
INSERT INTO item (name, type_id) VALUES ('Diesel', 8);
INSERT INTO item (name, type_id) VALUES ('Money Donation', 9);
INSERT INTO item (name, type_id) VALUES ('Emergency Radio', 10);
INSERT INTO item (name, type_id) VALUES ('First Aid Kit', 10);

-- Insert data into donor
INSERT INTO donor (name, phone, user_name, password, account_name, account_id, address, profile_picture) VALUES ('Mohammad', '01712345678', 'mohammad', 'scrypt:32768:8:1$J6QmFgyffiG5AR0f$2303b25e5d5e43e65ec5929e701d0a4f2cb22f0d8939a5729e635744d098018869ec060e95a6cefe811d4c75951d7a3d07ade4be714ead1210a4040d57637416', 'Mohammad', 1, 'Dhaka, Bangladesh', NULL);
INSERT INTO donor (name, phone, user_name, password, account_name, account_id, address, profile_picture) VALUES ('Abdullah', '01812345679', 'abdullah', 'scrypt:32768:8:1$4el3cJ5k0YcrhU4G$b6802d05af7fbcd0e7ee234de5e6478f32ab5f4db1c4a99c9ed80e1a58badcdaa04e7c3b1c95ce0da9b2dcaaf47d67327671c395f9acd27559afe1b68ed9cf0d', 'Abdullah', 2, 'Chittagong, Bangladesh', NULL);
INSERT INTO donor (name, phone, user_name, password, account_name, account_id, address, profile_picture) VALUES ('Fatima', '01912345680', 'fatima', 'scrypt:32768:8:1$ijXlAFnrMmawHJ8S$0b4b9c65d62d5123b9394572e6ef554480f4a97e6efe0a90797a6c81167fbd507dcbdaaea6353eaca7708f6bf2fb8606ea01f0fe02f166c883308757b586dfcf', 'Fatima', 3, 'Khulna, Bangladesh', NULL);
INSERT INTO donor (name, phone, user_name, password, account_name, account_id, address, profile_picture) VALUES ('Ayesha', '01722345681', 'ayesha', 'scrypt:32768:8:1$2bWVIUqFVMvkBFtO$5b64ad2c2fe05f9e66f5b08efe384a3205a37f65c8f720e0e472257ce53d3b60132ea65e6bdfc2c9dd5d9c9fcb7aaa45a8e3df2fd19b170699b7653c42c2e69d', 'Ayesha', 1, 'Rajshahi, Bangladesh', NULL);
INSERT INTO donor (name, phone, user_name, password, account_name, account_id, address, profile_picture) VALUES ('Rahman', '01822345682', 'rahman', 'scrypt:32768:8:1$NHYYZjhT2YaKVBMq$f464243f4d09967c3a78c3d86ddfa034741763f08f7fd6822c8eb28a45c6c8301e01af4f6eff591a9ea722b48a6442ce84a1727018ec0dcb96f03e10810ff57a', 'Rahman', 2, 'Sylhet, Bangladesh', NULL);
INSERT INTO donor (name, phone, user_name, password, account_name, account_id, address, profile_picture) VALUES ('Karim', '01922345683', 'karim', 'scrypt:32768:8:1$YfkXVQQ362jJ8bHw$d6fe75debcc683ef218dfe40157993c7d8faac7f13dcc81a5c1036b7265d3ded2b31e40ac812f6b4b3bc0615ab8e87e8929b7500322aad3dde6404df1239a1ac', 'Karim', 3, 'Barisal, Bangladesh', NULL);
INSERT INTO donor (name, phone, user_name, password, account_name, account_id, address, profile_picture) VALUES ('Sultana', '01732345684', 'sultana', 'scrypt:32768:8:1$25KrZfhNw9pZCfFF$ba80d46ee46fa786d05d6db4a0ff57d6650b909832e72fccab4f92cb20f7ee468305825dc9253ceee8d90e7247efb32920abf12a1a47c8537382bca0821799fc', 'Sultana', 1, 'Rangpur, Bangladesh', NULL);
INSERT INTO donor (name, phone, user_name, password, account_name, account_id, address, profile_picture) VALUES ('Hasan', '01832345685', 'hasan', 'scrypt:32768:8:1$xGXJk7dQpfdQQpU9$164bd16d67930c7537e8da5c987cc3391db173bb7200980bc6474577af925c754fb38328fc3ceb2ef444a8df9ea94c211582153d8ee9324cc38e30df8c1048b7', 'Hasan', 2, 'Comilla, Bangladesh', NULL);
INSERT INTO donor (name, phone, user_name, password, account_name, account_id, address, profile_picture) VALUES ('Nadia', '01932345686', 'nadia', 'scrypt:32768:8:1$MCvGw6ox7dpc7tcb$15d28af47f0565992d25f23030d4fd065dbc59310eddb4ca80c7ab2b82a980bc3f1e6e3179e700d3f5d111f2a1469b4a0d5b7b95db1fdc9ed8eaa2bb37d33ccf', 'Nadia', 3, 'Narayanganj, Bangladesh', NULL);
INSERT INTO donor (name, phone, user_name, password, account_name, account_id, address, profile_picture) VALUES ('Jamal', '01742345687', 'jamal', 'scrypt:32768:8:1$JIwlU8eNL1lJCs6E$773db0b8080644bbf5d164204c32d5f4d02a6244993e3bc90c48d121dd4cb2f5f806266de2f110c0d6f4b53e387a8f0b0da63a5cc1600de6ba83e60755c4d807', 'Jamal', 1, 'Gazipur, Bangladesh', NULL);

-- Insert data into receiver
INSERT INTO receiver (name, phone, user_name, password, emergency_phone, address, email, profile_picture) VALUES ('Mohammad', '01752345688', 'mohammad', 'scrypt:32768:8:1$J6QmFgyffiG5AR0f$2303b25e5d5e43e65ec5929e701d0a4f2cb22f0d8939a5729e635744d098018869ec060e95a6cefe811d4c75951d7a3d07ade4be714ead1210a4040d57637416', '01762345689', 'Dhaka, Bangladesh', 'mohammad@example.com', NULL);
INSERT INTO receiver (name, phone, user_name, password, emergency_phone, address, email, profile_picture) VALUES ('Abdullah', '01852345690', 'abdullah', 'scrypt:32768:8:1$4el3cJ5k0YcrhU4G$b6802d05af7fbcd0e7ee234de5e6478f32ab5f4db1c4a99c9ed80e1a58badcdaa04e7c3b1c95ce0da9b2dcaaf47d67327671c395f9acd27559afe1b68ed9cf0d', '01862345691', 'Chittagong, Bangladesh', 'abdullah@example.com', NULL);
INSERT INTO receiver (name, phone, user_name, password, emergency_phone, address, email, profile_picture) VALUES ('Fatima', '01952345692', 'fatima', 'scrypt:32768:8:1$ijXlAFnrMmawHJ8S$0b4b9c65d62d5123b9394572e6ef554480f4a97e6efe0a90797a6c81167fbd507dcbdaaea6353eaca7708f6bf2fb8606ea01f0fe02f166c883308757b586dfcf', '01962345693', 'Khulna, Bangladesh', 'fatima@example.com', NULL);
INSERT INTO receiver (name, phone, user_name, password, emergency_phone, address, email, profile_picture) VALUES ('Ayesha', '01762345694', 'ayesha', 'scrypt:32768:8:1$2bWVIUqFVMvkBFtO$5b64ad2c2fe05f9e66f5b08efe384a3205a37f65c8f720e0e472257ce53d3b60132ea65e6bdfc2c9dd5d9c9fcb7aaa45a8e3df2fd19b170699b7653c42c2e69d', '01772345695', 'Rajshahi, Bangladesh', 'ayesha@example.com', NULL);
INSERT INTO receiver (name, phone, user_name, password, emergency_phone, address, email, profile_picture) VALUES ('Rahman', '01862345696', 'rahman', 'scrypt:32768:8:1$NHYYZjhT2YaKVBMq$f464243f4d09967c3a78c3d86ddfa034741763f08f7fd6822c8eb28a45c6c8301e01af4f6eff591a9ea722b48a6442ce84a1727018ec0dcb96f03e10810ff57a', '01872345697', 'Sylhet, Bangladesh', 'rahman@example.com', NULL);
INSERT INTO receiver (name, phone, user_name, password, emergency_phone, address, email, profile_picture) VALUES ('Karim', '01962345698', 'karim', 'scrypt:32768:8:1$YfkXVQQ362jJ8bHw$d6fe75debcc683ef218dfe40157993c7d8faac7f13dcc81a5c1036b7265d3ded2b31e40ac812f6b4b3bc0615ab8e87e8929b7500322aad3dde6404df1239a1ac', '01972345699', 'Barisal, Bangladesh', 'karim@example.com', NULL);
INSERT INTO receiver (name, phone, user_name, password, emergency_phone, address, email, profile_picture) VALUES ('Sultana', '01772345700', 'sultana', 'scrypt:32768:8:1$25KrZfhNw9pZCfFF$ba80d46ee46fa786d05d6db4a0ff57d6650b909832e72fccab4f92cb20f7ee468305825dc9253ceee8d90e7247efb32920abf12a1a47c8537382bca0821799fc', '01782345701', 'Rangpur, Bangladesh', 'sultana@example.com', NULL);
INSERT INTO receiver (name, phone, user_name, password, emergency_phone, address, email, profile_picture) VALUES ('Hasan', '01872345702', 'hasan', 'scrypt:32768:8:1$xGXJk7dQpfdQQpU9$164bd16d67930c7537e8da5c987cc3391db173bb7200980bc6474577af925c754fb38328fc3ceb2ef444a8df9ea94c211582153d8ee9324cc38e30df8c1048b7', '01882345703', 'Comilla, Bangladesh', 'hasan@example.com', NULL);
INSERT INTO receiver (name, phone, user_name, password, emergency_phone, address, email, profile_picture) VALUES ('Nadia', '01972345704', 'nadia', 'scrypt:32768:8:1$MCvGw6ox7dpc7tcb$15d28af47f0565992d25f23030d4fd065dbc59310eddb4ca80c7ab2b82a980bc3f1e6e3179e700d3f5d111f2a1469b4a0d5b7b95db1fdc9ed8eaa2bb37d33ccf', '01982345705', 'Narayanganj, Bangladesh', 'nadia@example.com', NULL);
INSERT INTO receiver (name, phone, user_name, password, emergency_phone, address, email, profile_picture) VALUES ('Jamal', '01782345706', 'jamal', 'scrypt:32768:8:1$JIwlU8eNL1lJCs6E$773db0b8080644bbf5d164204c32d5f4d02a6244993e3bc90c48d121dd4cb2f5f806266de2f110c0d6f4b53e387a8f0b0da63a5cc1600de6ba83e60755c4d807', '01792345707', 'Gazipur, Bangladesh', 'jamal@example.com', NULL);

-- Insert data into volunteer
INSERT INTO volunteer (name, phone, email, dob, address, pref_address, join_time, user_name, password, nid_birthcert, profile_picture, status) VALUES ('Mohammad', '01792345708', 'mohammad@example.com', '1990-01-01', 'Dhaka, Bangladesh', 'Chittagong, Bangladesh', '2024-10-01', 'mohammad', 'scrypt:32768:8:1$J6QmFgyffiG5AR0f$2303b25e5d5e43e65ec5929e701d0a4f2cb22f0d8939a5729e635744d098018869ec060e95a6cefe811d4c75951d7a3d07ade4be714ead1210a4040d57637416', NULL, NULL, 'new');
INSERT INTO volunteer (name, phone, email, dob, address, pref_address, join_time, user_name, password, nid_birthcert, profile_picture, status) VALUES ('Abdullah', '01892345709', 'abdullah@example.com', '1991-02-15', 'Chittagong, Bangladesh', 'Khulna, Bangladesh', '2024-11-15', 'abdullah', 'scrypt:32768:8:1$4el3cJ5k0YcrhU4G$b6802d05af7fbcd0e7ee234de5e6478f32ab5f4db1c4a99c9ed80e1a58badcdaa04e7c3b1c95ce0da9b2dcaaf47d67327671c395f9acd27559afe1b68ed9cf0d', NULL, NULL, 'active');
INSERT INTO volunteer (name, phone, email, dob, address, pref_address, join_time, user_name, password, nid_birthcert, profile_picture, status) VALUES ('Fatima', '01992345710', 'fatima@example.com', '1992-03-20', 'Khulna, Bangladesh', 'Rajshahi, Bangladesh', '2024-12-20', 'fatima', 'scrypt:32768:8:1$ijXlAFnrMmawHJ8S$0b4b9c65d62d5123b9394572e6ef554480f4a97e6efe0a90797a6c81167fbd507dcbdaaea6353eaca7708f6bf2fb8606ea01f0fe02f166c883308757b586dfcf', NULL, NULL, 'new');
INSERT INTO volunteer (name, phone, email, dob, address, pref_address, join_time, user_name, password, nid_birthcert, profile_picture, status) VALUES ('Ayesha', '01702345711', 'ayesha@example.com', '1993-04-25', 'Rajshahi, Bangladesh', 'Sylhet, Bangladesh', '2024-01-25', 'ayesha', 'scrypt:32768:8:1$2bWVIUqFVMvkBFtO$5b64ad2c2fe05f9e66f5b08efe384a3205a37f65c8f720e0e472257ce53d3b60132ea65e6bdfc2c9dd5d9c9fcb7aaa45a8e3df2fd19b170699b7653c42c2e69d', NULL, NULL, 'active');
INSERT INTO volunteer (name, phone, email, dob, address, pref_address, join_time, user_name, password, nid_birthcert, profile_picture, status) VALUES ('Rahman', '01802345712', 'rahman@example.com', '1994-05-30', 'Sylhet, Bangladesh', 'Barisal, Bangladesh', '2024-02-28', 'rahman', 'scrypt:32768:8:1$NHYYZjhT2YaKVBMq$f464243f4d09967c3a78c3d86ddfa034741763f08f7fd6822c8eb28a45c6c8301e01af4f6eff591a9ea722b48a6442ce84a1727018ec0dcb96f03e10810ff57a', NULL, NULL, 'new');
INSERT INTO volunteer (name, phone, email, dob, address, pref_address, join_time, user_name, password, nid_birthcert, profile_picture, status) VALUES ('Karim', '01902345713', 'karim@example.com', '1995-06-10', 'Barisal, Bangladesh', 'Rangpur, Bangladesh', '2024-03-15', 'karim', 'scrypt:32768:8:1$YfkXVQQ362jJ8bHw$d6fe75debcc683ef218dfe40157993c7d8faac7f13dcc81a5c1036b7265d3ded2b31e40ac812f6b4b3bc0615ab8e87e8929b7500322aad3dde6404df1239a1ac', NULL, NULL, 'active');
INSERT INTO volunteer (name, phone, email, dob, address, pref_address, join_time, user_name, password, nid_birthcert, profile_picture, status) VALUES ('Sultana', '01712345714', 'sultana@example.com', '1996-07-05', 'Rangpur, Bangladesh', 'Comilla, Bangladesh', '2024-04-10', 'sultana', 'scrypt:32768:8:1$25KrZfhNw9pZCfFF$ba80d46ee46fa786d05d6db4a0ff57d6650b909832e72fccab4f92cb20f7ee468305825dc9253ceee8d90e7247efb32920abf12a1a47c8537382bca0821799fc', NULL, NULL, 'new');
INSERT INTO volunteer (name, phone, email, dob, address, pref_address, join_time, user_name, password, nid_birthcert, profile_picture, status) VALUES ('Hasan', '01812345715', 'hasan@example.com', '1997-08-12', 'Comilla, Bangladesh', 'Narayanganj, Bangladesh', '2024-05-20', 'hasan', 'scrypt:32768:8:1$xGXJk7dQpfdQQpU9$164bd16d67930c7537e8da5c987cc3391db173bb7200980bc6474577af925c754fb38328fc3ceb2ef444a8df9ea94c211582153d8ee9324cc38e30df8c1048b7', NULL, NULL, 'active');
INSERT INTO volunteer (name, phone, email, dob, address, pref_address, join_time, user_name, password, nid_birthcert, profile_picture, status) VALUES ('Nadia', '01912345716', 'nadia@example.com', '1998-09-18', 'Narayanganj, Bangladesh', 'Gazipur, Bangladesh', '2024-06-25', 'nadia', 'scrypt:32768:8:1$MCvGw6ox7dpc7tcb$15d28af47f0565992d25f23030d4fd065dbc59310eddb4ca80c7ab2b82a980bc3f1e6e3179e700d3f5d111f2a1469b4a0d5b7b95db1fdc9ed8eaa2bb37d33ccf', NULL, NULL, 'new');
INSERT INTO volunteer (name, phone, email, dob, address, pref_address, join_time, user_name, password, nid_birthcert, profile_picture, status) VALUES ('Jamal', '01722345717', 'jamal@example.com', '1999-10-22', 'Gazipur, Bangladesh', 'Dhaka, Bangladesh', '2024-07-30', 'jamal', 'scrypt:32768:8:1$JIwlU8eNL1lJCs6E$773db0b8080644bbf5d164204c32d5f4d02a6244993e3bc90c48d121dd4cb2f5f806266de2f110c0d6f4b53e387a8f0b0da63a5cc1600de6ba83e60755c4d807', NULL, NULL, 'active');

-- Insert data into donation
INSERT INTO donation (message, date, donor_id, item_id_list) VALUES ('Helping with food', '2024-10-01', 1, '1');
INSERT INTO donation (message, date, donor_id, item_id_list) VALUES ('Clothing donation', '2024-11-15', 2, '2');
INSERT INTO donation (message, date, donor_id, item_id_list) VALUES ('Medical supplies', '2024-12-20', 3, '3');
INSERT INTO donation (message, date, donor_id, item_id_list) VALUES ('Water bottles', '2024-01-25', 4, '4');
INSERT INTO donation (message, date, donor_id, item_id_list) VALUES ('Shelter materials', '2024-02-28', 5, '5');
INSERT INTO donation (message, date, donor_id, item_id_list) VALUES ('Hygiene products', '2024-03-15', 6, '6');
INSERT INTO donation (message, date, donor_id, item_id_list) VALUES ('Tools for rebuilding', '2024-04-10', 7, '7');
INSERT INTO donation (message, date, donor_id, item_id_list) VALUES ('Fuel for generators', '2024-05-20', 8, '8');
INSERT INTO donation (message, date, donor_id, item_id_list) VALUES ('Cash donation for emergency relief', '2024-06-25', 9, '9');
INSERT INTO donation (message, date, donor_id, item_id_list) VALUES ('Emergency radio equipment', '2024-07-30', 10, '10');
INSERT INTO donation (message, date, donor_id, item_id_list) VALUES ('Medical aid funds', '2024-08-15', 1, '9');
INSERT INTO donation (message, date, donor_id, item_id_list) VALUES ('Emergency cash support', '2024-09-01', 3, '9');
INSERT INTO donation (message, date, donor_id, item_id_list) VALUES ('New Year relief fund', '2025-01-05', 2, '9');
INSERT INTO donation (message, date, donor_id, item_id_list) VALUES ('Winter emergency money', '2025-01-20', 5, '9');
INSERT INTO donation (message, date, donor_id, item_id_list) VALUES ('Spring disaster fund', '2025-03-10', 7, '9');
INSERT INTO donation (message, date, donor_id, item_id_list) VALUES ('Summer relief cash', '2025-07-15', 4, '9');
INSERT INTO donation (message, date, donor_id, item_id_list) VALUES ('Monsoon emergency fund', '2025-07-28', 6, '9');

-- Insert data into money_transfer
INSERT INTO money_transfer (account_id, donation_id, amount) VALUES (3, 9, 700.00);
INSERT INTO money_transfer (account_id, donation_id, amount) VALUES (1, 11, 2500.00);
INSERT INTO money_transfer (account_id, donation_id, amount) VALUES (2, 12, 3000.00);
INSERT INTO money_transfer (account_id, donation_id, amount) VALUES (1, 13, 1800.00);
INSERT INTO money_transfer (account_id, donation_id, amount) VALUES (3, 14, 2200.00);
INSERT INTO money_transfer (account_id, donation_id, amount) VALUES (2, 15, 1500.00);
INSERT INTO money_transfer (account_id, donation_id, amount) VALUES (1, 16, 3500.00);
INSERT INTO money_transfer (account_id, donation_id, amount) VALUES (3, 17, 2800.00);

-- Insert data into stock
INSERT INTO stock (price, quantity, purchase_date, stock_date, expire_date, item_id) VALUES (50, 100, '2024-10-01', '2024-10-01', '2025-10-01', 1);
INSERT INTO stock (price, quantity, purchase_date, stock_date, expire_date, item_id) VALUES (20, 200, '2024-11-15', '2024-11-15', '2025-11-15', 2);
INSERT INTO stock (price, quantity, purchase_date, stock_date, expire_date, item_id) VALUES (10, 500, '2024-12-20', '2024-12-20', '2025-12-20', 3);
INSERT INTO stock (price, quantity, purchase_date, stock_date, expire_date, item_id) VALUES (5, 1000, '2024-01-25', '2024-01-25', '2025-01-25', 4);
INSERT INTO stock (price, quantity, purchase_date, stock_date, expire_date, item_id) VALUES (100, 50, '2024-02-28', '2024-02-28', '2025-02-28', 5);
INSERT INTO stock (price, quantity, purchase_date, stock_date, expire_date, item_id) VALUES (15, 300, '2024-03-15', '2024-03-15', '2025-03-15', 6);
INSERT INTO stock (price, quantity, purchase_date, stock_date, expire_date, item_id) VALUES (30, 150, '2024-04-10', '2024-04-10', '2025-04-10', 7);
INSERT INTO stock (price, quantity, purchase_date, stock_date, expire_date, item_id) VALUES (40, 80, '2024-05-20', '2024-05-20', '2025-05-20', 8);
INSERT INTO stock (price, quantity, purchase_date, stock_date, expire_date, item_id) VALUES (25, 120, '2024-06-25', '2024-06-25', '2025-06-25', 9);
INSERT INTO stock (price, quantity, purchase_date, stock_date, expire_date, item_id) VALUES (60, 70, '2024-07-30', '2024-07-30', '2025-07-30', 10);

-- Insert data into donation_receiver
INSERT INTO donation_receiver (receiver_id, date, priority_message, item_id_list, additional_item) VALUES (1, '2024-10-01', 'High priority', '1', 'Extra rice');
INSERT INTO donation_receiver (receiver_id, date, priority_message, item_id_list, additional_item) VALUES (2, '2024-11-15', 'Medium priority', '2', 'Warm blanket');
INSERT INTO donation_receiver (receiver_id, date, priority_message, item_id_list, additional_item) VALUES (3, '2024-12-20', 'Urgent', '3', 'Pain relievers');
INSERT INTO donation_receiver (receiver_id, date, priority_message, item_id_list, additional_item) VALUES (4, '2024-01-25', 'Normal', '4', 'Clean water');
INSERT INTO donation_receiver (receiver_id, date, priority_message, item_id_list, additional_item) VALUES (5, '2024-02-28', 'High', '5', 'Tent accessories');
INSERT INTO donation_receiver (receiver_id, date, priority_message, item_id_list, additional_item) VALUES (6, '2024-03-15', 'Medium', '6', 'Soap bars');
INSERT INTO donation_receiver (receiver_id, date, priority_message, item_id_list, additional_item) VALUES (7, '2024-04-10', 'Urgent', '7', 'Nails');
INSERT INTO donation_receiver (receiver_id, date, priority_message, item_id_list, additional_item) VALUES (8, '2024-05-20', 'Normal', '8', 'Fuel cans');
INSERT INTO donation_receiver (receiver_id, date, priority_message, item_id_list, additional_item) VALUES (9, '2024-06-25', 'High', '9', 'Batteries');
INSERT INTO donation_receiver (receiver_id, date, priority_message, item_id_list, additional_item) VALUES (10, '2024-07-30', 'Medium', '10', 'Bandages');

-- Insert data into event
INSERT INTO event (volunteer_id_list, event_type_id, item_id_list, donation_receiver_id, start_date, end_date, status) VALUES ('1', 1, '1', 1, '2024-10-01', '2024-10-05', 'Completed');
INSERT INTO event (volunteer_id_list, event_type_id, item_id_list, donation_receiver_id, start_date, end_date, status) VALUES ('2', 2, '2', 2, '2024-11-15', '2024-11-20', 'Completed');
INSERT INTO event (volunteer_id_list, event_type_id, item_id_list, donation_receiver_id, start_date, end_date, status) VALUES ('3', 3, '3', 3, '2024-12-20', '2024-12-25', 'Completed');
INSERT INTO event (volunteer_id_list, event_type_id, item_id_list, donation_receiver_id, start_date, end_date, status) VALUES ('4', 4, '4', 4, '2024-01-25', '2024-01-30', 'Completed');
INSERT INTO event (volunteer_id_list, event_type_id, item_id_list, donation_receiver_id, start_date, end_date, status) VALUES ('5', 5, '5', 5, '2024-02-28', '2024-03-05', 'Completed');
INSERT INTO event (volunteer_id_list, event_type_id, item_id_list, donation_receiver_id, start_date, end_date, status) VALUES ('6', 6, '6', 6, '2024-03-15', '2024-03-20', 'Completed');
INSERT INTO event (volunteer_id_list, event_type_id, item_id_list, donation_receiver_id, start_date, end_date, status) VALUES ('7', 7, '7', 7, '2024-04-10', '2024-04-15', 'Completed');
INSERT INTO event (volunteer_id_list, event_type_id, item_id_list, donation_receiver_id, start_date, end_date, status) VALUES ('8', 8, '8', 8, '2024-05-20', '2024-05-25', 'Completed');
INSERT INTO event (volunteer_id_list, event_type_id, item_id_list, donation_receiver_id, start_date, end_date, status) VALUES ('9', 9, '9', 9, '2024-06-25', '2024-06-30', 'Completed');
INSERT INTO event (volunteer_id_list, event_type_id, item_id_list, donation_receiver_id, start_date, end_date, status) VALUES ('10', 10, '10', 10, '2024-07-30', '2024-08-04', 'Completed');

-- Insert data into feedback
INSERT INTO feedback (receiver_id, volunteer_id, donor_id, message, picture) VALUES (1, NULL, NULL, 'Great help!', NULL);
INSERT INTO feedback (receiver_id, volunteer_id, donor_id, message, picture) VALUES (2, NULL, NULL, 'Thank you for the support.', NULL);
INSERT INTO feedback (receiver_id, volunteer_id, donor_id, message, picture) VALUES (3, NULL, NULL, 'Very useful items.', NULL);
INSERT INTO feedback (receiver_id, volunteer_id, donor_id, message, picture) VALUES (4, NULL, NULL, 'Appreciate the aid.', NULL);
INSERT INTO feedback (receiver_id, volunteer_id, donor_id, message, picture) VALUES (5, NULL, NULL, 'Helped a lot.', NULL);
INSERT INTO feedback (receiver_id, volunteer_id, donor_id, message, picture) VALUES (6, NULL, NULL, 'Good service.', NULL);
INSERT INTO feedback (receiver_id, volunteer_id, donor_id, message, picture) VALUES (NULL, NULL, 7, 'Excellent work.', NULL);
INSERT INTO feedback (receiver_id, volunteer_id, donor_id, message, picture) VALUES (8, NULL, NULL, 'Thankful for the donation.', NULL);
INSERT INTO feedback (receiver_id, volunteer_id, donor_id, message, picture) VALUES (NULL, 9, NULL, 'Beneficial for the community.', NULL);
INSERT INTO feedback (receiver_id, volunteer_id, donor_id, message, picture) VALUES (NULL, NULL, 10, 'Keep up the good work.', NULL);
