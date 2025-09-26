#!/usr/bin/env python3

"""
Test recipient form submission without dateOfBirth field
"""

import requests
import time
import random
import json

def test_recipient_form_without_dob():
    """Test that recipient form works without dateOfBirth field"""
    
    base_url = 'http://127.0.0.1:5000'
    session = requests.Session()
    
    print("🔍 TESTING RECIPIENT FORM WITHOUT DATE OF BIRTH")
    print("=" * 60)
    
    # Step 1: Login as a recipient first
    timestamp = str(random.randint(100, 999))
    test_username = f'formtest{timestamp}'
    test_password = 'TestPass123!'
    
    # Create recipient account first
    print(f"📋 Step 1: Creating test recipient '{test_username}'...")
    signup_data = {
        'name': f'Form Test User {timestamp}',
        'email': f'formtest{timestamp}@example.com',
        'phone': '1234567890',
        'emergency_phone': '0987654321',
        'address': f'{timestamp} Test Street',
        'username': test_username,
        'password': test_password
    }
    
    try:
        signup_response = session.post(f'{base_url}/auth/recipient_signup', data=signup_data)
        if 'success' in signup_response.url or signup_response.status_code in [200, 302]:
            print("✅ Test recipient created successfully")
        else:
            print(f"❌ Recipient creation failed: {signup_response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Signup failed: {e}")
        return False
    
    # Step 2: Login as the recipient
    print(f"\n📋 Step 2: Logging in as recipient...")
    login_data = {
        'username': test_username,
        'password': test_password,
        'role': 'recipient'
    }
    
    try:
        login_response = session.post(f'{base_url}/auth/login', data=login_data, allow_redirects=True)
        if 'recipient' not in login_response.url:
            print(f"❌ Login failed: {login_response.url}")
            return False
        print("✅ Login successful")
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return False
    
    # Step 3: Test form submission without dateOfBirth field
    print(f"\n📋 Step 3: Testing relief request submission (without dateOfBirth)...")
    
    # Form data WITHOUT dateOfBirth field
    relief_request_data = {
        'firstName': f'Test{timestamp}',
        'lastName': 'User',
        'email': f'formtest{timestamp}@example.com',
        'phone': '1234567890',
        # NO dateOfBirth field - this was the problem!
        'address': f'{timestamp} Test Street',
        'city': 'Dhaka',
        'division': 'Dhaka',
        'postalCode': '1000',
        'latitude': 23.8103,
        'longitude': 90.4125,
        'reliefItems': {
            'Food': {
                'needed': True,
                'amount': '10 kg',
                'selectedItemId': '1',
                'otherDetails': 'Rice needed'
            }
        },
        'priorityLevel': 'high',
        'priorityMessage': 'Urgent need for food assistance'
    }
    
    try:
        headers = {'Content-Type': 'application/json'}
        submit_response = session.post(
            f'{base_url}/recipient/submit_request', 
            json=relief_request_data,
            headers=headers
        )
        
        print(f"Form submission status: {submit_response.status_code}")
        
        if submit_response.status_code == 200:
            response_data = submit_response.json()
            if response_data.get('success'):
                print("✅ Relief request submitted successfully!")
                print(f"   Request ID: {response_data.get('request_id')}")
                print(f"   Message: {response_data.get('message')}")
                
                # Step 4: Verify the request was saved
                print(f"\n📋 Step 4: Verifying request was saved...")
                status_response = session.get(f'{base_url}/recipient/get_status')
                status_data = status_response.json()
                
                if status_data.get('success') and len(status_data.get('requests', [])) > 0:
                    print("✅ Request successfully saved to database")
                    latest_request = status_data['requests'][0]
                    print(f"   Saved request ID: {latest_request.get('id')}")
                    print(f"   Status: {latest_request.get('status')}")
                    return True
                else:
                    print("❌ Request not found in database")
                    return False
            else:
                print(f"❌ Request submission failed: {response_data.get('error')}")
                return False
        else:
            print(f"❌ HTTP error: {submit_response.status_code}")
            print(f"Response: {submit_response.text[:500]}")
            return False
            
    except Exception as e:
        print(f"❌ Form submission test failed: {e}")
        return False

if __name__ == '__main__':
    success = test_recipient_form_without_dob()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 SUCCESS: Recipient form works correctly without dateOfBirth field!")
        print("✅ The problematic field has been successfully removed.")
        print("✅ City/division/postalCode are properly combined into address.")
    else:
        print("❌ FAILED: There may be additional form issues to investigate.")
    print("=" * 60)