"""
Quick Status Update Tool for Testing Progress Bar
"""

import mysql.connector
import sys

def update_request_status(request_id, new_status):
    """Update a specific request status"""
    try:
        db = mysql.connector.connect(
            host='localhost',
            user='flaskuser',
            password='flask',
            database='project2'
        )
        cursor = db.cursor()
        
        cursor.execute(
            'UPDATE donation_receiver SET status = %s WHERE donation_receiver_id = %s',
            (new_status, request_id)
        )
        
        db.commit()
        
        print(f"✅ Updated Request {request_id} to status: '{new_status}'")
        
        # Show all current statuses
        cursor.execute('''
            SELECT donation_receiver_id, status 
            FROM donation_receiver 
            WHERE receiver_id = 6 
            ORDER BY donation_receiver_id DESC 
            LIMIT 5
        ''')
        
        requests = cursor.fetchall()
        print("\n📊 Current Request Status:")
        for req in requests:
            progress_map = {"submitted": 25, "pending": 50, "approved": 75, "completed": 100}
            progress = progress_map.get(req[1], 25)
            print(f"  Request {req[0]}: '{req[1]}' → {progress}%")
        
        cursor.close()
        db.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_all_statuses():
    """Set up demo data with all different statuses"""
    print("🎭 Setting up demo data with all status types...")
    
    try:
        db = mysql.connector.connect(
            host='localhost',
            user='flaskuser',
            password='flask',
            database='project2'
        )
        cursor = db.cursor()
        
        # Get the latest 4 requests for user 6
        cursor.execute('''
            SELECT donation_receiver_id 
            FROM donation_receiver 
            WHERE receiver_id = 6 
            ORDER BY donation_receiver_id DESC 
            LIMIT 4
        ''')
        
        requests = cursor.fetchall()
        
        if len(requests) >= 4:
            statuses = ["submitted", "pending", "approved", "completed"]
            
            for i, req in enumerate(requests):
                if i < len(statuses):
                    cursor.execute(
                        'UPDATE donation_receiver SET status = %s WHERE donation_receiver_id = %s',
                        (statuses[i], req[0])
                    )
                    print(f"  Request {req[0]} → '{statuses[i]}'")
            
            db.commit()
            print("\n✅ Demo data setup complete!")
            
        cursor.close()
        db.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("📈 Progress Bar Status Manager")
        print("=" * 40)
        print("Usage:")
        print("  python status_manager.py demo          # Set up demo with all statuses")
        print("  python status_manager.py 24 pending    # Update request 24 to pending")
        print("  python status_manager.py 23 approved   # Update request 23 to approved")
        print("\nAvailable statuses: submitted, pending, approved, completed")
        
    elif len(sys.argv) == 2 and sys.argv[1] == "demo":
        demo_all_statuses()
        
    elif len(sys.argv) == 3:
        request_id = int(sys.argv[1])
        new_status = sys.argv[2]
        update_request_status(request_id, new_status)
        
    else:
        print("❌ Invalid arguments. Use: python status_manager.py demo  OR  python status_manager.py <request_id> <status>")