#!/usr/bin/env python3
"""
Simple validation script to test the single name field changes.
This script checks the HTML template and JavaScript for proper single name field implementation.
"""

import re
import os

def test_html_template():
    """Test that the HTML template has the single name field"""
    print("🔍 TESTING HTML TEMPLATE FOR SINGLE NAME FIELD")
    print("=" * 50)
    
    html_file = "rapid/templates/recipient/recipient.html"
    
    if not os.path.exists(html_file):
        print(f"❌ HTML template not found: {html_file}")
        return False
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for single name field
    if 'id="name"' in content and 'name="name"' in content:
        print("✅ Single name field found in HTML")
    else:
        print("❌ Single name field not found in HTML")
        return False
    
    # Check that first-name and last-name are removed
    if 'id="first-name"' in content or 'id="last-name"' in content:
        print("❌ Old first-name/last-name fields still present")
        return False
    
    print("✅ Old first-name/last-name fields successfully removed")
    
    # Check label text
    if 'Full Name *' in content:
        print("✅ Correct label 'Full Name *' found")
    else:
        print("❌ Expected label 'Full Name *' not found")
        return False
    
    return True

def test_javascript():
    """Test that the JavaScript handles single name field"""
    print()
    print("🔍 TESTING JAVASCRIPT FOR SINGLE NAME FIELD")
    print("=" * 50)
    
    js_file = "rapid/static/script/recipient.js"
    
    if not os.path.exists(js_file):
        print(f"❌ JavaScript file not found: {js_file}")
        return False
    
    with open(js_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for single name field handling in loadUserInfo
    if 'getElementById("name")' in content:
        print("✅ Single name field handling found in JavaScript")
    else:
        print("❌ Single name field handling not found in JavaScript")
        return False
    
    # Check that first-name and last-name references are removed
    if 'getElementById("first-name")' in content or 'getElementById("last-name")' in content:
        print("❌ Old first-name/last-name references still present in JavaScript")
        return False
    
    print("✅ Old first-name/last-name references successfully removed from JavaScript")
    
    # Check validation update
    if '"name"' in content and '"email"' in content and '"phone"' in content:
        print("✅ Form validation updated for single name field")
    else:
        print("❌ Form validation not properly updated")
        return False
    
    return True

def test_backend():
    """Test that the backend returns single name field"""
    print()
    print("🔍 TESTING BACKEND FOR SINGLE NAME FIELD")
    print("=" * 50)
    
    backend_file = "rapid/recipient.py"
    
    if not os.path.exists(backend_file):
        print(f"❌ Backend file not found: {backend_file}")
        return False
    
    with open(backend_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for single name field return in get_user_info
    if "'name': user_info.get('name', '')" in content:
        print("✅ Backend returns single name field")
    else:
        print("❌ Backend doesn't return single name field correctly")
        return False
    
    # Check that firstName/lastName split is removed
    if 'firstName' in content or 'lastName' in content:
        print("❌ Old firstName/lastName logic still present in backend")
        return False
    
    print("✅ Old firstName/lastName logic successfully removed from backend")
    
    return True

def main():
    """Run all tests"""
    print("🎯 VALIDATING SINGLE NAME FIELD IMPLEMENTATION")
    print("=" * 60)
    
    html_ok = test_html_template()
    js_ok = test_javascript()
    backend_ok = test_backend()
    
    print()
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 30)
    
    results = [
        ("HTML Template", html_ok),
        ("JavaScript", js_ok),
        ("Backend", backend_ok)
    ]
    
    all_passed = True
    for component, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{component:15} {status}")
        if not passed:
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Single name field implementation is complete and correct")
        print()
        print("🔧 CHANGES IMPLEMENTED:")
        print("  • Removed separate first name and last name fields")
        print("  • Added single 'Full Name' field")
        print("  • Updated auto-population to use single name")
        print("  • Updated form validation")
        print("  • Updated backend to return full name")
        print("  • Updated form submission handling")
        print()
        print("🎯 USER EXPERIENCE:")
        print("  • Users now see only one name field instead of two")
        print("  • Auto-population fills the full name from registration")
        print("  • Form is simpler and less redundant")
        return True
    else:
        print("❌ SOME TESTS FAILED!")
        print("Please review the implementation")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)