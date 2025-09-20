import mysql.connector

# Database connection
db = mysql.connector.connect(
    host='localhost',
    user='flaskuser',
    password='flask',
    database='project2'
)
cursor = db.cursor()

# Add missing columns to donation_receiver table
try:
    cursor.execute('ALTER TABLE donation_receiver ADD COLUMN priority_level VARCHAR(20) DEFAULT "medium"')
    print('Added priority_level column')
except Exception as e:
    print(f'priority_level column: {e}')

try:
    cursor.execute('ALTER TABLE donation_receiver ADD COLUMN latitude DECIMAL(10, 8)')
    print('Added latitude column')
except Exception as e:
    print(f'latitude column: {e}')

try:
    cursor.execute('ALTER TABLE donation_receiver ADD COLUMN longitude DECIMAL(11, 8)')
    print('Added longitude column')
except Exception as e:
    print(f'longitude column: {e}')

try:
    cursor.execute('ALTER TABLE donation_receiver ADD COLUMN status VARCHAR(50) DEFAULT "submitted"')
    print('Added status column')
except Exception as e:
    print(f'status column: {e}')

# Add some sample items to test with
items_to_add = [
    ('Food', 1, 'Rice'),
    ('Food', 1, 'Lentils'),
    ('Food', 1, 'Oil'),
    ('Food', 1, 'Water'),
    ('Medical', 2, 'First Aid Kit'),
    ('Medical', 2, 'Medicine'),
    ('Clothing', 3, 'Blankets'),
    ('Clothing', 3, 'Clothes'),
    ('Shelter', 4, 'Tents'),
    ('Financial', 5, 'Cash Assistance')
]

# First, add type_list entries
types = [
    (1, 'Food'),
    (2, 'Medical'),
    (3, 'Clothing'),
    (4, 'Shelter'),
    (5, 'Financial')
]

for type_id, type_name in types:
    try:
        cursor.execute('INSERT INTO type_list (type_id, type_name) VALUES (%s, %s)', (type_id, type_name))
        print(f'Added type: {type_name}')
    except Exception as e:
        print(f'Type {type_name}: {e}')

# Add items
for category, type_id, item_name in items_to_add:
    try:
        cursor.execute('INSERT INTO item (name, type_id) VALUES (%s, %s)', (item_name, type_id))
        print(f'Added item: {item_name}')
    except Exception as e:
        print(f'Item {item_name}: {e}')

db.commit()
cursor.close()
print('Database setup completed!')
