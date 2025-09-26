#!/usr/bin/env python3

"""
Analyze recipient form fields vs database schema to find mismatches
"""

def analyze_recipient_form_vs_database():
    """Compare recipient form fields with database schema"""
    
    print("🔍 RECIPIENT FORM vs DATABASE SCHEMA ANALYSIS")
    print("=" * 60)
    
    # Database schema for receiver table
    database_fields = {
        'receiver_id': 'INT PRIMARY KEY AUTO_INCREMENT',
        'name': 'VARCHAR(100) NOT NULL',
        'phone': 'VARCHAR(20) NOT NULL', 
        'user_name': 'VARCHAR(20) NOT NULL UNIQUE',
        'password': 'TEXT NOT NULL',
        'emergency_phone': 'VARCHAR(20)',
        'address': 'TEXT',
        'email': 'VARCHAR(100)',
        'profile_picture': 'BLOB'
    }
    
    # Form fields from recipient dashboard (based on screenshot and HTML)
    form_fields = [
        'firstName',        # Step 1: Personal Information
        'lastName',         # Step 1: Personal Information  
        'email',           # Step 1: Personal Information
        'phone',           # Step 1: Personal Information
        'dateOfBirth',     # Step 1: Personal Information ❌ NOT IN DATABASE
        'address',         # Step 2: Location Information
        'city',            # Step 2: Location Information ❌ NOT IN DATABASE
        'division',        # Step 2: Location Information ❌ NOT IN DATABASE
        'postalCode',      # Step 2: Location Information ❌ NOT IN DATABASE
        'latitude',        # Step 2: GPS Coordinates (stored in donation_receiver table)
        'longitude',       # Step 2: GPS Coordinates (stored in donation_receiver table)
        'reliefItems',     # Step 3: Relief Items (stored in donation_receiver table)
        'priorityLevel',   # Step 4: Priority Information (stored in donation_receiver table)
        'priorityMessage', # Step 4: Priority Information (stored in donation_receiver table)
    ]
    
    print("✅ FIELDS IN DATABASE (receiver table):")
    for field, datatype in database_fields.items():
        print(f"   - {field}: {datatype}")
    
    print(f"\n📝 FIELDS IN RECIPIENT FORM:")
    fields_in_db = []
    fields_not_in_db = []
    
    for field in form_fields:
        # Map form fields to database fields
        db_equivalent = None
        
        if field in ['firstName', 'lastName']:
            db_equivalent = 'name'  # Combined into single name field
        elif field == 'email':
            db_equivalent = 'email'
        elif field == 'phone':
            db_equivalent = 'phone'
        elif field == 'address':
            db_equivalent = 'address'
        elif field in ['latitude', 'longitude', 'reliefItems', 'priorityLevel', 'priorityMessage']:
            db_equivalent = 'donation_receiver table'  # Different table
        elif field in ['dateOfBirth', 'city', 'division', 'postalCode']:
            db_equivalent = None  # Not in database
            
        if db_equivalent:
            fields_in_db.append(f"{field} → {db_equivalent}")
            print(f"   ✅ {field} → {db_equivalent}")
        else:
            fields_not_in_db.append(field)
            print(f"   ❌ {field} → NOT IN DATABASE!")
    
    print(f"\n🚨 CRITICAL ISSUES FOUND:")
    print(f"   - Fields NOT in database: {len(fields_not_in_db)}")
    
    for field in fields_not_in_db:
        print(f"     ❌ {field}")
        
        if field == 'dateOfBirth':
            print(f"        Impact: Form collects birth date but can't save it")
        elif field == 'city':
            print(f"        Impact: City info collected but only 'address' field exists in DB")
        elif field == 'division':
            print(f"        Impact: Division info collected but only 'address' field exists in DB") 
        elif field == 'postalCode':
            print(f"        Impact: Postal code collected but only 'address' field exists in DB")
    
    print(f"\n💡 RECOMMENDED FIXES:")
    
    if 'dateOfBirth' in fields_not_in_db:
        print(f"   1. Remove 'Date of Birth' field from form (not in database)")
        print(f"      OR add date_of_birth column to receiver table")
    
    if any(field in fields_not_in_db for field in ['city', 'division', 'postalCode']):
        print(f"   2. Combine city/division/postalCode into address field")
        print(f"      OR add separate columns to receiver table")
        
    print(f"\n🎯 SUMMARY:")
    print(f"   - Total form fields: {len(form_fields)}")
    print(f"   - Fields with DB mapping: {len(fields_in_db)}")
    print(f"   - Fields without DB mapping: {len(fields_not_in_db)}")
    
    return fields_not_in_db

if __name__ == '__main__':
    problematic_fields = analyze_recipient_form_vs_database()
    
    print("\n" + "=" * 60)
    if problematic_fields:
        print(f"❌ ISSUES FOUND: {len(problematic_fields)} fields not in database")
        print("These fields will cause data loss or errors!")
    else:
        print("✅ All form fields match database schema")
    print("=" * 60)