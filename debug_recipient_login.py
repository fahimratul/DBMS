#!/usr/bin/env python3

"""
Debug script to check what's happening with recipient login
"""

import mysql.connector
import time
import random
from werkzeug.security import check_password_hash

def debug_recipient_login():
    """Debug the recipient login process step by step"""
    
    print("🔍 DEBUGGING RECIPIENT LOGIN ISSUES")
    print("=" * 50)
    
    # Step 1: Check database connection
    print("\n📋 Step 1: Testing database connection...")
    try:
        db = mysql.connector.connect(
            host='localhost',
            user='flaskuser',
            password='flask',
            database='project2'
        )
        cursor = db.cursor(dictionary=True)
        print("✅ Database connection successful")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
    
    # Step 2: Check receiver table structure
    print("\n📋 Step 2: Checking receiver table structure...")
    try:
        cursor.execute("DESCRIBE receiver")
        columns = cursor.fetchall()
        print("✅ Receiver table structure:")
        for col in columns:
            print(f"   - {col['Field']} ({col['Type']}) {'NOT NULL' if col['Null'] == 'NO' else 'NULL'}")
    except Exception as e:
        print(f"❌ Failed to check table structure: {e}")
        return False
    
    # Step 3: Create a test recipient manually to verify signup process
    print("\n📋 Step 3: Creating test recipient...")
    timestamp = str(random.randint(100, 999))  # Keep it short for 20 char limit
    test_username = f'duser{timestamp}'  # Much shorter username
    test_password = 'TestPassword123!'
    
    # Hash the password like the signup process does
    from werkzeug.security import generate_password_hash
    hashed_password = generate_password_hash(test_password)
    
    try:
        cursor.execute("""
            INSERT INTO receiver (name, phone, user_name, password, emergency_phone, address, email)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            f'Debug Test User {timestamp}',
            '1234567890',
            test_username,
            hashed_password,
            '0987654321',
            f'{timestamp} Debug Street',
            f'debug{timestamp}@example.com'
        ))
        db.commit()
        
        # Get the created user ID
        test_user_id = cursor.lastrowid
        print(f"✅ Test recipient created with ID: {test_user_id}")
        print(f"   Username: {test_username}")
        print(f"   Password: {test_password}")
        print(f"   Hashed: {hashed_password[:50]}...")
        
    except Exception as e:
        print(f"❌ Failed to create test recipient: {e}")
        return False
    
    # Step 4: Test the login query exactly as auth.py does it
    print("\n📋 Step 4: Testing login query...")
    try:
        # This is the exact query from auth.py
        cursor.execute(
            'SELECT receiver_id as id, user_name as username, password FROM receiver WHERE user_name = %s', 
            (test_username,)
        )
        user = cursor.fetchone()
        
        if user:
            print("✅ User found in database:")
            print(f"   ID: {user['id']}")
            print(f"   Username: {user['username']}")
            print(f"   Password hash: {user['password'][:50]}...")
            
            # Step 5: Test password verification
            print("\n📋 Step 5: Testing password verification...")
            if check_password_hash(user['password'], test_password):
                print("✅ Password verification successful")
            else:
                print("❌ Password verification failed!")
                print(f"   Stored hash: {user['password']}")
                print(f"   Test password: {test_password}")
                
                # Try to understand why password check is failing
                print("\n🔍 Password hash analysis:")
                print(f"   Hash method: {user['password'].split(':')[0] if ':' in user['password'] else 'Unknown'}")
                print(f"   Hash length: {len(user['password'])}")
                
        else:
            print("❌ User not found in database!")
            
            # Check if there are any users at all
            cursor.execute("SELECT COUNT(*) as count FROM receiver")
            count_result = cursor.fetchone()
            print(f"   Total receivers in database: {count_result['count']}")
            
            # Show recent users
            cursor.execute("SELECT receiver_id, user_name, name FROM receiver ORDER BY receiver_id DESC LIMIT 5")
            recent_users = cursor.fetchall()
            print("   Recent users:")
            for user in recent_users:
                print(f"     - ID: {user['receiver_id']}, Username: {user['user_name']}, Name: {user['name']}")
    
    except Exception as e:
        print(f"❌ Login query test failed: {e}")
        return False
    
    # Step 6: Test with an existing user from the database
    print("\n📋 Step 6: Testing with existing users...")
    try:
        cursor.execute("SELECT receiver_id, user_name, name FROM receiver ORDER BY receiver_id DESC LIMIT 3")
        existing_users = cursor.fetchall()
        
        if existing_users:
            print("✅ Found existing users in database:")
            for user in existing_users:
                print(f"   - ID: {user['receiver_id']}, Username: {user['user_name']}, Name: {user['name']}")
                
                # Try to fetch this user with the login query
                cursor.execute(
                    'SELECT receiver_id as id, user_name as username, password FROM receiver WHERE user_name = %s', 
                    (user['user_name'],)
                )
                login_test = cursor.fetchone()
                if login_test:
                    print(f"     ✅ Login query works for {user['user_name']}")
                else:
                    print(f"     ❌ Login query failed for {user['user_name']}")
        else:
            print("❌ No existing users found in database")
    
    except Exception as e:
        print(f"❌ Existing users test failed: {e}")
    
    # Clean up
    cursor.close()
    db.close()
    
    print("\n🔍 Debug analysis complete!")
    print("=" * 50)
    return True

if __name__ == '__main__':
    debug_recipient_login()