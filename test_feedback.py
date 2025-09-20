#!/usr/bin/env python3
"""
Test script to verify recipient feedback functionality
"""
import mysql.connector

def test_feedback_connection():
    print("🧪 Testing Recipient Feedback Connection")
    print("=" * 50)
    
    # Test database connection first
    try:
        db = mysql.connector.connect(
            host='localhost',
            user='flaskuser',
            password='flask',
            database='project2'
        )
        cursor = db.cursor(dictionary=True)
        
        # Check if feedback table exists
        cursor.execute("SHOW TABLES LIKE 'feedback'")
        if cursor.fetchone():
            print("✅ Feedback table exists in database")
        else:
            print("❌ Feedback table missing!")
            return
            
        # Check feedback table structure
        cursor.execute("DESCRIBE feedback")
        columns = cursor.fetchall()
        column_names = [col['Field'] for col in columns]
        required_columns = ['receiver_id', 'message', 'picture']
        
        missing_cols = [col for col in required_columns if col not in column_names]
        if missing_cols:
            print(f"❌ Missing columns in feedback table: {missing_cols}")
        else:
            print("✅ Feedback table has all required columns")
        
        # Check existing feedback entries
        cursor.execute("SELECT COUNT(*) as count FROM feedback")
        feedback_count = cursor.fetchone()['count']
        print(f"📊 Current feedback entries: {feedback_count}")
        
        cursor.close()
        db.close()
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return
    
    print("\n" + "=" * 50)
    print("🎯 FEEDBACK TESTING INSTRUCTIONS")
    print("=" * 50)
    
    print("\n1. 🌐 OPEN BROWSER:")
    print("   Go to: http://127.0.0.1:5000/auth/login")
    
    print("\n2. 👤 LOGIN AS RECIPIENT:")
    print("   Username: abdullah (or ayesha, fatima)")
    print("   Password: [use the password set during registration]")
    
    print("\n3. 📝 ACCESS FEEDBACK:")
    print("   a) Click on 'Feedback' button in the navigation")
    print("   b) OR click the floating feedback button")
    print("   c) Should redirect to: http://127.0.0.1:5000/recipient/feedback")
    
    print("\n4. ✅ TEST FEEDBACK FORM:")
    print("   a) Name field should be pre-filled with recipient name")
    print("   b) Enter a test message")
    print("   c) Optionally upload an image")
    print("   d) Click 'Submit'")
    print("   e) Should see success and return to dashboard")
    
    print("\n5. 🔍 VERIFY IN DATABASE:")
    print("   Check if feedback was saved in the feedback table")
    
    print("\n" + "=" * 50)
    print("✅ If all steps work, feedback is fully connected!")
    print("❌ If any step fails, check the browser console for errors")

if __name__ == "__main__":
    test_feedback_connection()