-- ========================
-- DROP TABLES IN CORRECT ORDER
-- ========================
-- DROP TABLE IF EXISTS feedback;
-- DROP TABLE IF EXISTS money_transfer;
-- DROP TABLE IF EXISTS event;
-- DROP TABLE IF EXISTS donation_receiver;
-- DROP TABLE IF EXISTS stock;
-- DROP TABLE IF EXISTS donation;
-- DROP TABLE IF EXISTS item;
-- DROP TABLE IF EXISTS volunteer;
-- DROP TABLE IF EXISTS event_type;
-- DROP TABLE IF EXISTS donor;
-- DROP TABLE IF EXISTS receiver;
-- DROP TABLE IF EXISTS type_list;
-- DROP TABLE IF EXISTS account;

-- ========================
-- CREATE TABLES
-- ========================

CREATE TABLE account (
    account_id INT PRIMARY KEY AUTO_INCREMENT,
    account_name VARCHAR(100) NOT NULL,
    method_name VARCHAR(100) NOT NULL,
    balance DECIMAL(10,2) CHECK (balance >= 0)
);

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

CREATE TABLE type_list (
    type_id INT PRIMARY KEY AUTO_INCREMENT,
    type_name VARCHAR(50)
);

CREATE TABLE event_type (
    event_type_id INT PRIMARY KEY AUTO_INCREMENT,
    event_type VARCHAR(100)
);

CREATE TABLE `volunteer` (
    `volunteer_id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(100) NOT NULL,
    `phone` varchar(20) NOT NULL,
    `email` varchar(100) DEFAULT NULL,
    `dob` date NOT NULL,
    `address` text NOT NULL,
    `pref_address` text,
    `join_time` date NOT NULL,
    `user_name` varchar(20) NOT NULL,
    `password` text NOT NULL,
    `nid_birthcert` mediumblob,
    `profile_picture` mediumblob,
    `status` varchar(255) DEFAULT 'new',
    PRIMARY KEY (`volunteer_id`),
    UNIQUE KEY `user_name` (`user_name`)
);

CREATE TABLE item (
    item_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    type_id INT,
    FOREIGN KEY (type_id) REFERENCES type_list(type_id)
        ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE donation (
    donation_id INT PRIMARY KEY AUTO_INCREMENT,
    message TEXT,
    date DATE,
    donor_id INT,
    item_id_list TEXT,
    FOREIGN KEY (donor_id) REFERENCES donor(donor_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE money_transfer (
    money_transfer_id INT PRIMARY KEY AUTO_INCREMENT,
    account_id INT,
    donation_id INT,
    amount DECIMAL CHECK (amount > 0),
    FOREIGN KEY (account_id) REFERENCES account(account_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (donation_id) REFERENCES donation(donation_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE stock (
    stock_id INT PRIMARY KEY AUTO_INCREMENT,
    price INT CHECK (price >= 0),
    quantity INT CHECK (quantity >= 0),
    purchase_date DATE,
    stock_date DATE NOT NULL,
    expire_date DATE,
    item_id INT,
    
    FOREIGN KEY (item_id) REFERENCES item(item_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);


 CREATE TABLE donation_receiver (
    donation_receiver_id INT PRIMARY KEY AUTO_INCREMENT,
     receiver_id INT,
     date DATE NOT NULL,
     priority_message TEXT,
     item_id_list TEXT,
     additional_item TEXT,
     FOREIGN KEY (receiver_id) REFERENCES receiver(receiver_id)
         ON UPDATE CASCADE ON DELETE CASCADE
 );

CREATE TABLE event (
    event_id INT PRIMARY KEY AUTO_INCREMENT,
    volunteer_id_list TEXT,
    event_type_id INT,
    item_id_list TEXT,
    donation_receiver_id INT,
    start_date DATE,
    end_date DATE,
    status VARCHAR(30) NOT NULL
);



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
