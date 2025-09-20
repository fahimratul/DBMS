from werkzeug.security import generate_password_hash
import mysql.connector

# Generate proper password hash
password_hash = generate_password_hash('testpass123')

# Database connection
db = mysql.connector.connect(
    host='localhost',
    user='flaskuser',
    password='flask',
    database='project2'
)
cursor = db.cursor()

# Delete existing test user if any
cursor.execute("DELETE FROM receiver WHERE user_name = 'test_recipient'")

# Create test recipient with proper password hash
cursor.execute("""
    INSERT INTO receiver (name, phone, user_name, password, email, address) 
    VALUES (%s, %s, %s, %s, %s, %s)
""", (
    'Test Recipient',
    '+880 1712-345678',
    'test_recipient',
    password_hash,
    'test@example.com',
    'Test Address, Dhaka'
))

db.commit()
cursor.close()
db.close()

print("✅ Test recipient account created successfully!")
print("   Username: test_recipient")
print("   Password: testpass123")
print("   Email: test@example.com")
print()
print("🔗 Now you can test at: http://127.0.0.1:5000/auth/login")
