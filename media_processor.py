"""
Media processing system
Handles GitHub → S3 → Delete workflow for uploaded media files
"""

import os
import boto3
import shutil
from PIL import Image
from pathlib import Path
from config import (
    AWS_ACCESS_KEY_ID_S3, AWS_SECRET_ACCESS_KEY_S3, S3_BUCKET, S3_PATH, S3_URL_BASE,
    SUPPORTED_IMAGE_FORMATS, SUPPORTED_VIDEO_FORMATS, MAX_IMAGE_SIZE
)
from content_queue import add_to_queue


class MediaProcessor:
    """
    Processes media files: resize, upload to S3, add to queue, cleanup
    """
    
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID_S3,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY_S3
        )
        self.media_folder = 'media'
        self.temp_folder = 'temp'
    
    def get_media_type(self, filename):
        """
        Determine if file is image or video
        
        Args:
            filename (str): Name of the file
            
        Returns:
            str: 'image', 'video', or None if unsupported
        """
        file_ext = Path(filename).suffix.lower()
        
        if file_ext in SUPPORTED_IMAGE_FORMATS:
            return 'image'
        elif file_ext in SUPPORTED_VIDEO_FORMATS:
            return 'video'
        else:
            return None
    
    def process_image(self, file_path, output_path):
        """
        Process and resize image if needed
        
        Args:
            file_path (str): Path to original image
            output_path (str): Path for processed image
            
        Returns:
            bool: True if successful
        """
        try:
            with Image.open(file_path) as img:
                # Convert to RGB if needed
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize if larger than max size
                if img.width > MAX_IMAGE_SIZE[0] or img.height > MAX_IMAGE_SIZE[1]:
                    img = img.resize(MAX_IMAGE_SIZE, Image.Resampling.LANCZOS)
                    print(f"📐 Resized image to {MAX_IMAGE_SIZE}")
                
                # Save as JPEG
                img.save(output_path, 'JPEG', quality=90, optimize=True)
                return True
                
        except Exception as e:
            print(f"❌ Error processing image: {e}")
            return False
    
    def process_video(self, file_path, output_path):
        """
        Process video (currently just copies, but can be extended)
        
        Args:
            file_path (str): Path to original video
            output_path (str): Path for processed video
            
        Returns:
            bool: True if successful
        """
        try:
            # For now, just copy the video
            # Future: could add video compression, format conversion, etc.
            shutil.copy2(file_path, output_path)
            print(f"📹 Video copied for processing")
            return True
            
        except Exception as e:
            print(f"❌ Error processing video: {e}")
            return False
    
    def upload_to_s3(self, file_path, s3_key):
        """
        Upload file to S3
        
        Args:
            file_path (str): Local file path
            s3_key (str): S3 object key
            
        Returns:
            str: S3 URL if successful, None if failed
        """
        try:
            self.s3_client.upload_file(file_path, S3_BUCKET, s3_key)
            s3_url = f"{S3_URL_BASE}{os.path.basename(s3_key)}"
            print(f"☁️ Uploaded to S3: {s3_url}")
            return s3_url
            
        except Exception as e:
            print(f"❌ S3 upload failed: {e}")
            return None
    
    def process_media_files(self):
        """
        Process all media files in the media folder
        
        Returns:
            list: List of processed files with their S3 URLs
        """
        if not os.path.exists(self.media_folder):
            print(f"📁 Media folder not found: {self.media_folder}")
            return []
        
        # Create temp folder for processing
        os.makedirs(self.temp_folder, exist_ok=True)
        
        processed_files = []
        media_files = [f for f in os.listdir(self.media_folder) 
                      if os.path.isfile(os.path.join(self.media_folder, f))
                      and not f.startswith('.')]
        
        if not media_files:
            print("📭 No media files found to process")
            return []
        
        print(f"🔄 Processing {len(media_files)} media files...")
        
        for filename in media_files:
            file_path = os.path.join(self.media_folder, filename)
            media_type = self.get_media_type(filename)
            
            if not media_type:
                print(f"⚠️ Unsupported file type: {filename}")
                continue
            
            print(f"🎯 Processing {media_type}: {filename}")
            
            # Generate processed filename
            base_name = Path(filename).stem
            if media_type == 'image':
                processed_filename = f"{base_name}_processed.jpg"
            else:  # video
                processed_filename = f"{base_name}_processed{Path(filename).suffix}"
            
            processed_path = os.path.join(self.temp_folder, processed_filename)
            
            # Process the file
            if media_type == 'image':
                success = self.process_image(file_path, processed_path)
            else:  # video
                success = self.process_video(file_path, processed_path)
            
            if not success:
                print(f"❌ Failed to process: {filename}")
                continue
            
            # Upload to S3
            s3_key = f"{S3_PATH}/{processed_filename}"
            s3_url = self.upload_to_s3(processed_path, s3_key)
            
            if s3_url:
                # Add to content queue
                queue_item = add_to_queue(
                    filename=filename,
                    s3_url=s3_url,
                    media_type=media_type,
                    local_path=processed_path  # Keep temp file for platforms that need it
                )
                
                processed_files.append({
                    'original_filename': filename,
                    'processed_filename': processed_filename,
                    's3_url': s3_url,
                    'media_type': media_type,
                    'queue_id': queue_item['id']
                })
                
                # Remove original file from media folder
                os.remove(file_path)
                print(f"🗑️ Removed original file: {filename}")
            
            else:
                print(f"❌ Failed to upload: {filename}")
                # Clean up processed file if upload failed
                if os.path.exists(processed_path):
                    os.remove(processed_path)
        
        print(f"✅ Processed {len(processed_files)} files successfully")
        return processed_files
    
    def cleanup_temp_files(self, older_than_hours=24):
        """
        Clean up old temporary files
        
        Args:
            older_than_hours (int): Remove files older than this many hours
        """
        if not os.path.exists(self.temp_folder):
            return
        
        import time
        current_time = time.time()
        cutoff_time = current_time - (older_than_hours * 3600)
        
        removed_count = 0
        for filename in os.listdir(self.temp_folder):
            file_path = os.path.join(self.temp_folder, filename)
            if os.path.isfile(file_path):
                file_time = os.path.getmtime(file_path)
                if file_time < cutoff_time:
                    os.remove(file_path)
                    removed_count += 1
        
        if removed_count > 0:
            print(f"🧹 Cleaned up {removed_count} old temp files")


def process_new_media():
    """
    Main function to process new media files
    Called by GitHub Actions when new files are detected
    
    Returns:
        dict: Processing results
    """
    processor = MediaProcessor()
    
    # Process all media files
    processed_files = processor.process_media_files()
    
    # Clean up old temp files
    processor.cleanup_temp_files()
    
    # Return summary
    return {
        'processed_count': len(processed_files),
        'processed_files': processed_files,
        'timestamp': os.environ.get('GITHUB_RUN_ID', 'local-run')
    }


if __name__ == "__main__":
    # For testing locally
    results = process_new_media()
    print(f"\n📊 Processing Summary:")
    print(f"   Files processed: {results['processed_count']}")
    for file_info in results['processed_files']:
        print(f"   ✅ {file_info['original_filename']} → {file_info['s3_url']}")
