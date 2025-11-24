#!/usr/bin/env python3
"""
Instagram webhook server for handling comment notifications
Detects "FUN FACT" comments and sends DM responses
"""

from flask import Flask, request, jsonify
import json
import os
import requests
from datetime import datetime
# Load environment variables with fallbacks
INSTAGRAM_ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN', '')
INSTAGRAM_PAGE_ID = os.getenv('INSTAGRAM_PAGE_ID', '')

app = Flask(__name__)

# Instagram Graph API configuration
INSTAGRAM_API_BASE = "https://graph.facebook.com/v18.0"

class InstagramWebhookHandler:
    """Handle Instagram webhook events and DM automation"""
    
    def __init__(self):
        self.access_token = INSTAGRAM_ACCESS_TOKEN
        self.page_id = INSTAGRAM_PAGE_ID
        self.instagram_account_id = None
        self._get_instagram_account_id()
    
    def _get_instagram_account_id(self):
        """Get the Instagram Business Account ID from the Facebook Page"""
        try:
            url = f"{INSTAGRAM_API_BASE}/{self.page_id}"
            params = {
                'access_token': self.access_token,
                'fields': 'instagram_business_account'
            }
            response = requests.get(url, params=params)
            data = response.json()
            
            if 'instagram_business_account' in data:
                self.instagram_account_id = data['instagram_business_account']['id']
                print(f"✅ Instagram Account ID: {self.instagram_account_id}")
            else:
                print("❌ No Instagram Business Account found for this page")
        except Exception as e:
            print(f"❌ Error getting Instagram account ID: {e}")
    
    def get_fun_fact_for_post(self, media_id):
        """
        Get the fun_fact_followup for a specific Instagram post
        
        Args:
            media_id (str): Instagram media ID
            
        Returns:
            str: Fun fact followup or None if not found
        """
        try:
            # Load the content queue to find the matching post
            queue_file = 'scheduled_posts/content_queue.json'
            if not os.path.exists(queue_file):
                return None
            
            with open(queue_file, 'r') as f:
                queue = json.load(f)
            
            # Find the post by Instagram media ID
            for item in queue:
                posting_results = item.get('posting_results', {})
                instagram_result = posting_results.get('instagram', {})
                
                if isinstance(instagram_result, dict) and instagram_result.get('id') == media_id:
                    return item.get('fun_fact_followup', '')
            
            return None
            
        except Exception as e:
            print(f"❌ Error getting fun fact for post {media_id}: {e}")
            return None
    
    def send_dm(self, user_id, message):
        """
        Send a direct message to a user
        
        Args:
            user_id (str): Instagram user ID
            message (str): Message to send
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.instagram_account_id:
            print("❌ Instagram account ID not available")
            return False
        
        try:
            url = f"{INSTAGRAM_API_BASE}/{self.instagram_account_id}/messages"
            data = {
                'recipient': {'id': user_id},
                'message': {'text': message},
                'access_token': self.access_token
            }
            
            response = requests.post(url, json=data)
            result = response.json()
            
            if response.status_code == 200:
                print(f"✅ DM sent to user {user_id}")
                return True
            else:
                print(f"❌ Failed to send DM: {result}")
                return False
                
        except Exception as e:
            print(f"❌ Error sending DM: {e}")
            return False
    
    def handle_comment(self, comment_data):
        """
        Process a comment and send DM if it matches "FUN FACT"
        
        Args:
            comment_data (dict): Comment data from webhook
        """
        try:
            comment_text = comment_data.get('text', '').strip().upper()
            user_id = comment_data.get('from', {}).get('id')
            media_id = comment_data.get('media', {}).get('id')
            
            print(f"📝 Processing comment: '{comment_text}' from user {user_id} on media {media_id}")
            
            # Check if comment matches our trigger
            if comment_text == "FUN FACT":
                # Get the fun fact for this post
                fun_fact = self.get_fun_fact_for_post(media_id)
                
                if fun_fact:
                    # Send DM with the fun fact
                    dm_message = f"Here's your didactic fun fact: {fun_fact}"
                    
                    if self.send_dm(user_id, dm_message):
                        print(f"✅ Sent fun fact DM to user {user_id}")
                        
                        # Log the interaction
                        self._log_interaction(user_id, media_id, fun_fact)
                    else:
                        print(f"❌ Failed to send DM to user {user_id}")
                else:
                    print(f"⚠️ No fun fact found for media {media_id}")
            else:
                print(f"ℹ️ Comment doesn't match trigger: '{comment_text}'")
                
        except Exception as e:
            print(f"❌ Error handling comment: {e}")
    
    def _log_interaction(self, user_id, media_id, fun_fact):
        """Log DM interaction for tracking"""
        try:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'user_id': user_id,
                'media_id': media_id,
                'fun_fact_sent': fun_fact[:100] + "..." if len(fun_fact) > 100 else fun_fact,
                'action': 'fun_fact_dm_sent'
            }
            
            # Simple logging to file
            log_file = 'instagram_interactions.log'
            with open(log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
                
        except Exception as e:
            print(f"⚠️ Failed to log interaction: {e}")

# Initialize webhook handler
webhook_handler = InstagramWebhookHandler()

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """Verify webhook for Instagram"""
    verify_token = os.getenv('WEBHOOK_VERIFY_TOKEN', 'your_verify_token_here')
    
    if request.args.get('hub.verify_token') == verify_token:
        return request.args.get('hub.challenge')
    else:
        return 'Invalid verify token', 403

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    """Handle incoming webhook events"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'status': 'error', 'message': 'No data received'}), 400
        
        # Process webhook entries
        for entry in data.get('entry', []):
            for change in entry.get('changes', []):
                if change.get('field') == 'comments':
                    comment_data = change.get('value', {})
                    webhook_handler.handle_comment(comment_data)
        
        return jsonify({'status': 'success'}), 200
        
    except Exception as e:
        print(f"❌ Webhook error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'instagram_account_id': webhook_handler.instagram_account_id
    })

if __name__ == '__main__':
    print("🚀 Starting Instagram webhook server...")
    print(f"📱 Instagram Account ID: {webhook_handler.instagram_account_id}")
    
    # Get port from environment (Railway sets PORT automatically)
    port = int(os.getenv('PORT', 5000))
    
    # Run in production mode for Railway
    app.run(host='0.0.0.0', port=port, debug=False)
