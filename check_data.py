import mysql.connector

def check_current_data():
    print("🔍 Checking Current Database Data")
    print("=" * 50)
    
    db = mysql.connector.connect(
        host='localhost',
        user='flaskuser',
        password='flask',
        database='project2'
    )
    cursor = db.cursor()
    
    # Check what's in the donation_receiver table for your user
    print("1. Current donation_receiver records:")
    cursor.execute("""
        SELECT dr.donation_receiver_id, dr.receiver_id, dr.date, dr.item_id_list, 
               dr.additional_item, dr.priority_level, dr.status, r.user_name
        FROM donation_receiver dr
        JOIN receiver r ON dr.receiver_id = r.receiver_id
        WHERE r.user_name = 'Jamal'
        ORDER BY dr.date DESC, dr.donation_receiver_id DESC
    """)
    records = cursor.fetchall()
    
    for record in records:
        dr_id, recv_id, date, item_list, additional, priority, status, username = record
        print(f"   ID: {dr_id} | User: {username} | Date: {date}")
        print(f"      item_id_list: {item_list}")
        print(f"      additional_item: {additional}")
        print(f"      status: {status}")
        print(f"      ---")
    
    if not records:
        print("   No records found for user 'Jamal'")
    
    # Check receiver table for Jamal
    print(f"\n2. Receiver info for 'Jamal':")
    cursor.execute("SELECT receiver_id, name, user_name FROM receiver WHERE user_name = 'Jamal'")
    receiver = cursor.fetchone()
    if receiver:
        print(f"   Receiver ID: {receiver[0]} | Name: {receiver[1]} | Username: {receiver[2]}")
    else:
        print("   User 'Jamal' not found in receiver table")
    
    cursor.close()
    db.close()
    
    print(f"\n🔧 FIXES APPLIED:")
    print("=" * 50)
    print("✅ Updated item parsing to handle new format: ID#ItemName#Quantity$")
    print("✅ Added debug logging to see what's being processed")
    print("✅ Fixed status display to show correct item information")
    print()
    print("🧪 TO TEST THE FIX:")
    print("1. Go to: http://127.0.0.1:5000/recipient/recipient_dashboard")
    print("2. Login with Jamal / Jamal@12345")
    print("3. Click 'Check Status' button")
    print("4. Verify that ONLY your actual requests are shown")
    print("5. Check Flask console for debug messages")

if __name__ == "__main__":
    check_current_data()
