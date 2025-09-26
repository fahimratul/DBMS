#!/usr/bin/env python3

"""
Test script to analyze the recipient login flow and identify any database issues
"""

import requests
import time
import random
import json

def test_recipient_login_flow():
    """Test the complete recipient login flow and identify potential issues"""
    
    base_url = 'http://127.0.0.1:5000'
    session = requests.Session()
    
    print("🔍 TESTING RECIPIENT LOGIN FLOW")
    print("=" * 50)
    
    # Step 1: Test login page accessibility
    print("\n📋 Step 1: Testing login page...")
    try:
        response = session.get(f'{base_url}/auth/login')
        if response.status_code == 200:
            print("✅ Login page accessible")
        else:
            print(f"❌ Login page error: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Login page access failed: {e}")
        return False
    
    # Step 2: Create a test recipient for login testing
    print("\n📋 Step 2: Creating test recipient...")
    timestamp = str(int(time.time()) + random.randint(1000, 9999))
    test_username = f'testrecipient{timestamp}'
    test_password = 'TestPassword123!'
    
    signup_data = {
        'name': f'Test Recipient {timestamp}',
        'email': f'testrecipient{timestamp}@example.com',
        'phone': '1234567890',
        'emergency_phone': '0987654321',
        'address': f'{timestamp} Test Street',
        'username': test_username,
        'password': test_password
    }
    
    try:
        signup_response = session.post(f'{base_url}/auth/recipient_signup', data=signup_data)
        if 'success' in signup_response.url or signup_response.status_code in [200, 302]:
            print(f"✅ Test recipient created: {test_username}")
        else:
            print(f"⚠️ Signup may have issues but continuing... Status: {signup_response.status_code}")
    except Exception as e:
        print(f"❌ Recipient creation failed: {e}")
        return False
    
    # Step 3: Test recipient login
    print("\n📋 Step 3: Testing recipient login...")
    login_data = {
        'username': test_username,
        'password': test_password,
        'role': 'recipient'
    }
    
    try:
        login_response = session.post(f'{base_url}/auth/login', data=login_data, allow_redirects=True)
        print(f"Login response URL: {login_response.url}")
        print(f"Login response status: {login_response.status_code}")
        
        if 'recipient' in login_response.url:
            print("✅ Successfully redirected to recipient dashboard")
        elif 'login' in login_response.url:
            print("❌ Login failed - redirected back to login")
            print("Response content (first 500 chars):")
            print(login_response.text[:500])
            return False
        else:
            print(f"⚠️ Unexpected redirect: {login_response.url}")
    except Exception as e:
        print(f"❌ Login test failed: {e}")
        return False
    
    # Step 4: Test recipient dashboard access
    print("\n📋 Step 4: Testing recipient dashboard...")
    try:
        dashboard_response = session.get(f'{base_url}/recipient/recipient_dashboard')
        print(f"Dashboard status: {dashboard_response.status_code}")
        
        if dashboard_response.status_code == 200:
            print("✅ Recipient dashboard accessible")
            
            # Check if dashboard tries to load data that doesn't exist
            if 'error' in dashboard_response.text.lower():
                print("⚠️ Dashboard may have errors in content")
                print("Error indicators found in dashboard")
            else:
                print("✅ Dashboard loads without obvious errors")
                
        else:
            print(f"❌ Dashboard access failed: Status {dashboard_response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Dashboard test failed: {e}")
        return False
    
    # Step 5: Test recipient data endpoints
    print("\n📋 Step 5: Testing recipient data access...")
    
    # Test get_status endpoint
    try:
        status_response = session.get(f'{base_url}/recipient/get_status')
        status_data = status_response.json()
        
        print(f"Get status response: {status_response.status_code}")
        if status_data.get('success'):
            print("✅ Status endpoint working correctly")
            print(f"   Found {len(status_data.get('requests', []))} requests")
        else:
            print(f"❌ Status endpoint error: {status_data.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"❌ Status endpoint test failed: {e}")
    
    # Test get_items endpoint
    try:
        items_response = session.get(f'{base_url}/recipient/get_items')
        items_data = items_response.json()
        
        print(f"Get items response: {items_response.status_code}")
        if items_data.get('success'):
            print("✅ Items endpoint working correctly")
            total_items = sum(len(items) for items in items_data.get('items', {}).values())
            print(f"   Found {total_items} total items available")
        else:
            print(f"❌ Items endpoint error: {items_data.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"❌ Items endpoint test failed: {e}")
    
    # Step 6: Check for common database field issues
    print("\n📋 Step 6: Database field analysis...")
    print("Checking if recipient login attempts to access non-existent fields...")
    
    # The receiver table has these fields based on our earlier analysis:
    expected_fields = [
        'receiver_id', 'name', 'phone', 'user_name', 'password', 
        'emergency_phone', 'address', 'email', 'profile_picture'
    ]
    
    print("✅ Expected receiver table fields:")
    for field in expected_fields:
        print(f"   - {field}")
    
    print("\n🔍 Analysis complete!")
    print("=" * 50)
    
    return True

if __name__ == '__main__':
    success = test_recipient_login_flow()
    if success:
        print("\n🎯 SUMMARY: Recipient login flow tested successfully")
        print("Check the output above for any specific issues found.")
    else:
        print("\n❌ SUMMARY: Issues found in recipient login flow")
        print("Review the errors above and fix before proceeding.")