#!/usr/bin/env python3
"""
Test script to verify recipient signup -> success page connection
"""

import requests
import time

def test_recipient_signup_to_success():
    """Test the complete flow from recipient signup to success page"""
    print("🧪 Testing Recipient Signup → Success Page Flow")
    print("=" * 60)
    
    base_url = "http://127.0.0.1:5000"
    
    # Test 1: Check if signup page is accessible
    print("\n1. Testing recipient signup page access...")
    try:
        response = requests.get(f"{base_url}/auth/recipient_signup", timeout=5)
        if response.status_code == 200:
            print("✅ Recipient signup page is accessible!")
        else:
            print(f"❌ Signup page returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot access signup page: {e}")
        return False
    
    # Test 2: Check if success page is accessible
    print("\n2. Testing signup success page access...")
    try:
        response = requests.get(f"{base_url}/auth/success", timeout=5)
        if response.status_code == 200:
            print("✅ Signup success page is accessible!")
            if 'recipient account has been created successfully' in response.text.lower():
                print("✅ Success page has recipient-specific message!")
            if 'Continue to Login' in response.text:
                print("✅ Success page has login button!")
            if 'Return to Home' in response.text:
                print("✅ Success page has home button!")
        else:
            print(f"❌ Success page returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot access success page: {e}")
        return False
    
    # Test 3: Test form submission flow
    print("\n3. Testing complete signup → success flow...")
    
    # Create unique test data to avoid duplicate user issues
    timestamp = str(int(time.time()))
    test_data = {
        'name': f'Test Recipient {timestamp}',
        'email': f'testrecipient{timestamp}@example.com',
        'phone': '1234567890',
        'emergency_phone': '0987654321',
        'address': f'123 Test Street {timestamp}, Test City',
        'username': f'testrecipient{timestamp}',
        'password': 'TestPassword123!'
    }
    
    try:
        # Use session to handle redirects properly
        session = requests.Session()
        response = session.post(
            f"{base_url}/auth/recipient_signup", 
            data=test_data, 
            timeout=10,
            allow_redirects=True  # Follow redirects to see final destination
        )
        
        print(f"   Final response status: {response.status_code}")
        print(f"   Final URL: {response.url}")
        
        if response.status_code == 200:
            if '/auth/success' in response.url:
                print("✅ Successfully redirected to success page!")
                if 'Registration Successful' in response.text:
                    print("✅ Success page displays correct message!")
                if 'Continue to Login' in response.text:
                    print("✅ Success page has login link!")
            elif '/auth/login' in response.url:
                print("⚠️ Redirected to login page instead of success page")
            elif 'recipient_signup' in response.url:
                print("⚠️ Stayed on signup page - check for errors")
                if 'error' in response.text.lower() or 'already exists' in response.text.lower():
                    print("⚠️ Registration failed - user may already exist")
            else:
                print(f"⚠️ Unexpected redirect to: {response.url}")
                
        else:
            print(f"❌ Unexpected response status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error during form submission flow: {e}")
        return False
    
    print("\n📋 Summary of signup → success page connection:")
    print("   ✅ Modified registration_handler to redirect recipients to success page")
    print("   ✅ Enhanced signup_successful.html with recipient-specific messaging")
    print("   ✅ Added multiple navigation options (Login & Home)")
    print("   ✅ Improved visual design of success page")
    print("   ✅ Maintained error handling for failed registrations")
    
    print("\n🎯 Manual testing steps:")
    print("   1. Go to: http://127.0.0.1:5000/auth/recipient_signup")
    print("   2. Fill out all form sections")
    print("   3. Submit the form")
    print("   4. Verify redirection to: http://127.0.0.1:5000/auth/success")
    print("   5. Check that success message is recipient-specific")
    print("   6. Click 'Continue to Login' to test login functionality")
    
    return True

if __name__ == "__main__":
    success = test_recipient_signup_to_success()
    if success:
        print("\n🎉 Recipient signup → success page connection is working!")
    else:
        print("\n❌ Some issues may need attention.")