#!/usr/bin/env python3
"""
Enhanced Recipient Verification Script
Check email and profile_picture fields specifically
"""

import mysql.connector
from datetime import datetime

def verify_recipient_details():
    try:
        # Connect to database
        db = mysql.connector.connect(
            host='localhost',
            user='flaskuser',
            password='flask',
            database='project2'
        )
        cursor = db.cursor()
        
        print("=== ENHANCED RECIPIENT VERIFICATION ===")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Check the most recent recipients with email and profile data
        cursor.execute('''
            SELECT receiver_id, name, user_name, email, 
                   CASE 
                       WHEN profile_picture IS NULL THEN 'NULL'
                       WHEN LENGTH(profile_picture) > 0 THEN CONCAT('BLOB (', LENGTH(profile_picture), ' bytes)')
                       ELSE 'EMPTY'
                   END as profile_status
            FROM receiver 
            ORDER BY receiver_id DESC 
            LIMIT 5
        ''')
        recipients = cursor.fetchall()
        
        print("Recent recipients with email and profile picture status:")
        print("-" * 80)
        print(f"{'ID':<4} {'Name':<20} {'Username':<15} {'Email':<25} {'Profile':<15}")
        print("-" * 80)
        
        for rec in recipients:
            email_status = rec[3] if rec[3] else 'NULL'
            print(f"{rec[0]:<4} {rec[1]:<20} {rec[2]:<15} {email_status:<25} {rec[4]:<15}")
        
        # Count how many have email vs null
        cursor.execute('SELECT COUNT(*) FROM receiver WHERE email IS NOT NULL')
        with_email = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM receiver WHERE email IS NULL')
        without_email = cursor.fetchone()[0]
        
        print(f"\nEmail Statistics:")
        print(f"  With email: {with_email}")
        print(f"  Without email (NULL): {without_email}")
        
        # Count how many have profile pictures
        cursor.execute('SELECT COUNT(*) FROM receiver WHERE profile_picture IS NOT NULL')
        with_profile = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM receiver WHERE profile_picture IS NULL')
        without_profile = cursor.fetchone()[0]
        
        print(f"\nProfile Picture Statistics:")
        print(f"  With profile picture: {with_profile}")
        print(f"  Without profile picture (NULL): {without_profile}")
        
        cursor.close()
        db.close()
        print(f"\n=== VERIFICATION COMPLETE ===")
        
    except Exception as e:
        print(f"Database error: {e}")

if __name__ == '__main__':
    verify_recipient_details()