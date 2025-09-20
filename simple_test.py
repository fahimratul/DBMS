import mysql.connector
import json

def test_database_setup():
    print("🧪 Testing RAPID Relief Database Setup")
    print("=" * 50)
    
    try:
        # Test database connection
        print("\n1. Testing database connection...")
        db = mysql.connector.connect(
            host='localhost',
            user='flaskuser',
            password='flask',
            database='project2'
        )
        cursor = db.cursor()
        print("✅ Database connection successful!")
        
        # Test donation_receiver table structure
        print("\n2. Checking donation_receiver table structure...")
        cursor.execute("DESCRIBE donation_receiver")
        columns = cursor.fetchall()
        column_names = [col[0] for col in columns]
        
        print("   Current columns:", column_names)
        
        required_columns = ['receiver_id', 'date', 'priority_message', 'item_id_list', 
                          'additional_item', 'priority_level', 'latitude', 'longitude', 'status']
        missing_columns = [col for col in required_columns if col not in column_names]
        
        if missing_columns:
            print(f"❌ Missing columns: {missing_columns}")
        else:
            print("✅ All required columns present!")
        
        # Test items and types
        print("\n3. Checking available items...")
        cursor.execute("""
            SELECT t.type_name, i.name 
            FROM item i 
            JOIN type_list t ON i.type_id = t.type_id 
            ORDER BY t.type_name, i.name
        """)
        items = cursor.fetchall()
        
        if items:
            print("✅ Items available:")
            current_type = None
            for type_name, item_name in items:
                if type_name != current_type:
                    current_type = type_name
                    print(f"   📁 {type_name}:")
                print(f"      - {item_name}")
        else:
            print("❌ No items found in database")
        
        # Test receiver table
        print("\n4. Checking receiver table...")
        cursor.execute("DESCRIBE receiver")
        receiver_columns = cursor.fetchall()
        print("   receiver table columns:", [col[0] for col in receiver_columns])
        
        cursor.close()
        db.close()
        
        # Create a test recipient account if needed
        print("\n5. Creating test recipient account...")
        db = mysql.connector.connect(
            host='localhost',
            user='flaskuser',
            password='flask',
            database='project2'
        )
        cursor = db.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO receiver (name, phone, user_name, password, email, address) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                'Test Recipient',
                '+880 1712-345678',
                'test_recipient',
                'pbkdf2:sha256:600000$dummy$hash',  # You'll need proper password hashing
                'test@example.com',
                'Test Address, Dhaka'
            ))
            db.commit()
            print("✅ Test recipient account created!")
            print("   Username: test_recipient")
            print("   Password: (you'll need to set this properly)")
        except Exception as e:
            if "Duplicate entry" in str(e):
                print("✅ Test recipient account already exists")
            else:
                print(f"❌ Error creating test account: {e}")
        
        cursor.close()
        db.close()
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎯 TESTING INSTRUCTIONS")
    print("=" * 60)
    print("Your Flask app is running at: http://127.0.0.1:5000")
    print()
    print("📋 Step-by-step manual testing:")
    print()
    print("1. 🌐 OPEN BROWSER:")
    print("   - Go to: http://127.0.0.1:5000/recipient/recipient_dashboard")
    print("   - You should be redirected to login page")
    print()
    print("2. 👤 CREATE/LOGIN AS RECIPIENT:")
    print("   - Register a new recipient account OR")
    print("   - Login with existing recipient credentials")
    print()
    print("3. 📝 TEST THE RELIEF REQUEST FORM:")
    print("   a) Fill Personal Information (Step 1)")
    print("   b) Fill Location Information (Step 2)")
    print("   c) Select Relief Items (Step 3) - items should load from database")
    print("   d) Set Priority Level (Step 4)")
    print("   e) Review and Submit (Step 5)")
    print()
    print("4. 🔍 CHECK FOR SUCCESS:")
    print("   - Form should submit successfully")
    print("   - Success message should appear")
    print("   - Check browser console (F12) for any errors")
    print()
    print("5. 📊 TEST STATUS CHECKING:")
    print("   - Click 'Check Status' button")
    print("   - Your submitted request should appear")
    print()
    print("6. 🚨 TROUBLESHOOTING:")
    print("   - Open browser console (F12) to see JavaScript errors")
    print("   - Check Flask console for backend errors")
    print("   - Verify database connection is working")
    print()
    print("=" * 60)
    print("🎉 If all steps work, your system is fully connected!")
    
if __name__ == "__main__":
    test_database_setup()
