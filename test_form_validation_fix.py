#!/usr/bin/env python3

"""
Test that the recipient form now works without dateOfBirth validation
"""

import requests
import time
import random

def test_form_validation_fix():
    """Test that form validation no longer requires dateOfBirth"""
    
    base_url = 'http://127.0.0.1:5000'
    session = requests.Session()
    
    print("🔍 TESTING FIXED FORM VALIDATION")
    print("=" * 50)
    
    # Step 1: Create and login as recipient
    timestamp = str(random.randint(100, 999))
    test_username = f'valtest{timestamp}'
    test_password = 'TestPass123!'
    
    print(f"📋 Step 1: Creating test user '{test_username}'...")
    signup_data = {
        'name': f'Validation Test {timestamp}',
        'email': f'valtest{timestamp}@example.com',
        'phone': '1234567890',
        'emergency_phone': '0987654321',
        'address': f'{timestamp} Test Street',
        'username': test_username,
        'password': test_password
    }
    
    try:
        signup_response = session.post(f'{base_url}/auth/recipient_signup', data=signup_data)
        login_data = {
            'username': test_username,
            'password': test_password,
            'role': 'recipient'
        }
        login_response = session.post(f'{base_url}/auth/login', data=login_data, allow_redirects=True)
        
        if 'recipient' not in login_response.url:
            print(f"❌ Login failed: {login_response.url}")
            return False
        print("✅ User created and logged in successfully")
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return False
    
    # Step 2: Access the recipient dashboard page
    print(f"\n📋 Step 2: Accessing recipient dashboard...")
    try:
        dashboard_response = session.get(f'{base_url}/recipient/recipient_dashboard')
        
        if dashboard_response.status_code == 200:
            print("✅ Dashboard page loaded successfully")
            
            # Check if the page contains dateOfBirth references
            page_content = dashboard_response.text
            
            if 'date-of-birth' in page_content.lower() or 'dateofbirth' in page_content.lower():
                print("❌ ISSUE: Page still contains dateOfBirth references")
                
                # Find the specific lines
                lines = page_content.split('\n')
                for i, line in enumerate(lines):
                    if 'date-of-birth' in line.lower() or 'dateofbirth' in line.lower():
                        print(f"   Line {i+1}: {line.strip()[:100]}...")
                return False
            else:
                print("✅ No dateOfBirth references found in HTML")
                
            # Check if required form fields exist (the ones that should be there)
            required_fields = ['first-name', 'last-name', 'email', 'phone']
            missing_fields = []
            
            for field in required_fields:
                if f'id="{field}"' not in page_content:
                    missing_fields.append(field)
                    
            if missing_fields:
                print(f"❌ Missing required fields: {missing_fields}")
                return False
            else:
                print("✅ All required form fields present")
                
        else:
            print(f"❌ Dashboard access failed: {dashboard_response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Dashboard test failed: {e}")
        return False
    
    # Step 3: Test form submission with valid data (no dateOfBirth)
    print(f"\n📋 Step 3: Testing form submission...")
    relief_data = {
        'firstName': f'Test{timestamp}',
        'lastName': 'User',
        'email': f'valtest{timestamp}@example.com',
        'phone': '1234567890',
        # No dateOfBirth field!
        'address': f'{timestamp} Test Street',
        'city': 'Dhaka',
        'division': 'Dhaka',
        'postalCode': '1000',
        'latitude': 23.8103,
        'longitude': 90.4125,
        'reliefItems': {
            'Food assistance': {
                'needed': True,
                'amount': '5 kg rice',
                'selectedItemId': '1',
                'otherDetails': 'Urgent food needed'
            }
        },
        'priorityLevel': 'medium',
        'priorityMessage': 'Testing form submission'
    }
    
    try:
        headers = {'Content-Type': 'application/json'}
        submit_response = session.post(
            f'{base_url}/recipient/submit_request',
            json=relief_data,
            headers=headers
        )
        
        if submit_response.status_code == 200:
            result = submit_response.json()
            if result.get('success'):
                print("✅ Form submission successful!")
                print(f"   Request ID: {result.get('request_id')}")
                return True
            else:
                print(f"❌ Form submission failed: {result.get('error')}")
                return False
        else:
            print(f"❌ HTTP error: {submit_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Form submission test failed: {e}")
        return False

if __name__ == '__main__':
    success = test_form_validation_fix()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 SUCCESS: Form validation fixed completely!")
        print("✅ No more dateOfBirth validation errors")
        print("✅ Form submission works properly") 
        print("✅ All required fields working correctly")
    else:
        print("❌ FAILED: Still has dateOfBirth validation issues")
        print("Check the error messages above for specific problems")
    print("=" * 50)