"""
Main orchestrator for scheduled posting system
Clean, minimal entry point that coordinates all components
"""

import sys
import os
import requests
from datetime import datetime
from content_queue import get_next_post, mark_posted, get_status, cleanup_queue
from caption_generator import generate_content_captions
from platform_publishers import post_to_all_platforms


def download_file_from_s3(s3_url, local_path):
    """
    Download file from S3 URL to local path for platforms that need local files
    
    Args:
        s3_url (str): S3 URL of the file
        local_path (str): Local path where to save the file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        # Download file from S3
        print(f"📥 Downloading {os.path.basename(local_path)} from S3...")
        response = requests.get(s3_url)
        response.raise_for_status()
        
        # Save to local path
        with open(local_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Downloaded to {local_path}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to download file: {e}")
        return False


def main():
    """
    Main posting function - called by GitHub Actions on schedule
    """
    print(f"🚀 Starting scheduled posting at {datetime.now()}")
    
    # Get next content to post
    content = get_next_post()
    if not content:
        print("📭 No content available to post")
        return
    
    print(f"🎯 Selected content: {content['filename']} (ID: {content['id']})")
    
    # Generate captions for all platforms
    print("🤖 Generating captions...")
    try:
        captions = generate_content_captions(content['url'])
        print(f"✅ Generated caption: {captions['base_caption']}")
    except Exception as e:
        print(f"❌ Caption generation failed: {e}")
        return
    
    # Download file from S3 to local path for platforms that need local files
    local_path = content.get('local_path')
    if local_path and not os.path.exists(local_path):
        if not download_file_from_s3(content['url'], local_path):
            print("❌ Failed to download file for local platforms")
            return
    
    # Prepare content data for posting
    content_data = {
        'url': content['url'],
        'local_path': local_path,
        'media_type': content['media_type'],
        'filename': content['filename']
    }
    
    # Post to all platforms simultaneously
    print("📤 Posting to all platforms...")
    try:
        results = post_to_all_platforms(content_data, captions)
        
        # Log results
        print("\n📊 Posting Results:")
        for platform, result in results.items():
            if result and result != "Skipped (images not supported)":
                print(f"   ✅ {platform.capitalize()}: Success")
            elif result == "Skipped (images not supported)":
                print(f"   ⏭️ {platform.capitalize()}: {result}")
            else:
                print(f"   ❌ {platform.capitalize()}: Failed")
        
        # Mark as posted
        mark_posted(content['id'], results)
        
        print(f"✅ Successfully posted: {content['filename']}")
        
    except Exception as e:
        print(f"❌ Posting failed: {e}")
        return
    
    # Clean up old posted items (keep last 30 days)
    cleanup_queue(30)
    
    # Show queue status
    status = get_status()
    print(f"\n📈 Queue Status: {status['pending_items']} pending, {status['posted_items']} posted")


def show_status():
    """Show current queue status"""
    status = get_status()
    print(f"📊 Content Queue Status:")
    print(f"   Total items: {status['total_items']}")
    print(f"   Posted items: {status['posted_items']}")
    print(f"   Pending items: {status['pending_items']}")
    
    if status['pending_items'] > 0:
        print(f"\n📋 Next few items to post:")
        unposted = [item for item in status['queue'] if not item['posted']]
        for i, item in enumerate(unposted[:5]):
            print(f"   {i+1}. {item['filename']} ({item['media_type']}) - Added: {item['added_date'][:10]}")


if __name__ == "__main__":
    # Handle command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "status":
            show_status()
        elif sys.argv[1] == "post":
            main()
        else:
            print("Usage: python main.py [status|post]")
    else:
        # Default action is to post
        main()
