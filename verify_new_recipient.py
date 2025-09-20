#!/usr/bin/env python3
"""
Verify New Recipient Script
Run this after creating a new recipient to verify database insertion
"""

import mysql.connector
from datetime import datetime

def verify_new_recipient():
    try:
        # Connect to database
        db = mysql.connector.connect(
            host='localhost',
            user='flaskuser',
            password='flask',
            database='project2'
        )
        cursor = db.cursor()
        
        print("=== RECIPIENT DATABASE VERIFICATION ===")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Get current count
        cursor.execute('SELECT COUNT(*) FROM receiver')
        total_count = cursor.fetchone()[0]
        print(f"Total recipients in database: {total_count}")
        
        # Show the most recent recipient (likely the one just created)
        cursor.execute('''
            SELECT receiver_id, name, user_name, phone, emergency_phone, address 
            FROM receiver 
            ORDER BY receiver_id DESC 
            LIMIT 1
        ''')
        latest = cursor.fetchone()
        
        if latest:
            print(f"\nMost recent recipient:")
            print(f"  ID: {latest[0]}")
            print(f"  Name: {latest[1]}")
            print(f"  Username: {latest[2]}")
            print(f"  Phone: {latest[3]}")
            print(f"  Emergency Phone: {latest[4]}")
            print(f"  Address: {latest[5]}")
        
        # Show last 3 recipients for comparison
        print(f"\nLast 3 recipients for comparison:")
        cursor.execute('''
            SELECT receiver_id, name, user_name, phone 
            FROM receiver 
            ORDER BY receiver_id DESC 
            LIMIT 3
        ''')
        recent = cursor.fetchall()
        
        for i, rec in enumerate(recent, 1):
            status = "🆕 NEW" if i == 1 else "   existing"
            print(f"  {status} - ID: {rec[0]}, Name: {rec[1]}, Username: {rec[2]}")
        
        # Check for any recent signups (if username provided)
        print(f"\nLooking for common test usernames...")
        test_usernames = ['sarah_test', 'john_test', 'test_user', 'new_recipient']
        for username in test_usernames:
            cursor.execute('SELECT receiver_id, name FROM receiver WHERE user_name = %s', (username,))
            result = cursor.fetchone()
            if result:
                print(f"  ✅ Found: {username} -> ID: {result[0]}, Name: {result[1]}")
        
        cursor.close()
        db.close()
        print(f"\n=== VERIFICATION COMPLETE ===")
        
    except Exception as e:
        print(f"Database error: {e}")

if __name__ == '__main__':
    verify_new_recipient()