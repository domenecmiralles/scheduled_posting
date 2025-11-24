#!/usr/bin/env python3
"""
Automated Facebook token renewal script
Renews long-lived access token every 50 days
"""

import requests
import json
import os
from datetime import datetime, timedelta

# Your app credentials - loaded from environment for security
CLIENT_ID = os.getenv('FACEBOOK_CLIENT_ID')
CLIENT_SECRET = os.getenv('FACEBOOK_CLIENT_SECRET')

def renew_access_token(current_token):
    """
    Renew Facebook access token
    
    Args:
        current_token (str): Current access token
        
    Returns:
        dict: New token data or None if failed
    """
    try:
        url = "https://graph.facebook.com/v18.0/oauth/access_token"
        params = {
            'grant_type': 'fb_exchange_token',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'fb_exchange_token': current_token
        }
        
        print(f"🔄 Renewing Facebook access token...")
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            token_data = response.json()
            print(f"✅ Token renewed successfully!")
            print(f"   New token: {token_data['access_token'][:50]}...")
            print(f"   Expires in: {token_data['expires_in']} seconds ({token_data['expires_in']//86400} days)")
            return token_data
        else:
            print(f"❌ Token renewal failed: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error renewing token: {e}")
        return None

def update_env_file(new_token):
    """
    Update .env file with new token
    
    Args:
        new_token (str): New access token
    """
    try:
        env_file = '.env'
        
        # Read current .env file
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                lines = f.readlines()
        else:
            lines = []
        
        # Update or add INSTAGRAM_ACCESS_TOKEN
        updated = False
        for i, line in enumerate(lines):
            if line.startswith('INSTAGRAM_ACCESS_TOKEN='):
                lines[i] = f'INSTAGRAM_ACCESS_TOKEN={new_token}\n'
                updated = True
                break
        
        if not updated:
            lines.append(f'INSTAGRAM_ACCESS_TOKEN={new_token}\n')
        
        # Write back to .env file
        with open(env_file, 'w') as f:
            f.writelines(lines)
        
        print(f"✅ Updated .env file with new token")
        
    except Exception as e:
        print(f"❌ Error updating .env file: {e}")

def log_renewal(token_data):
    """
    Log token renewal for tracking
    
    Args:
        token_data (dict): Token renewal response
    """
    try:
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'new_token': token_data['access_token'][:20] + '...',
            'expires_in_seconds': token_data['expires_in'],
            'expires_in_days': token_data['expires_in'] // 86400,
            'next_renewal_date': (datetime.now() + timedelta(days=50)).isoformat()
        }
        
        # Append to renewal log
        with open('token_renewals.log', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        print(f"✅ Logged renewal - next renewal needed around {log_entry['next_renewal_date'][:10]}")
        
    except Exception as e:
        print(f"⚠️ Could not log renewal: {e}")

def main():
    """
    Main renewal function
    """
    print(f"🚀 Facebook Token Renewal - {datetime.now()}")
    
    # Get current token from environment
    current_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
    
    if not current_token:
        print("❌ No INSTAGRAM_ACCESS_TOKEN found in environment")
        print("💡 Make sure to set it in your .env file first")
        return
    
    # Renew the token
    token_data = renew_access_token(current_token)
    
    if token_data:
        new_token = token_data['access_token']
        
        # Update .env file
        update_env_file(new_token)
        
        # Log the renewal
        log_renewal(token_data)
        
        print(f"\n🎉 Token renewal complete!")
        print(f"📝 Next steps:")
        print(f"   1. Update GitHub secrets with new token")
        print(f"   2. Update deployment environment variables")
        print(f"   3. Next renewal needed in ~50 days")
        
        # Output for easy copying
        print(f"\n📋 New token for GitHub secrets:")
        print(f"   {new_token}")
        
    else:
        print(f"❌ Token renewal failed")

if __name__ == "__main__":
    main()
