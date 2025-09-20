import mysql.connector

def check_feedback_count():
    try:
        db = mysql.connector.connect(
            host='localhost',
            user='flaskuser',
            password='flask',
            database='project2'
        )
        cursor = db.cursor(dictionary=True)
        
        cursor.execute('SELECT COUNT(*) as count FROM feedback')
        count = cursor.fetchone()['count']
        print(f"Current feedback count: {count}")
        
        # Show latest 2 feedback entries
        cursor.execute('SELECT feedback_id, receiver_id, volunteer_id, donor_id, LEFT(message, 50) as short_message FROM feedback ORDER BY feedback_id DESC LIMIT 2')
        recent = cursor.fetchall()
        print("\nLatest feedback entries:")
        for fb in recent:
            user_type = "Recipient" if fb['receiver_id'] else "Volunteer" if fb['volunteer_id'] else "Donor"
            user_id = fb['receiver_id'] or fb['volunteer_id'] or fb['donor_id']
            print(f"  ID {fb['feedback_id']}: {user_type} {user_id} - {fb['short_message']}...")
        
        cursor.close()
        db.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_feedback_count()