#!/usr/bin/env python3
"""
Test script to verify feedback form submission works end-to-end
"""
import mysql.connector
import time

def test_feedback_submission():
    print("🧪 Testing Feedback Form Submission")
    print("=" * 50)
    
    # Get current feedback count
    try:
        db = mysql.connector.connect(
            host='localhost',
            user='flaskuser',
            password='flask',
            database='project2'
        )
        cursor = db.cursor(dictionary=True)
        
        cursor.execute('SELECT COUNT(*) as count FROM feedback')
        initial_count = cursor.fetchone()['count']
        print(f"📊 Initial feedback count: {initial_count}")
        
        cursor.close()
        db.close()
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎯 MANUAL TESTING INSTRUCTIONS")
    print("=" * 50)
    
    print("\n1. 🌐 Open your browser and go to:")
    print("   http://127.0.0.1:5000/auth/login")
    
    print("\n2. 👤 Login as recipient:")
    print("   Username: karim (or abdullah, ayesha, fatima)")
    print("   Password: [recipient password]")
    
    print("\n3. 📝 Go to feedback page:")
    print("   Click 'Feedback' button or go to:")
    print("   http://127.0.0.1:5000/recipient/feedback")
    
    print("\n4. ✅ Submit test feedback:")
    print("   - Name should be pre-filled")
    print("   - Enter message: 'This is a test feedback from recipient'")
    print("   - Optionally upload an image")
    print("   - Click 'Submit'")
    
    print("\n5. 🔍 Check if feedback was saved:")
    print("   Run: python check_feedback_count.py")
    
    print("\n⏰ After submitting, press Enter to check the database...")
    input()
    
    # Check final count
    try:
        db = mysql.connector.connect(
            host='localhost',
            user='flaskuser',
            password='flask',
            database='project2'
        )
        cursor = db.cursor(dictionary=True)
        
        cursor.execute('SELECT COUNT(*) as count FROM feedback')
        final_count = cursor.fetchone()['count']
        print(f"\n📊 Final feedback count: {final_count}")
        
        if final_count > initial_count:
            print("✅ SUCCESS! New feedback was saved to database")
            
            # Show the latest feedback
            cursor.execute('SELECT feedback_id, receiver_id, message, picture IS NOT NULL as has_picture FROM feedback ORDER BY feedback_id DESC LIMIT 1')
            latest = cursor.fetchone()
            print(f"📝 Latest feedback:")
            print(f"   ID: {latest['feedback_id']}")
            print(f"   Receiver ID: {latest['receiver_id']}")
            print(f"   Message: {latest['message']}")
            print(f"   Has Picture: {latest['has_picture']}")
        else:
            print("❌ No new feedback found. Submission may have failed.")
        
        cursor.close()
        db.close()
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_feedback_submission()