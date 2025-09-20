import mysql.connector

def check_feedback_table():
    try:
        db = mysql.connector.connect(
            host='localhost',
            user='flaskuser',
            password='flask',
            database='project2'
        )
        cursor = db.cursor(dictionary=True)
        
        print('=== FEEDBACK TABLE STRUCTURE ===')
        cursor.execute('DESCRIBE feedback')
        columns = cursor.fetchall()
        for col in columns:
            print(f'{col["Field"]:20} | {col["Type"]:15} | {col["Null"]:5} | {col["Key"]:5}')
        
        print('\n=== CURRENT FEEDBACK COUNT ===')
        cursor.execute('SELECT COUNT(*) as total FROM feedback')
        total = cursor.fetchone()['total']
        print(f'Total feedback entries: {total}')
        
        print('\n=== RECENT FEEDBACK (last 3) ===')
        cursor.execute('SELECT feedback_id, receiver_id, volunteer_id, donor_id, LEFT(message, 50) as short_message, picture IS NOT NULL as has_picture FROM feedback ORDER BY feedback_id DESC LIMIT 3')
        recent = cursor.fetchall()
        for fb in recent:
            print(f'ID: {fb["feedback_id"]} | Receiver: {fb["receiver_id"]} | Volunteer: {fb["volunteer_id"]} | Donor: {fb["donor_id"]} | Message: {fb["short_message"]}... | Picture: {fb["has_picture"]}')
        
        cursor.close()
        db.close()
        print('\n✅ Database connection successful')
        return True
    except Exception as e:
        print(f'❌ Error: {e}')
        return False

if __name__ == "__main__":
    check_feedback_table()