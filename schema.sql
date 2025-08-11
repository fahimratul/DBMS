CREATE TABLE donor (
    donor_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    user_name VARCHAR(20) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    account_name VARCHAR(20) NOT NULL,
    account_id INT NOT NULL,
    address TEXT
);

CREATE TABLE donation (
    donation_id INT PRIMARY KEY AUTO_INCREMENT,
    message TEXT,
    date DATE,
    donor_id INT,
    item_id INT,
    FOREIGN KEY (donor_id) REFERENCES donor(donor_id),
    FOREIGN KEY (item_id) REFERENCES item(item_id)
);

CREATE TABLE receiver (
    receiver_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    user_name VARCHAR(20) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    emergency_phone VARCHAR(20),
    address TEXT
);

CREATE TABLE donation_receiver (
    donation_receiver_id INT PRIMARY KEY AUTO_INCREMENT,
    receiver_id INT,
    date DATE NOT NULL ,
    priority_message TEXT,
    stock_id INT,
    additional_item TEXT,
    FOREIGN KEY (stock_id) REFERENCES stock(stock_id),
    FOREIGN KEY (receiver_id) REFERENCES receiver(receiver_id)
);

CREATE TABLE stock (
    stock_id INT PRIMARY KEY AUTO_INCREMENT,
    price INT NOT NULL CHECK (price >= 0),
    quantity INT CHECK (quantity >= 0),
    purchase_date DATE NOT NULL ,
    stock_date DATE NOT NULL ,
    expire_date DATE NOT NULL ,
    item_id INT,
    account_id INT,
    FOREIGN KEY (item_id) REFERENCES item(item_id),
    FOREIGN KEY (account_id) REFERENCES account(account_id)
);

CREATE TABLE item (
    item_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    type_id INT,
    FOREIGN KEY (type_id) REFERENCES type_list(type_id)
);

CREATE TABLE type_list (
    type_id INT PRIMARY KEY AUTO_INCREMENT,
    type_name VARCHAR(50)
);

CREATE TABLE account (
    account_id INT PRIMARY KEY AUTO_INCREMENT,
    account_name VARCHAR(100) NOT NULL,
    method_name VARCHAR(100) NOT NULL,
    balance DECIMAL(10,2) CHECK (balance >= 0)
);

CREATE TABLE event_type (
    event_type_id INT PRIMARY KEY AUTO_INCREMENT,
    event_type VARCHAR(100)
);

CREATE TABLE volunteer (
    volunteer_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100),
    dob DATE NOT NULL,
    address TEXT NOT NULL,
    pref_address TEXT,
    join_time DATE NOT NULL,
    user_name VARCHAR(20) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    nid_birthcert BLOB NOT NULL
);

CREATE TABLE feedback (
    feedback_id INT PRIMARY KEY AUTO_INCREMENT,
    receiver_id INT,
    volunteer_id INT,
    donor_id INT,
    task_id INT,
    message TEXT,
    picture BLOB,
    FOREIGN KEY (receiver_id) REFERENCES receiver(receiver_id),
    FOREIGN KEY (volunteer_id) REFERENCES volunteer(volunteer_id),
    FOREIGN KEY (donor_id) REFERENCES donor(donor_id),
    FOREIGN KEY (task_id) REFERENCES event(task_id)
);

CREATE TABLE event (
    task_id INT PRIMARY KEY AUTO_INCREMENT,
    volunteer_id INT,
    event_type_id INT,
    item_id INT,
    donation_receiver_id INT,
    status VARCHAR(30) NOT NULL,
    FOREIGN KEY (volunteer_id) REFERENCES volunteer(volunteer_id),
    FOREIGN KEY (event_type_id) REFERENCES event_type(event_type_id),
    FOREIGN KEY (item_id) REFERENCES item(item_id)
);

CREATE TABLE money_transfer (
    trx_id INT PRIMARY KEY AUTO_INCREMENT,
    account_id INT,
    donation_id INT,
    date DATE,
    FOREIGN KEY (account_id) REFERENCES account(account_id),
    FOREIGN KEY (donation_id) REFERENCES donation(donation_id)
)