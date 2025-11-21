#!/usr/bin/env python3
"""
Simple Instagram API debugging script
Tests token validity and page access step by step
"""

import requests
import json
from config import INSTAGRAM_ACCESS_TOKEN, INSTAGRAM_PAGE_ID

def test_token_validity():
    """Step 1: Test if the access token is valid"""
    print("🔍 Step 1: Testing access token validity...")
    
    url = "https://graph.facebook.com/v18.0/me"
    params = {
        'access_token': INSTAGRAM_ACCESS_TOKEN,
        'fields': 'id,name'
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'error' in data:
            print(f"❌ Token invalid: {data['error']}")
            return False
        else:
            print(f"✅ Token valid - Connected to: {data.get('name', 'Unknown')} (ID: {data.get('id')})")
            return True
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def test_page_access():
    """Step 2: Test if we can access the specific page"""
    print(f"\n🔍 Step 2: Testing access to page ID {INSTAGRAM_PAGE_ID}...")
    
    url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_PAGE_ID}"
    params = {
        'access_token': INSTAGRAM_ACCESS_TOKEN,
        'fields': 'id,name,instagram_business_account'
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'error' in data:
            print(f"❌ Cannot access page: {data['error']}")
            return False, None
        else:
            print(f"✅ Page accessible: {data.get('name', 'Unknown')} (ID: {data.get('id')})")
            instagram_account = data.get('instagram_business_account')
            if instagram_account:
                print(f"✅ Instagram Business Account connected: {instagram_account['id']}")
            else:
                print("⚠️ No Instagram Business Account found")
            return True, instagram_account
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False, None

def test_instagram_account_access(instagram_account_id):
    """Step 3: Test direct access to Instagram Business Account"""
    if not instagram_account_id:
        print("\n⏭️ Step 3: Skipping - No Instagram account ID")
        return False
        
    print(f"\n🔍 Step 3: Testing Instagram Business Account {instagram_account_id}...")
    
    url = f"https://graph.facebook.com/v18.0/{instagram_account_id}"
    params = {
        'access_token': INSTAGRAM_ACCESS_TOKEN,
        'fields': 'id,username'
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'error' in data:
            print(f"❌ Cannot access Instagram account: {data['error']}")
            return False
        else:
            print(f"✅ Instagram account accessible: @{data.get('username', 'Unknown')} (ID: {data.get('id')})")
            return True
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def test_media_permissions(instagram_account_id):
    """Step 4: Test media posting permissions"""
    if not instagram_account_id:
        print("\n⏭️ Step 4: Skipping - No Instagram account ID")
        return False
        
    print(f"\n🔍 Step 4: Testing media posting permissions...")
    
    # Try to access the media endpoint on the Instagram account (not the page)
    url = f"https://graph.facebook.com/v18.0/{instagram_account_id}/media"
    params = {
        'access_token': INSTAGRAM_ACCESS_TOKEN
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'error' in data:
            print(f"❌ Cannot access media endpoint: {data['error']}")
            return False
        else:
            print(f"✅ Media endpoint accessible on Instagram account")
            return True
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def main():
    """Run all diagnostic tests"""
    print("🚀 Instagram API Diagnostic Tool")
    print("=" * 50)
    
    # Step 1: Token validity
    if not test_token_validity():
        print("\n❌ DIAGNOSIS: Access token is invalid or expired")
        return
    
    # Step 2: Page access
    page_ok, instagram_account = test_page_access()
    if not page_ok:
        print("\n❌ DIAGNOSIS: Cannot access the specified page ID")
        print("   - Check if the page ID is correct")
        print("   - Verify the token has permissions for this page")
        return
    
    # Step 3: Instagram account access
    instagram_account_id = instagram_account['id'] if instagram_account else None
    if not test_instagram_account_access(instagram_account_id):
        print("\n❌ DIAGNOSIS: Instagram Business Account not properly connected")
        print("   - Connect an Instagram Business Account to your Facebook page")
        print("   - Ensure the account has proper permissions")
        return
    
    # Step 4: Media permissions
    if not test_media_permissions(instagram_account_id):
        print("\n❌ DIAGNOSIS: No permissions to post media")
        print("   - Check if your app has 'instagram_basic' and 'pages_show_list' permissions")
        print("   - Verify the Instagram account allows API posting")
        return
    
    print("\n✅ ALL TESTS PASSED!")
    print("   Your Instagram setup appears to be working correctly.")
    print("   The issue might be in the specific API request format.")

if __name__ == "__main__":
    main()
