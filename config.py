"""
Configuration settings for the scheduled posting system
"""

import os
from dotenv import load_dotenv

load_dotenv()

# AWS Configuration
# Bedrock AI credentials (for caption generation)
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

# S3 Storage credentials (separate from Bedrock)
AWS_ACCESS_KEY_ID_S3 = os.getenv('AWS_ACCESS_KEY_ID_S3')
AWS_SECRET_ACCESS_KEY_S3 = os.getenv('AWS_SECRET_ACCESS_KEY_S3')

# S3 Configuration
S3_BUCKET = os.getenv('S3_BUCKET', 'majindonpatch-public')
S3_PATH = 'posts_insta'
S3_URL_BASE = f'https://{S3_BUCKET}.s3.amazonaws.com/{S3_PATH}/'

# Social Media API Configuration
INSTAGRAM_ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN')
INSTAGRAM_PAGE_ID = os.getenv('INSTAGRAM_PAGE_ID')
TIKTOK_ACCESS_TOKEN = os.getenv('TIKTOK_ACCESS_TOKEN')
# AWS Bedrock is used for AI captions (using same AWS credentials as S3)

# Tumblr API Configuration
TUMBLR_CONSUMER_KEY = os.getenv('TUMBLR_CONSUMER_KEY')
TUMBLR_CONSUMER_SECRET = os.getenv('TUMBLR_CONSUMER_SECRET')
TUMBLR_OAUTH_TOKEN = os.getenv('TUMBLR_OAUTH_TOKEN')
TUMBLR_OAUTH_TOKEN_SECRET = os.getenv('TUMBLR_OAUTH_TOKEN_SECRET')
TUMBLR_BLOG_NAME = os.getenv('TUMBLR_BLOG_NAME')

# Bluesky Configuration
BLUESKY_USERNAME = os.getenv('BLUESKY_USERNAME')
BLUESKY_PASSWORD = os.getenv('BLUESKY_PASSWORD')

# Content Settings
SUPPORTED_IMAGE_FORMATS = ['.png', '.jpg', '.jpeg', '.gif']
SUPPORTED_VIDEO_FORMATS = ['.mp4', '.mov', '.avi']
MAX_IMAGE_SIZE = (1080, 1080)

# File paths
MEDIA_LINKS_FILE = 'scheduled_posts/media_links.json'
CONTENT_QUEUE_FILE = 'scheduled_posts/content_queue.json'
