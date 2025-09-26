#!/usr/bin/env python3

"""
Test recipient login with proper username length constraints
"""

import requests
import time
import random

def test_recipient_login_with_short_username():
    """Test recipient login with username that fits database constraints"""
    
    base_url = 'http://127.0.0.1:5000'
    session = requests.Session()
    
    print("🔍 TESTING RECIPIENT LOGIN WITH SHORT USERNAME")
    print("=" * 60)
    
    # Create a short username (under 20 characters)
    timestamp = str(random.randint(100, 999))
    test_username = f'recip{timestamp}'  # Only 8 characters long
    test_password = 'TestPass123!'
    
    print(f"📝 Test username: '{test_username}' (length: {len(test_username)})")
    
    # Step 1: Create recipient with short username
    print("\n📋 Step 1: Creating recipient with short username...")
    signup_data = {
        'name': f'Test Recipient {timestamp}',
        'email': f'test{timestamp}@example.com',
        'phone': '1234567890',
        'emergency_phone': '0987654321',
        'address': f'{timestamp} Test Street',
        'username': test_username,
        'password': test_password
    }
    
    try:
        signup_response = session.post(f'{base_url}/auth/recipient_signup', data=signup_data, allow_redirects=True)
        print(f"Signup response URL: {signup_response.url}")
        print(f"Signup status: {signup_response.status_code}")
        
        if 'success' in signup_response.url:
            print("✅ Recipient created successfully and redirected to success page")
        elif 'login' in signup_response.url:
            print("⚠️ Redirected to login - may indicate successful signup")
        else:
            print(f"❌ Unexpected signup redirect: {signup_response.url}")
            
    except Exception as e:
        print(f"❌ Signup failed: {e}")
        return False
    
    # Step 2: Test login with the short username
    print(f"\n📋 Step 2: Testing login with username '{test_username}'...")
    login_data = {
        'username': test_username,
        'password': test_password,
        'role': 'recipient'
    }
    
    try:
        login_response = session.post(f'{base_url}/auth/login', data=login_data, allow_redirects=True)
        print(f"Login response URL: {login_response.url}")
        print(f"Login status: {login_response.status_code}")
        
        if 'recipient' in login_response.url:
            print("✅ LOGIN SUCCESSFUL! Redirected to recipient dashboard")
            
            # Step 3: Test dashboard functionality
            print("\n📋 Step 3: Testing dashboard functionality...")
            
            # Test get_status
            status_response = session.get(f'{base_url}/recipient/get_status')
            if status_response.status_code == 200:
                status_data = status_response.json()
                if status_data.get('success'):
                    print("✅ Status endpoint working")
                else:
                    print(f"⚠️ Status endpoint error: {status_data.get('error')}")
            else:
                print(f"❌ Status endpoint failed: {status_response.status_code}")
            
            # Test get_items 
            items_response = session.get(f'{base_url}/recipient/get_items')
            if items_response.status_code == 200:
                items_data = items_response.json()
                if items_data.get('success'):
                    print("✅ Items endpoint working")
                else:
                    print(f"⚠️ Items endpoint error: {items_data.get('error')}")
            else:
                print(f"❌ Items endpoint failed: {items_response.status_code}")
                
            return True
            
        elif 'login' in login_response.url:
            print("❌ Login failed - redirected back to login page")
            print("This might indicate password issues or other login problems")
            return False
        else:
            print(f"❌ Unexpected login redirect: {login_response.url}")
            return False
            
    except Exception as e:
        print(f"❌ Login test failed: {e}")
        return False

if __name__ == '__main__':
    success = test_recipient_login_with_short_username()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 SUCCESS: Recipient login working with proper username constraints!")
        print("✅ The username length limit fix resolved the login issues.")
    else:
        print("❌ FAILED: There may be additional login issues to investigate.")
    print("=" * 60)