"""
Content queue management system
Simple, clean queue operations for scheduled posting
"""

import json
import os
import random
from datetime import datetime
from config import CONTENT_QUEUE_FILE, MEDIA_LINKS_FILE


class ContentQueue:
    """
    Manages the content posting queue
    Simple Python data structures for clean queue operations
    """
    
    def __init__(self):
        self.queue_file = CONTENT_QUEUE_FILE
        self.links_file = MEDIA_LINKS_FILE
        self.queue = self._load_queue()
        self.media_links = self._load_media_links()
    
    def _load_queue(self):
        """Load queue from file or create empty queue with duplicate ID validation"""
        if os.path.exists(self.queue_file):
            try:
                with open(self.queue_file, 'r') as f:
                    queue = json.load(f)
                    
                # Validate and fix duplicate IDs
                queue = self._validate_and_fix_duplicate_ids(queue)
                return queue
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def _validate_and_fix_duplicate_ids(self, queue):
        """
        Validate queue for duplicate IDs and fix them
        
        Args:
            queue (list): The loaded queue
            
        Returns:
            list: Queue with fixed IDs
        """
        if not queue:
            return queue
            
        seen_ids = set()
        fixed_queue = []
        max_id = max([item.get('id', 0) for item in queue], default=0)
        needs_save = False
        
        for item in queue:
            item_id = item.get('id')
            
            if item_id in seen_ids:
                # Duplicate ID found - assign new unique ID
                max_id += 1
                old_id = item_id
                item['id'] = max_id
                print(f"⚠️ Fixed duplicate ID {old_id} -> {max_id} for {item.get('filename', 'unknown')}")
                needs_save = True
            
            seen_ids.add(item['id'])
            fixed_queue.append(item)
        
        # Save the fixed queue if changes were made
        if needs_save:
            print("💾 Saving queue with fixed duplicate IDs...")
            with open(self.queue_file, 'w') as f:
                json.dump(fixed_queue, f, indent=2)
        
        return fixed_queue
    
    def _save_queue(self):
        """Save queue to file"""
        os.makedirs(os.path.dirname(self.queue_file), exist_ok=True)
        with open(self.queue_file, 'w') as f:
            json.dump(self.queue, f, indent=2)
    
    def _load_media_links(self):
        """Load media links tracking file"""
        if os.path.exists(self.links_file):
            try:
                with open(self.links_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def _save_media_links(self):
        """Save media links to file"""
        os.makedirs(os.path.dirname(self.links_file), exist_ok=True)
        with open(self.links_file, 'w') as f:
            json.dump(self.media_links, f, indent=2)
    
    def add_content(self, filename, s3_url, media_type, local_path=None):
        """
        Add content to the posting queue with fun facts generation
        
        Args:
            filename (str): Original filename
            s3_url (str): S3 URL of the uploaded content
            media_type (str): 'image' or 'video'
            local_path (str): Local path for platforms that need it
            
        Returns:
            dict: The content item added to queue
        """
        # Generate complete caption data for the content
        print(f"🤖 Generating complete caption data for {filename}...")
        try:
            from caption_generator import generate_content_captions
            captions_data = generate_content_captions(s3_url)
            
            kaomoji = captions_data['base_caption']
            fun_fact = captions_data['fun_fact']
            fun_fact_followup = captions_data['fun_fact_followup']
            hashtags = captions_data['hashtags']['instagram']  # Same hashtags for all platforms
            platform_captions = {
                'instagram': captions_data['instagram'],
                'tiktok': captions_data['tiktok'],
                'tumblr': captions_data['tumblr'],
                'bluesky': captions_data['bluesky']
            }
            engagement_hook_used = True
            
            print(f"✅ Generated complete caption data for {filename}")
            
        except Exception as e:
            print(f"⚠️ Failed to generate caption data for {filename}: {e}")
            kaomoji = ""
            fun_fact = ""
            fun_fact_followup = ""
            hashtags = []
            platform_captions = {
                'instagram': "",
                'tiktok': "",
                'tumblr': "",
                'bluesky': ""
            }
            engagement_hook_used = False
        
        content_item = {
            'id': max([item['id'] for item in self.queue], default=0) + 1,
            'filename': filename,
            'url': s3_url,
            'media_type': media_type,
            'local_path': local_path,
            'added_date': datetime.now().isoformat(),
            'posted': False,
            'posted_date': None,
            'posting_results': {},
            'kaomoji': kaomoji,
            'fun_fact': fun_fact,
            'fun_fact_followup': fun_fact_followup,
            'hashtags': hashtags,
            'platform_captions': platform_captions,
            'engagement_hook_used': engagement_hook_used
        }
        
        self.queue.append(content_item)
        self._save_queue()
        
        # Also track in media links for permanent record
        link_record = {
            'filename': filename,
            'url': s3_url,
            'media_type': media_type,
            'upload_date': datetime.now().isoformat()
        }
        self.media_links.append(link_record)
        self._save_media_links()
        
        print(f"✅ Added to queue: {filename} -> {s3_url}")
        return content_item
    
    def get_next_content(self):
        """
        Get the next content item to post (random selection from unposted)
        
        Returns:
            dict: Content item to post, or None if queue is empty
        """
        unposted = [item for item in self.queue if not item['posted']]
        
        if not unposted:
            print("📭 No content available in queue")
            return None
        
        # Random selection from unposted content
        selected = random.choice(unposted)
        print(f"🎯 Selected for posting: {selected['filename']}")
        return selected
    
    def mark_as_posted(self, content_id, results):
        """
        Mark content as posted with results
        
        Args:
            content_id (int): ID of the content item
            results (dict): Results from platform posting
        """
        # Clean results to make them JSON serializable
        clean_results = self._clean_results_for_json(results)
        
        for item in self.queue:
            if item['id'] == content_id:
                item['posted'] = True
                item['posted_date'] = datetime.now().isoformat()
                item['posting_results'] = clean_results
                break
        
        self._save_queue()
        print(f"✅ Marked as posted: ID {content_id}")
    
    def _clean_results_for_json(self, results):
        """
        Clean posting results to make them JSON serializable
        
        Args:
            results (dict): Raw results from platform posting
            
        Returns:
            dict: JSON-serializable results
        """
        clean_results = {}
        
        for platform, result in results.items():
            if result is None:
                clean_results[platform] = None
            elif isinstance(result, str):
                clean_results[platform] = result
            elif isinstance(result, dict):
                clean_results[platform] = result
            elif hasattr(result, '__dict__'):
                # Convert objects to dict, but only keep basic info
                try:
                    if hasattr(result, 'uri') and hasattr(result, 'cid'):
                        # Bluesky response
                        clean_results[platform] = {
                            'uri': str(result.uri),
                            'cid': str(result.cid),
                            'success': True
                        }
                    else:
                        # Generic object - try to get useful info
                        clean_results[platform] = {
                            'success': True,
                            'type': type(result).__name__
                        }
                except:
                    clean_results[platform] = {'success': True, 'serialized': str(result)}
            else:
                # Fallback - convert to string
                clean_results[platform] = str(result)
        
        return clean_results
    
    def get_queue_status(self):
        """
        Get current queue status
        
        Returns:
            dict: Queue statistics
        """
        total = len(self.queue)
        posted = len([item for item in self.queue if item['posted']])
        pending = total - posted
        
        return {
            'total_items': total,
            'posted_items': posted,
            'pending_items': pending,
            'queue': self.queue
        }
    
    def cleanup_old_posted(self, days_old=30):
        """
        Remove old posted items from queue (keeps media_links intact)
        
        Args:
            days_old (int): Remove items posted more than this many days ago
        """
        from datetime import datetime, timedelta
        
        cutoff_date = datetime.now() - timedelta(days=days_old)
        original_count = len(self.queue)
        
        self.queue = [
            item for item in self.queue
            if not item['posted'] or 
            (item['posted_date'] and 
             datetime.fromisoformat(item['posted_date']) > cutoff_date)
        ]
        
        removed_count = original_count - len(self.queue)
        if removed_count > 0:
            self._save_queue()
            print(f"🧹 Cleaned up {removed_count} old posted items")
        
        return removed_count
    
    def get_media_links(self):
        """
        Get all media links (permanent record)
        
        Returns:
            list: All uploaded media links
        """
        return self.media_links


# Convenience functions for easy use in main script
def add_to_queue(filename, s3_url, media_type, local_path=None):
    """Add content to queue"""
    queue = ContentQueue()
    return queue.add_content(filename, s3_url, media_type, local_path)


def get_next_post():
    """Get next content to post"""
    queue = ContentQueue()
    return queue.get_next_content()


def mark_posted(content_id, results):
    """Mark content as posted"""
    queue = ContentQueue()
    queue.mark_as_posted(content_id, results)


def get_status():
    """Get queue status"""
    queue = ContentQueue()
    return queue.get_queue_status()


def cleanup_queue(days_old=30):
    """Clean up old posted items"""
    queue = ContentQueue()
    return queue.cleanup_old_posted(days_old)
