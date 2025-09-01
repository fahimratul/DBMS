#!/usr/bin/env python3
"""
Script to load volunteer profile pictures into the database
"""

import mysql.connector
from mysql.connector import Error
import os

def load_volunteer_pictures():
    """Load profile pictures for all volunteers"""
    
    connection = None
    cursor = None
    
    # Database connection
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='project',
            user='flaskuser',
            password='flask'  # Replace with your actual password
        )
        
        cursor = connection.cursor()
        
        # Base path for images
        base_path = '/home/shahariar/Class_note/Year3-Semester-1/Projects/DBMS_local/DBMS/rapid/static/images/profile_img'
        
        # Volunteer ID to image mapping
        volunteer_images = {
            1: 'profile1.jpeg',
            2: 'profile2.jpeg', 
            3: 'profile3.jpeg',
            4: 'profile4.jpeg',
            5: 'profile5.jpeg',
            6: 'profile6.jpeg'
        }
        
        for volunteer_id, image_file in volunteer_images.items():
            image_path = os.path.join(base_path, image_file)
            
            if os.path.exists(image_path):
                try:
                    # Read the image file
                    with open(image_path, 'rb') as file:
                        binary_data = file.read()
                    
                    # Update the volunteer record
                    sql_update_query = """UPDATE volunteer SET profile_picture = %s WHERE volunteer_id = %s"""
                    cursor.execute(sql_update_query, (binary_data, volunteer_id))
                    
                    print(f"Updated volunteer ID {volunteer_id} with {image_file}")
                    
                except Exception as e:
                    print(f"Error loading {image_file} for volunteer {volunteer_id}: {e}")
            else:
                print(f"Image file not found: {image_path}")
        
        # Commit all changes
        connection.commit()
        print(f"Successfully updated volunteer profile pictures!")
            
    except Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection and connection.is_connected():
            if cursor:
                cursor.close()
            connection.close()
            print("Database connection closed.")

if __name__ == "__main__":
    load_volunteer_pictures()
