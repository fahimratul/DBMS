import requests
import json

# Base URL
BASE_URL = "http://127.0.0.1:5000"

def test_endpoints():
    print("🧪 Testing RAPID Relief Recipient System")
    print("=" * 50)
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    # Test 1: Check if app is running
    print("\n1. Testing if Flask app is running...")
    try:
        response = session.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Flask app is running successfully!")
        else:
            print(f"❌ Flask app returned status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Cannot connect to Flask app: {e}")
        return False
    
    # Test 2: Try to access recipient dashboard (should redirect to login)
    print("\n2. Testing recipient dashboard access...")
    try:
        response = session.get(f"{BASE_URL}/recipient/recipient_dashboard")
        if response.status_code == 302:  # Redirect to login
            print("✅ Authentication is working - redirects to login")
        elif response.status_code == 200:
            print("⚠️  Dashboard accessible without login (check @login_required)")
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing dashboard: {e}")
    
    # Test 3: Test relief items endpoint (requires authentication)
    print("\n3. Testing relief items endpoint...")
    try:
        response = session.get(f"{BASE_URL}/recipient/get_items")
        if response.status_code == 302:
            print("✅ Items endpoint requires authentication")
        elif response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Items endpoint working!")
                print(f"   Available item types: {list(data.get('items', {}).keys())}")
            else:
                print(f"❌ Items endpoint error: {data.get('error')}")
        else:
            print(f"❌ Items endpoint status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing items endpoint: {e}")
    
    # Test 4: Database connection test
    print("\n4. Testing database connection...")
    try:
        import mysql.connector
        db = mysql.connector.connect(
            host='localhost',
            user='flaskuser',
            password='flask',
            database='project2'
        )
        cursor = db.cursor()
        
        # Test donation_receiver table structure
        cursor.execute("DESCRIBE donation_receiver")
        columns = cursor.fetchall()
        column_names = [col[0] for col in columns]
        
        required_columns = ['priority_level', 'latitude', 'longitude', 'status']
        missing_columns = [col for col in required_columns if col not in column_names]
        
        if missing_columns:
            print(f"❌ Missing columns in donation_receiver: {missing_columns}")
        else:
            print("✅ donation_receiver table has all required columns")
        
        # Test if items exist
        cursor.execute("SELECT COUNT(*) FROM item")
        item_count = cursor.fetchone()[0]
        print(f"✅ Database has {item_count} items available")
        
        # Test if types exist
        cursor.execute("SELECT COUNT(*) FROM type_list")
        type_count = cursor.fetchone()[0]
        print(f"✅ Database has {type_count} item types available")
        
        cursor.close()
        db.close()
        
    except Exception as e:
        print(f"❌ Database connection error: {e}")
    
    print("\n" + "=" * 50)
    print("🔍 Manual Testing Instructions:")
    print("=" * 50)
    print("1. Go to: http://127.0.0.1:5000")
    print("2. Register/Login as a recipient")
    print("3. Navigate to recipient dashboard")
    print("4. Fill out the relief request form")
    print("5. Check browser console (F12) for any JavaScript errors")
    print("6. Submit the form and check for success message")
    print("\n📍 If authentication is blocking you:")
    print("   - Create a recipient account first")
    print("   - Or temporarily disable @login_required for testing")

if __name__ == "__main__":
    test_endpoints()
