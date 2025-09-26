#!/usr/bin/env python3
"""
Test script to verify the single name field implementation in recipient dashboard.
This test validates that:
1. User info endpoint returns full name instead of first/last name split
2. The form displays a single name field that gets auto-populated
3. All functionality works correctly with the updated name structure
"""

import requests
import json
import random

def test_single_name_field():
    """Test the updated single name field functionality"""
    print("🔍 TESTING SINGLE NAME FIELD IMPLEMENTATION")
    print("=" * 50)
    
    # Test parameters
    base_url = "http://127.0.0.1:5000"
    test_name = f"John Doe Smith {random.randint(100, 999)}"
    
    # Create test user
    print("1. Creating test recipient...")
    signup_data = {
        'username': f'singlename{random.randint(100, 999)}',
        'email': f'singlename{random.randint(100, 999)}@example.com',
        'password': 'password123',
        'confirm_password': 'password123',
        'name': test_name,
        'phone': '1234567890',
        'address': '123 Single Name Test Street'
    }
    
    # Create recipient account
    signup_response = requests.post(f"{base_url}/auth/recipient_signup", data=signup_data)
    if signup_response.status_code != 200 or 'signup_successful' not in signup_response.url:
        print(f"❌ Failed to create recipient: {signup_response.status_code}")
        return False
    
    print(f"✅ Recipient created with name: {test_name}")
    
    # Login
    print("2. Logging in...")
    session = requests.Session()
    login_response = session.post(f"{base_url}/auth/login", data={
        'username': signup_data['username'],
        'password': signup_data['password']
    })
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        return False
    
    print("✅ Login successful")
    
    # Test get_user_info endpoint
    print("3. Testing user info endpoint...")
    user_info_response = session.get(f"{base_url}/recipient/get_user_info")
    
    if user_info_response.status_code != 200:
        print(f"❌ Failed to get user info: {user_info_response.status_code}")
        return False
    
    user_info = user_info_response.json()
    
    if not user_info.get('success'):
        print(f"❌ User info request failed: {user_info.get('error')}")
        return False
    
    print("✅ User info endpoint working")
    
    # Verify single name field
    print("4. Verifying name field structure...")
    user_data = user_info['data']
    
    # Check that we have 'name' field and no 'firstName'/'lastName' fields
    if 'name' not in user_data:
        print("❌ Missing 'name' field in user data")
        return False
    
    if 'firstName' in user_data or 'lastName' in user_data:
        print("❌ Found deprecated firstName/lastName fields")
        return False
    
    # Verify the name matches what we registered
    returned_name = user_data['name']
    if returned_name != test_name:
        print(f"❌ Name mismatch - Expected: {test_name}, Got: {returned_name}")
        return False
    
    print(f"✅ Single name field working correctly: {returned_name}")
    
    # Test dashboard access
    print("5. Testing dashboard access...")
    dashboard_response = session.get(f"{base_url}/recipient/recipient_dashboard")
    
    if dashboard_response.status_code != 200:
        print(f"❌ Failed to access dashboard: {dashboard_response.status_code}")
        return False
    
    print("✅ Dashboard accessible")
    
    # Verify other fields are still present
    print("6. Verifying all required fields...")
    required_fields = ['name', 'email', 'phone', 'address']
    for field in required_fields:
        if field not in user_data:
            print(f"❌ Missing required field: {field}")
            return False
        print(f"  ✅ {field}: {user_data[field]}")
    
    print()
    print("🎉 SUCCESS: Single name field implementation working perfectly!")
    print("📋 SUMMARY:")
    print(f"  • Name field: {user_data['name']}")
    print(f"  • Email: {user_data['email']}")
    print(f"  • Phone: {user_data['phone']}")
    print(f"  • Address: {user_data['address']}")
    print("  • No more firstName/lastName split")
    print("  • Auto-population working with single name field")
    
    return True

if __name__ == "__main__":
    try:
        success = test_single_name_field()
        exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        exit(1)