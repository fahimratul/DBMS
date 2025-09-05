import random
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

# Common Bangladeshi names
names = ['Mohammad', 'Abdullah', 'Fatima', 'Ayesha', 'Rahman', 'Karim', 'Sultana', 'Hasan', 'Nadia', 'Jamal']

# Generate random dates within 1 year from today (Sept 4, 2025), not too close
start_date = datetime(2024, 9, 4)
end_date = datetime(2025, 9, 4)
dates = []
for i in range(100):  # generate more to avoid duplicates
    random_date = start_date + timedelta(days=random.randint(0, 365))
    dates.append(random_date.strftime('%Y-%m-%d'))
dates = list(set(dates))[:50]  # unique dates

# Phones
phones = ['017' + str(random.randint(10000000, 99999999)) for _ in range(30)]

# Addresses
addresses = ['Dhaka, Bangladesh', 'Chittagong, Bangladesh', 'Khulna, Bangladesh', 'Rajshahi, Bangladesh', 'Sylhet, Bangladesh', 'Barisal, Bangladesh', 'Rangpur, Bangladesh', 'Comilla, Bangladesh', 'Narayanganj, Bangladesh', 'Gazipur, Bangladesh']

# Generate data
print("-- Insert into type_list")
types = ['Food', 'Clothing', 'Medicine', 'Water', 'Shelter', 'Hygiene', 'Tools', 'Fuel', 'Education', 'Other']
for i, t in enumerate(types, 1):
    print(f"INSERT INTO type_list (type_id, type_name) VALUES ({i}, '{t}');")

print("\n-- Insert into account")
accounts = [('Bank Account 1', 'Bkash', 10000.00), ('Bank Account 2', 'Nagad', 15000.00), ('Bank Account 3', 'Rocket', 20000.00), ('Bank Account 4', 'Bank Transfer', 25000.00), ('Bank Account 5', 'Cash', 5000.00), ('Bank Account 6', 'PayPal', 30000.00), ('Bank Account 7', 'Stripe', 40000.00), ('Bank Account 8', 'Venmo', 1000.00), ('Bank Account 9', 'Zelle', 2000.00), ('Bank Account 10', 'Other', 0.00)]
for i, (name, method, balance) in enumerate(accounts, 1):
    print(f"INSERT INTO account (account_id, account_name, method_name, balance) VALUES ({i}, '{name}', '{method}', {balance});")

print("\n-- Insert into event_type")
event_types = ['Relief Distribution', 'Medical Aid', 'Food Supply', 'Clothing Drive', 'Shelter Setup', 'Hygiene Kit Distribution', 'Tool Distribution', 'Fuel Supply', 'Education Support', 'General Aid']
for i, et in enumerate(event_types, 1):
    print(f"INSERT INTO event_type (event_type_id, event_type) VALUES ({i}, '{et}');")

print("\n-- Insert into item")
items = [('Rice', 1), ('Blanket', 2), ('Paracetamol', 3), ('Bottled Water', 4), ('Tent', 5), ('Soap', 6), ('Hammer', 7), ('Diesel', 8), ('Books', 9), ('First Aid Kit', 10)]
for i, (name, type_id) in enumerate(items, 1):
    print(f"INSERT INTO item (item_id, name, type_id) VALUES ({i}, '{name}', {type_id});")

print("\n-- Insert into donor")
for i, name in enumerate(names, 1):
    username = name.lower()
    password_plain = name.capitalize() + '@12345'
    password_hash = generate_password_hash(password_plain)
    phone = phones[i-1]
    account_name = f'Account {i}'
    account_id = random.randint(1, 10)
    address = addresses[i-1]
    print(f"INSERT INTO donor (donor_id, name, phone, user_name, password, account_name, account_id, address) VALUES ({i}, '{name}', '{phone}', '{username}', '{password_hash}', '{account_name}', {account_id}, '{address}');")

print("\n-- Insert into receiver")
for i, name in enumerate(names, 1):
    username = name.lower()
    password_plain = name.capitalize() + '@12345'
    password_hash = generate_password_hash(password_plain)
    phone = phones[i+9]
    emergency_phone = phones[i+19]
    address = addresses[i-1]
    print(f"INSERT INTO receiver (receiver_id, name, phone, user_name, password, emergency_phone, address) VALUES ({i}, '{name}', '{phone}', '{username}', '{password_hash}', '{emergency_phone}', '{address}');")

print("\n-- Insert into volunteer")
for i, name in enumerate(names, 1):
    username = name.lower()
    password_plain = name.capitalize() + '@12345'
    password_hash = generate_password_hash(password_plain)
    phone = phones[i+19]
    email = f'{username}@example.com'
    dob = dates[i-1]
    address = addresses[i-1]
    pref_address = addresses[(i)%10]
    join_time = dates[i+9]
    print(f"INSERT INTO volunteer (volunteer_id, name, phone, email, dob, address, pref_address, join_time, user_name, password, nid_birthcert, profile_picture) VALUES ({i}, '{name}', '{phone}', '{email}', '{dob}', '{address}', '{pref_address}', '{join_time}', '{username}', '{password_hash}', NULL, NULL);")

print("\n-- Insert into donation")
for i in range(1, 11):
    message = f'Donation message {i}'
    date = dates[i-1]
    donor_id = i
    item_id = i
    print(f"INSERT INTO donation (donation_id, message, date, donor_id, item_id) VALUES ({i}, '{message}', '{date}', {donor_id}, {item_id});")

print("\n-- Insert into stock")
for i in range(1, 11):
    price = random.randint(10, 1000)
    quantity = random.randint(1, 100)
    purchase_date = dates[i-1]
    stock_date = dates[i+9]
    expire_date = dates[i+19]
    item_id = i
    account_id = random.randint(1, 10)
    print(f"INSERT INTO stock (stock_id, price, quantity, purchase_date, stock_date, expire_date, item_id, account_id) VALUES ({i}, {price}, {quantity}, '{purchase_date}', '{stock_date}', '{expire_date}', {item_id}, {account_id});")

print("\n-- Insert into donation_receiver")
for i in range(1, 11):
    receiver_id = i
    date = dates[i+29]
    priority_message = f'Priority {i}'
    stock_id = i
    additional_item = f'Additional {i}'
    print(f"INSERT INTO donation_receiver (donation_receiver_id, receiver_id, date, priority_message, stock_id, additional_item) VALUES ({i}, {receiver_id}, '{date}', '{priority_message}', {stock_id}, '{additional_item}');")

print("\n-- Insert into event")
for i in range(1, 11):
    volunteer_id = i
    event_type_id = i
    item_id = i
    donation_receiver_id = i
    start_date = dates[i+39]
    end_date = dates[i+40] if i+40 < len(dates) else dates[-1]
    status = 'Completed' if i % 2 == 0 else 'Ongoing'
    print(f"INSERT INTO event (task_id, volunteer_id, event_type_id, item_id, donation_receiver_id, start_date, end_date, status) VALUES ({i}, {volunteer_id}, {event_type_id}, {item_id}, {donation_receiver_id}, '{start_date}', '{end_date}', '{status}');")

print("\n-- Insert into money_transfer")
for i in range(1, 11):
    account_id = random.randint(1, 10)
    donation_id = i
    date = dates[i+49]
    print(f"INSERT INTO money_transfer (trx_id, account_id, donation_id, date) VALUES ({i}, {account_id}, {donation_id}, '{date}');")

print("\n-- Insert into feedback")
for i in range(1, 11):
    receiver_id = i
    volunteer_id = i
    donor_id = i
    task_id = i
    message = f'Feedback {i}'
    print(f"INSERT INTO feedback (feedback_id, receiver_id, volunteer_id, donor_id, task_id, message, picture) VALUES ({i}, {receiver_id}, {volunteer_id}, {donor_id}, {task_id}, '{message}', NULL);")
