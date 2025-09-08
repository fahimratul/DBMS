import mysql.connector

def cleanup_duplicate_items():
    """Remove duplicate items from the database, keeping only the lowest ID for each unique item"""
    try:
        # Connect to database
        db = mysql.connector.connect(
            host='localhost',
            user='flaskuser',
            password='flask',
            database='project2'
        )
        cursor = db.cursor()

        print('Checking for duplicate items in the database...')

        # Find duplicate items (same name and type)
        cursor.execute('''
            SELECT name, type_id, COUNT(*) as count, GROUP_CONCAT(item_id) as ids
            FROM item 
            GROUP BY name, type_id 
            HAVING COUNT(*) > 1
            ORDER BY name, type_id
        ''')

        duplicates = cursor.fetchall()
        if duplicates:
            print(f'Found {len(duplicates)} sets of duplicate items:')
            for dup in duplicates:
                print(f'  {dup[0]} (type_id: {dup[1]}) - {dup[2]} duplicates (IDs: {dup[3]})')
            
            print('\nCleaning up duplicates by keeping the lowest ID for each item...')
            
            # For each duplicate set, keep only the one with the lowest ID
            for dup in duplicates:
                name, type_id, count, ids_str = dup
                ids = [int(id_str) for id_str in ids_str.split(',')]
                keep_id = min(ids)
                delete_ids = [id for id in ids if id != keep_id]
                
                print(f'  Keeping {name} (ID: {keep_id}), deleting IDs: {delete_ids}')
                
                # Delete the duplicate entries
                for delete_id in delete_ids:
                    cursor.execute('DELETE FROM item WHERE item_id = %s', (delete_id,))
            
            db.commit()
            print('\nDuplicate cleanup completed!')
        else:
            print('No duplicate items found.')

        # Check final item count
        cursor.execute('SELECT COUNT(*) FROM item')
        total_items = cursor.fetchone()[0]
        print(f'\nTotal items in database: {total_items}')

        cursor.close()
        db.close()
        
    except Exception as e:
        print(f'Error during cleanup: {e}')

if __name__ == '__main__':
    cleanup_duplicate_items()
