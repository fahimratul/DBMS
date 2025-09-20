import mysql.connector

def clean_old_format_data():
    print("🧹 Cleaning Old Format Data")
    print("=" * 40)
    
    db = mysql.connector.connect(
        host='localhost',
        user='flaskuser',
        password='flask',
        database='project2'
    )
    cursor = db.cursor()
    
    # Find all records with old format (no # symbol)
    cursor.execute("""
        SELECT donation_receiver_id, receiver_id, item_id_list, additional_item
        FROM donation_receiver 
        WHERE item_id_list IS NOT NULL 
        AND item_id_list NOT LIKE '%#%'
    """)
    old_records = cursor.fetchall()
    
    print(f"Found {len(old_records)} records with old format:")
    
    for record in old_records:
        dr_id, recv_id, item_list, additional = record
        print(f"   ID: {dr_id} | item_id_list: '{item_list}' | additional: '{additional}'")
    
    if old_records:
        choice = input(f"\nDo you want to DELETE these {len(old_records)} old format records? (y/N): ")
        
        if choice.lower() == 'y':
            # Delete old format records
            for record in old_records:
                dr_id = record[0]
                cursor.execute("DELETE FROM donation_receiver WHERE donation_receiver_id = %s", (dr_id,))
                print(f"   ✅ Deleted record ID: {dr_id}")
            
            db.commit()
            print(f"\n✅ Successfully deleted {len(old_records)} old format records!")
        else:
            print("\n❌ No records deleted.")
    else:
        print("✅ No old format records found!")
    
    # Show remaining records
    print(f"\n📊 Remaining records (NEW FORMAT ONLY):")
    cursor.execute("""
        SELECT dr.donation_receiver_id, dr.item_id_list, dr.additional_item, r.user_name
        FROM donation_receiver dr
        JOIN receiver r ON dr.receiver_id = r.receiver_id
        WHERE dr.item_id_list IS NOT NULL
        ORDER BY dr.donation_receiver_id DESC
    """)
    remaining = cursor.fetchall()
    
    for record in remaining:
        dr_id, item_list, additional, username = record
        print(f"   ID: {dr_id} | User: {username}")
        print(f"      item_id_list: {item_list}")
        print(f"      additional_item: {additional}")
        print(f"      ---")
    
    cursor.close()
    db.close()
    
    print(f"\n🎉 Database now contains ONLY new format entries!")
    print("   Format: ID#ItemName#Quantity$ID#ItemName#Quantity$...")

if __name__ == "__main__":
    clean_old_format_data()
