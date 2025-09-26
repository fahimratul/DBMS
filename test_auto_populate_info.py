#!/usr/bin/env python3

"""
Test that recipient dashboard auto-populates user information correctly
"""

import requests
import time
import random

def test_auto_populate_user_info():
    """Test that the recipient dashboard auto-populates user information from registration"""
    
    base_url = 'http://127.0.0.1:5000'
    session = requests.Session()
    
    print("🔍 TESTING AUTO-POPULATION OF USER INFO")
    print("=" * 60)
    
    # Step 1: Create recipient with known information
    timestamp = str(random.randint(100, 999))
    test_username = f'autopop{timestamp}'
    test_password = 'TestPass123!'
    test_name = f'AutoTest User{timestamp}'
    test_email = f'autotest{timestamp}@example.com'
    test_phone = '1234567890'
    test_address = f'{timestamp} Auto Test Street'
    
    print(f"📋 Step 1: Creating test recipient with known info...")
    print(f"   Name: {test_name}")
    print(f"   Email: {test_email}")
    print(f"   Phone: {test_phone}")
    print(f"   Address: {test_address}")
    
    signup_data = {
        'name': test_name,
        'email': test_email,
        'phone': test_phone,
        'emergency_phone': '0987654321',
        'address': test_address,
        'username': test_username,
        'password': test_password
    }
    
    try:
        signup_response = session.post(f'{base_url}/auth/recipient_signup', data=signup_data)
        if 'success' not in signup_response.url and signup_response.status_code not in [200, 302]:
            print(f"❌ Signup failed: {signup_response.status_code}")
            return False
        print("✅ Recipient created successfully")
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
    
    # Step 3: Test the get_user_info endpoint
    print(f"\n📋 Step 3: Testing user info endpoint...")
    try:
        user_info_response = session.get(f'{base_url}/recipient/get_user_info')
        
        if user_info_response.status_code == 200:
            user_data = user_info_response.json()
            
            if user_data.get('success'):
                print("✅ User info endpoint working")
                
                # Verify the data matches what we registered with
                returned_data = user_data.get('data', {})
                
                # Split the test name for comparison
                name_parts = test_name.split(' ', 1)
                expected_first = name_parts[0]
                expected_last = name_parts[1] if len(name_parts) > 1 else ''
                
                print(f"\n🔍 Checking returned data:")
                print(f"   Expected First Name: '{expected_first}' | Returned: '{returned_data.get('firstName', '')}'")
                print(f"   Expected Last Name: '{expected_last}' | Returned: '{returned_data.get('lastName', '')}'")
                print(f"   Expected Email: '{test_email}' | Returned: '{returned_data.get('email', '')}'")
                print(f"   Expected Phone: '{test_phone}' | Returned: '{returned_data.get('phone', '')}'")
                print(f"   Expected Address: '{test_address}' | Returned: '{returned_data.get('address', '')}'")
                
                # Validate each field
                all_correct = True
                
                if returned_data.get('firstName') != expected_first:
                    print(f"❌ First name mismatch!")
                    all_correct = False
                
                if returned_data.get('lastName') != expected_last:
                    print(f"❌ Last name mismatch!")
                    all_correct = False
                    
                if returned_data.get('email') != test_email:
                    print(f"❌ Email mismatch!")
                    all_correct = False
                    
                if returned_data.get('phone') != test_phone:
                    print(f"❌ Phone mismatch!")
                    all_correct = False
                    
                if returned_data.get('address') != test_address:
                    print(f"❌ Address mismatch!")
                    all_correct = False
                
                if all_correct:
                    print("✅ All user information matches registration data!")
                    return True
                else:
                    print("❌ Some user information doesn't match!")
                    return False
                    
            else:
                print(f"❌ User info endpoint error: {user_data.get('error')}")
                return False
        else:
            print(f"❌ User info endpoint failed: {user_info_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ User info test failed: {e}")
        return False

if __name__ == '__main__':
    success = test_auto_populate_user_info()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 SUCCESS: User info auto-population working perfectly!")
        print("✅ Registration data correctly retrieved")
        print("✅ Personal information will auto-populate on dashboard")
        print("✅ No more duplicate data entry required")
    else:
        print("❌ FAILED: User info auto-population has issues")
        print("Check the error messages above for specific problems")
    print("=" * 60)