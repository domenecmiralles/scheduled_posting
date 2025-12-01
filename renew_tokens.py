#!/usr/bin/env python3
"""
Unified token renewal script for Instagram and Threads
Renews long-lived access tokens before they expire
"""

import requests
import json
import os
import sys
import argparse
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Credentials loaded from environment
FACEBOOK_CLIENT_ID = os.getenv('FACEBOOK_CLIENT_ID')
FACEBOOK_CLIENT_SECRET = os.getenv('FACEBOOK_CLIENT_SECRET')
THREADS_APP_SECRET = os.getenv('THREADS_APP_SECRET')


def renew_instagram_token(current_token, dry_run=False):
    """
    Renew Instagram/Facebook access token (exchange for new long-lived token)
    
    Args:
        current_token (str): Current access token
        dry_run (bool): If True, simulate without making API calls
        
    Returns:
        dict: New token data or None if failed
    """
    if dry_run:
        print("🔄 [DRY RUN] Would renew Instagram token...")
        return {'access_token': 'DRY_RUN_TOKEN_INSTAGRAM', 'expires_in': 5184000}
    
    try:
        url = "https://graph.facebook.com/v18.0/oauth/access_token"
        params = {
            'grant_type': 'fb_exchange_token',
            'client_id': FACEBOOK_CLIENT_ID,
            'client_secret': FACEBOOK_CLIENT_SECRET,
            'fb_exchange_token': current_token
        }
        
        print("🔄 Renewing Instagram access token...")
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            token_data = response.json()
            print(f"✅ Instagram token renewed!")
            print(f"   Expires in: {token_data['expires_in']//86400} days")
            return token_data
        else:
            print(f"❌ Instagram token renewal failed: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error renewing Instagram token: {e}")
        return None


def renew_threads_token(current_token, dry_run=False):
    """
    Renew Threads access token (refresh long-lived token)
    
    Args:
        current_token (str): Current access token
        dry_run (bool): If True, simulate without making API calls
        
    Returns:
        dict: New token data or None if failed
    """
    if dry_run:
        print("🔄 [DRY RUN] Would renew Threads token...")
        return {'access_token': 'DRY_RUN_TOKEN_THREADS', 'expires_in': 5184000}
    
    try:
        url = "https://graph.threads.net/refresh_access_token"
        params = {
            'grant_type': 'th_refresh_token',
            'access_token': current_token
        }
        
        print("🔄 Renewing Threads access token...")
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            token_data = response.json()
            print(f"✅ Threads token renewed!")
            print(f"   Expires in: {token_data.get('expires_in', 5184000)//86400} days")
            return token_data
        else:
            print(f"❌ Threads token renewal failed: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error renewing Threads token: {e}")
        return None


def update_env_file(token_name, new_token, dry_run=False):
    """
    Update .env file with new token
    
    Args:
        token_name (str): Name of the token variable
        new_token (str): New access token
        dry_run (bool): If True, simulate without writing
    """
    if dry_run:
        print(f"📝 [DRY RUN] Would update {token_name} in .env")
        return
    
    try:
        env_file = '.env'
        
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                lines = f.readlines()
        else:
            lines = []
        
        updated = False
        for i, line in enumerate(lines):
            if line.startswith(f'{token_name}='):
                lines[i] = f'{token_name}={new_token}\n'
                updated = True
                break
        
        if not updated:
            lines.append(f'{token_name}={new_token}\n')
        
        with open(env_file, 'w') as f:
            f.writelines(lines)
        
        print(f"✅ Updated {token_name} in .env file")
        
    except Exception as e:
        print(f"❌ Error updating .env file: {e}")


def write_token_output(tokens, dry_run=False):
    """
    Write tokens to output file for GitHub Actions
    
    Args:
        tokens (dict): Dictionary of token_name -> token_value
        dry_run (bool): If True, simulate without writing
    """
    if dry_run:
        print("📝 [DRY RUN] Would write tokens to output file")
        return
    
    try:
        with open('renewed_tokens.json', 'w') as f:
            json.dump(tokens, f)
        print("✅ Tokens written to renewed_tokens.json")
    except Exception as e:
        print(f"❌ Error writing token output: {e}")


def log_renewal(platform, token_data, dry_run=False):
    """
    Log token renewal for tracking
    """
    if dry_run:
        return
    
    try:
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'platform': platform,
            'expires_in_days': token_data.get('expires_in', 5184000) // 86400,
            'next_renewal_date': (datetime.now() + timedelta(days=50)).isoformat()
        }
        
        with open('token_renewals.log', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
            
    except Exception as e:
        print(f"⚠️ Could not log renewal: {e}")


def main():
    parser = argparse.ArgumentParser(description='Renew Instagram and Threads access tokens')
    parser.add_argument('--dry-run', action='store_true', help='Simulate renewal without making API calls')
    parser.add_argument('--instagram-only', action='store_true', help='Only renew Instagram token')
    parser.add_argument('--threads-only', action='store_true', help='Only renew Threads token')
    args = parser.parse_args()
    
    dry_run = args.dry_run
    
    print(f"🚀 Token Renewal - {datetime.now()}")
    if dry_run:
        print("⚠️  DRY RUN MODE - No actual changes will be made")
    print("=" * 50)
    
    renewed_tokens = {}
    
    # Renew Instagram token
    if not args.threads_only:
        instagram_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
        if instagram_token:
            token_data = renew_instagram_token(instagram_token, dry_run)
            if token_data:
                new_token = token_data['access_token']
                update_env_file('INSTAGRAM_ACCESS_TOKEN', new_token, dry_run)
                log_renewal('instagram', token_data, dry_run)
                renewed_tokens['INSTAGRAM_ACCESS_TOKEN'] = new_token
        else:
            print("⚠️ No INSTAGRAM_ACCESS_TOKEN found, skipping")
    
    print()
    
    # Renew Threads token
    if not args.instagram_only:
        threads_token = os.getenv('THREADS_ACCESS_TOKEN')
        if threads_token:
            token_data = renew_threads_token(threads_token, dry_run)
            if token_data:
                new_token = token_data['access_token']
                update_env_file('THREADS_ACCESS_TOKEN', new_token, dry_run)
                log_renewal('threads', token_data, dry_run)
                renewed_tokens['THREADS_ACCESS_TOKEN'] = new_token
        else:
            print("⚠️ No THREADS_ACCESS_TOKEN found, skipping")
    
    # Write output for GitHub Actions
    if renewed_tokens and not dry_run:
        write_token_output(renewed_tokens, dry_run)
    
    print()
    print("=" * 50)
    if renewed_tokens:
        print(f"🎉 Renewed {len(renewed_tokens)} token(s)")
        for name in renewed_tokens:
            print(f"   ✅ {name}")
    else:
        print("⚠️ No tokens were renewed")
    
    return 0 if renewed_tokens else 1


if __name__ == "__main__":
    sys.exit(main())
