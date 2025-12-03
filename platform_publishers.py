"""
Social media platform publishers
Clean, modular posting functions for each platform
"""

import requests
import json
import time
import os
import pytumblr
from atproto import Client as BskyClient
from config import (
    INSTAGRAM_ACCESS_TOKEN, INSTAGRAM_PAGE_ID,
    TIKTOK_ACCESS_TOKEN,
    TUMBLR_CONSUMER_KEY, TUMBLR_CONSUMER_SECRET, 
    TUMBLR_OAUTH_TOKEN, TUMBLR_OAUTH_TOKEN_SECRET, TUMBLR_BLOG_NAME,
    BLUESKY_USERNAME, BLUESKY_PASSWORD,
    THREADS_ACCESS_TOKEN
)


class InstagramPublisher:
    """Instagram Graph API publisher"""
    
    def __init__(self):
        self.access_token = INSTAGRAM_ACCESS_TOKEN
        self.page_id = INSTAGRAM_PAGE_ID
        self.base_url = "https://graph.facebook.com/v21.0"
        self.instagram_account_id = None
        self._get_instagram_account_id()
    
    def _get_instagram_account_id(self):
        """Get the Instagram Business Account ID from the Facebook Page"""
        try:
            url = f"{self.base_url}/{self.page_id}"
            params = {
                'access_token': self.access_token,
                'fields': 'instagram_business_account'
            }
            response = requests.get(url, params=params)
            data = response.json()
            
            if 'instagram_business_account' in data:
                self.instagram_account_id = data['instagram_business_account']['id']
            else:
                print("❌ No Instagram Business Account found for this page")
        except Exception as e:
            print(f"❌ Error getting Instagram account ID: {e}")
    
    def post_content(self, content_data, caption):
        """
        Post content to Instagram
        
        Args:
            content_data (dict): Content information with 'url', 'media_type'
            caption (str): Formatted caption with hashtags
            
        Returns:
            dict: API response or None if failed
        """
        if not self.access_token or not self.instagram_account_id:
            print("Instagram API credentials not configured or Instagram account not found")
            return None
            
        try:
            media_type = content_data['media_type']
            media_url = content_data['url']
            
            # Step 1: Create media container using Instagram Business Account ID
            container_url = f"{self.base_url}/{self.instagram_account_id}/media"
            
            if media_type == 'video':
                container_params = {
                    'media_type': 'REELS',
                    'video_url': media_url,
                    'caption': caption,
                    'access_token': self.access_token,
                    'is_made_with_ai': 'true'
                }
            else:  # image
                container_params = {
                    'image_url': media_url,
                    'caption': caption,
                    'access_token': self.access_token,
                    'is_made_with_ai': 'true'
                }
            
            container_response = requests.post(container_url, data=container_params)
            container_data = container_response.json()
            
            if 'id' not in container_data:
                print(f"Instagram container creation failed: {container_data}")
                return None
                
            container_id = container_data['id']
            
            # Step 2: Wait for processing (videos only)
            if media_type == 'video':
                status_url = f"{self.base_url}/{container_id}"
                status_params = {
                    'fields': 'status_code',
                    'access_token': self.access_token
                }
                
                for attempt in range(30):
                    status_response = requests.get(status_url, params=status_params)
                    status_data = status_response.json()
                    
                    if status_data.get('status_code') == 'FINISHED':
                        break
                    elif status_data.get('status_code') == 'ERROR':
                        print(f"Instagram processing failed: {status_data}")
                        return None
                        
                    time.sleep(2)
            
            # Step 3: Publish using Instagram Business Account ID
            publish_url = f"{self.base_url}/{self.instagram_account_id}/media_publish"
            publish_params = {
                'creation_id': container_id,
                'access_token': self.access_token
            }
            
            publish_response = requests.post(publish_url, data=publish_params)
            publish_data = publish_response.json()
            
            if 'id' in publish_data:
                print(f"✅ Instagram: Posted {media_type} successfully")
                return publish_data
            else:
                print(f"❌ Instagram: Publishing failed - {publish_data}")
                return None
                
        except Exception as e:
            print(f"❌ Instagram: Error - {e}")
            return None


class TikTokPublisher:
    """TikTok Content Posting API publisher"""
    
    def __init__(self):
        self.access_token = TIKTOK_ACCESS_TOKEN
        self.base_url = "https://open.tiktokapis.com/v2"
    
    def post_content(self, content_data, caption):
        """
        Post video content to TikTok
        
        Args:
            content_data (dict): Content information with 'local_path', 'media_type'
            caption (str): Formatted caption with hashtags
            
        Returns:
            dict: API response or None if failed
        """
        if not self.access_token:
            print("TikTok API credentials not configured")
            return None
            
        if content_data['media_type'] != 'video':
            print("TikTok only supports video content")
            return None
            
        try:
            video_path = content_data['local_path']
            if not os.path.exists(video_path):
                print(f"TikTok: Video file not found - {video_path}")
                return None
                
            # Step 1: Initialize upload
            init_url = f"{self.base_url}/post/publish/video/init/"
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json; charset=UTF-8'
            }
            
            video_size = os.path.getsize(video_path)
            init_data = {
                "post_info": {
                    "title": caption,
                    "privacy_level": "PUBLIC_TO_EVERYONE",
                    "disable_duet": False,
                    "disable_comment": False,
                    "disable_stitch": False,
                    "video_cover_timestamp_ms": 1000
                },
                "source_info": {
                    "source": "FILE_UPLOAD",
                    "video_size": video_size,
                    "chunk_size": video_size,
                    "total_chunk_count": 1
                }
            }
            
            init_response = requests.post(init_url, headers=headers, json=init_data)
            init_result = init_response.json()
            
            if init_result.get('error', {}).get('code') != 'ok':
                print(f"TikTok initialization failed: {init_result}")
                return None
                
            publish_id = init_result['data']['publish_id']
            upload_url = init_result['data']['upload_url']
            
            # Step 2: Upload video
            with open(video_path, 'rb') as video_file:
                files = {'video': video_file}
                upload_headers = {'Authorization': f'Bearer {self.access_token}'}
                upload_response = requests.put(upload_url, headers=upload_headers, files=files)
                
                if upload_response.status_code != 200:
                    print(f"TikTok upload failed: {upload_response.text}")
                    return None
            
            # Step 3: Check status and publish
            status_url = f"{self.base_url}/post/publish/status/fetch/"
            status_data = {"publish_id": publish_id}
            
            for attempt in range(60):
                status_response = requests.post(status_url, headers=headers, json=status_data)
                status_result = status_response.json()
                
                status = status_result.get('data', {}).get('status')
                if status == 'PUBLISH_COMPLETE':
                    print("✅ TikTok: Video posted successfully")
                    return status_result
                elif status == 'FAILED':
                    print(f"❌ TikTok: Publishing failed - {status_result}")
                    return None
                    
                time.sleep(3)
            
            print("❌ TikTok: Upload timed out")
            return None
            
        except Exception as e:
            print(f"❌ TikTok: Error - {e}")
            return None


class TumblrPublisher:
    """Tumblr API publisher"""
    
    def __init__(self):
        # Debug: Check if all Tumblr credentials are present
        print(f"🔍 Tumblr credentials check:")
        print(f"   CONSUMER_KEY: {'✅' if TUMBLR_CONSUMER_KEY else '❌ None'}")
        print(f"   CONSUMER_SECRET: {'✅' if TUMBLR_CONSUMER_SECRET else '❌ None'}")
        print(f"   OAUTH_TOKEN: {'✅' if TUMBLR_OAUTH_TOKEN else '❌ None'}")
        print(f"   OAUTH_TOKEN_SECRET: {'✅' if TUMBLR_OAUTH_TOKEN_SECRET else '❌ None'}")
        print(f"   BLOG_NAME: {'✅' if TUMBLR_BLOG_NAME else '❌ None'}")
        
        if not all([TUMBLR_CONSUMER_KEY, TUMBLR_CONSUMER_SECRET, TUMBLR_OAUTH_TOKEN, TUMBLR_OAUTH_TOKEN_SECRET, TUMBLR_BLOG_NAME]):
            print("❌ Missing Tumblr credentials - posting will fail")
            self.client = None
            return
            
        self.client = pytumblr.TumblrRestClient(
            TUMBLR_CONSUMER_KEY,
            TUMBLR_CONSUMER_SECRET,
            TUMBLR_OAUTH_TOKEN,
            TUMBLR_OAUTH_TOKEN_SECRET
        )
    
    def post_content(self, content_data, caption, hashtags):
        """
        Post content to Tumblr
        
        Args:
            content_data (dict): Content information with 'local_path', 'media_type'
            caption (str): Caption text
            hashtags (list): List of hashtag strings
            
        Returns:
            dict: API response or None if failed
        """
        if not self.client:
            print("❌ Tumblr: Client not initialized due to missing credentials")
            return None
            
        try:
            media_type = content_data['media_type']
            local_path = content_data['local_path']
            
            print(f"🔍 Tumblr: Posting {media_type} with caption: {caption[:50]}...")
            print(f"🔍 Tumblr: Using hashtags: {hashtags}")
            
            if media_type == 'image':
                response = self.client.create_photo(
                    TUMBLR_BLOG_NAME,
                    state="published",
                    tags=hashtags,
                    caption=caption,
                    source=local_path
                )
            else:  # video
                # For video posts, Tumblr uses different parameter names
                response = self.client.create_video(
                    TUMBLR_BLOG_NAME,
                    state="published",
                    tags=hashtags,
                    caption=caption,  # This should work for videos too
                    data=local_path
                )
            
            print(f"🔍 Tumblr API response: {response}")
            
            # Check if the post was created successfully
            if response.get('meta', {}).get('status') == 201:
                # For videos, Tumblr may return 'transcoding' state which is normal
                post_state = response.get('response', {}).get('state', '')
                if post_state == 'transcoding':
                    print("✅ Tumblr: Video posted successfully (processing)")
                else:
                    print("✅ Tumblr: Content posted successfully")
                return response
            else:
                print(f"❌ Tumblr: Posting failed - {response}")
                return None
                
        except Exception as e:
            print(f"❌ Tumblr: Error - {e}")
            return None


class BlueskyPublisher:
    """Bluesky AT Protocol publisher"""
    
    def __init__(self):
        self.client = BskyClient()
        try:
            self.client.login(BLUESKY_USERNAME, BLUESKY_PASSWORD)
        except Exception as e:
            print(f"Bluesky login failed: {e}")
            self.client = None
    
    def post_content(self, content_data, caption, facets=None):
        """
        Post content to Bluesky
        
        Args:
            content_data (dict): Content information with 'local_path', 'media_type'
            caption (str): Formatted caption with hashtags
            facets (list): Bluesky facets for hashtags
            
        Returns:
            dict: API response or None if failed
        """
        if not self.client:
            print("Bluesky client not initialized")
            return None
            
        try:
            media_type = content_data['media_type']
            local_path = content_data['local_path']
            
            with open(local_path, 'rb') as media_file:
                media_data = media_file.read()
            
            if media_type == 'video':
                response = self.client.send_video(
                    text=caption,
                    video=media_data,
                    video_alt=f"Video: {os.path.basename(local_path)}",
                    facets=facets or []
                )
            else:  # image
                response = self.client.send_image(
                    text=caption,
                    image=media_data,
                    image_alt=os.path.basename(local_path),
                    facets=facets or []
                )
            
            print("✅ Bluesky: Content posted successfully")
            return response
            
        except Exception as e:
            print(f"❌ Bluesky: Error - {e}")
            return None


class ThreadsPublisher:
    """Threads API publisher (Meta)"""
    
    def __init__(self):
        self.access_token = THREADS_ACCESS_TOKEN
        self.base_url = "https://graph.threads.net/v1.0"
        self.user_id = None
        self._get_user_id()
    
    def _get_user_id(self):
        """Get the Threads user ID from the access token"""
        if not self.access_token:
            return
        try:
            url = f"{self.base_url}/me"
            params = {
                'access_token': self.access_token,
                'fields': 'id,username'
            }
            response = requests.get(url, params=params)
            data = response.json()
            
            if 'id' in data:
                self.user_id = data['id']
                print(f"✅ Threads: Connected as @{data.get('username', 'unknown')}")
            else:
                print(f"❌ Threads: Failed to get user ID - {data}")
        except Exception as e:
            print(f"❌ Threads: Error getting user ID - {e}")
    
    def post_content(self, content_data, caption):
        """
        Post content to Threads
        
        Args:
            content_data (dict): Content information with 'url', 'media_type'
            caption (str): Formatted caption with hashtags
            
        Returns:
            dict: API response or None if failed
        """
        if not self.access_token or not self.user_id:
            print("❌ Threads: API credentials not configured or user ID not found")
            return None
            
        try:
            media_type = content_data['media_type']
            media_url = content_data['url']
            
            # Step 1: Create media container
            container_url = f"{self.base_url}/{self.user_id}/threads"
            
            if media_type == 'video':
                container_params = {
                    'media_type': 'VIDEO',
                    'video_url': media_url,
                    'text': caption,
                    'access_token': self.access_token,
                    'is_made_with_ai': 'true'
                }
            else:  # image
                container_params = {
                    'media_type': 'IMAGE',
                    'image_url': media_url,
                    'text': caption,
                    'access_token': self.access_token,
                    'is_made_with_ai': 'true'
                }
            
            print(f"🔄 Threads: Creating {media_type} container...")
            container_response = requests.post(container_url, data=container_params)
            container_data = container_response.json()
            
            if 'id' not in container_data:
                print(f"❌ Threads: Container creation failed - {container_data}")
                return None
                
            container_id = container_data['id']
            print(f"✅ Threads: Container created (ID: {container_id})")
            
            # Step 2: Wait for processing (especially for videos)
            status_url = f"{self.base_url}/{container_id}"
            status_params = {
                'fields': 'status',
                'access_token': self.access_token
            }
            
            for attempt in range(30):
                status_response = requests.get(status_url, params=status_params)
                status_data = status_response.json()
                status = status_data.get('status')
                
                if status == 'FINISHED':
                    print("✅ Threads: Media processing complete")
                    break
                elif status == 'ERROR':
                    print(f"❌ Threads: Media processing failed - {status_data}")
                    return None
                elif status == 'IN_PROGRESS':
                    print(f"🔄 Threads: Processing... (attempt {attempt + 1}/30)")
                    time.sleep(2)
                else:
                    # For images, status might not be returned
                    break
            
            # Step 3: Publish
            publish_url = f"{self.base_url}/{self.user_id}/threads_publish"
            publish_params = {
                'creation_id': container_id,
                'access_token': self.access_token
            }
            
            print("🔄 Threads: Publishing...")
            publish_response = requests.post(publish_url, data=publish_params)
            publish_data = publish_response.json()
            
            if 'id' in publish_data:
                print(f"✅ Threads: Posted {media_type} successfully (ID: {publish_data['id']})")
                return publish_data
            else:
                print(f"❌ Threads: Publishing failed - {publish_data}")
                return None
                
        except Exception as e:
            print(f"❌ Threads: Error - {e}")
            return None


def post_to_all_platforms(content_data, captions_data):
    """
    Post content to all platforms simultaneously
    
    Args:
        content_data (dict): Content information
        captions_data (dict): Platform-specific captions and hashtags
        
    Returns:
        dict: Results from all platforms
    """
    results = {}
    
    # Instagram
    instagram = InstagramPublisher()
    results['instagram'] = instagram.post_content(
        content_data, 
        captions_data['instagram']
    )
    
    # TikTok (videos only)
    if content_data['media_type'] == 'video':
        tiktok = TikTokPublisher()
        results['tiktok'] = tiktok.post_content(
            content_data,
            captions_data['tiktok']
        )
    else:
        results['tiktok'] = "Skipped (images not supported)"
    
    # Tumblr
    tumblr = TumblrPublisher()
    results['tumblr'] = tumblr.post_content(
        content_data,
        captions_data['tumblr'],
        captions_data['hashtags']['tumblr']
    )
    
    # Bluesky
    bluesky = BlueskyPublisher()
    from caption_generator import CaptionGenerator
    generator = CaptionGenerator()
    facets = generator.get_bluesky_facets(
        captions_data['bluesky'],
        captions_data['hashtags']['bluesky']
    )
    results['bluesky'] = bluesky.post_content(
        content_data,
        captions_data['bluesky'],
        facets
    )
    
    # Threads
    threads = ThreadsPublisher()
    results['threads'] = threads.post_content(
        content_data,
        captions_data.get('threads', captions_data['instagram'])  # Fallback to Instagram caption
    )
    
    return results
