"""
Simplified AI-powered caption and hashtag generation
Single AI call returns both kaomoji and hashtags
"""

import boto3
import requests
import io
import json
import subprocess
import tempfile
import os
from PIL import Image
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


class CaptionGenerator:
    """
    Simplified AI caption and hashtag generator
    Uses AWS Bedrock Nova vision model with single call for both caption and hashtags
    """
    
    def __init__(self):
        self.bedrock_runtime = boto3.client(
            service_name='bedrock-runtime',
            region_name='eu-west-2',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
        self.model_id = 'amazon.nova-pro-v1:0'
    
    def to_bold_unicode(self, text):
        """
        Convert text to Unicode bold characters for Instagram
        
        Args:
            text (str): Text to convert to bold
            
        Returns:
            str: Text with Unicode bold characters
        """
        bold_map = {
            'A': '𝗔', 'B': '𝗕', 'C': '𝗖', 'D': '𝗗', 'E': '𝗘', 'F': '𝗙', 'G': '𝗚', 'H': '𝗛',
            'I': '𝗜', 'J': '𝗝', 'K': '𝗞', 'L': '𝗟', 'M': '𝗠', 'N': '𝗡', 'O': '𝗢', 'P': '𝗣',
            'Q': '𝗤', 'R': '𝗥', 'S': '𝗦', 'T': '𝗧', 'U': '𝗨', 'V': '𝗩', 'W': '𝗪', 'X': '𝗫',
            'Y': '𝗬', 'Z': '𝗭', 'a': '𝗮', 'b': '𝗯', 'c': '𝗰', 'd': '𝗱', 'e': '𝗲', 'f': '𝗳',
            'g': '𝗴', 'h': '𝗵', 'i': '𝗶', 'j': '𝗷', 'k': '𝗸', 'l': '𝗹', 'm': '𝗺', 'n': '𝗻',
            'o': '𝗼', 'p': '𝗽', 'q': '𝗾', 'r': '𝗿', 's': '𝘀', 't': '𝘁', 'u': '𝘂', 'v': '𝘃',
            'w': '𝘄', 'x': '𝘅', 'y': '𝘆', 'z': '𝘇', '0': '𝟬', '1': '𝟭', '2': '𝟮', '3': '𝟯',
            '4': '𝟰', '5': '𝟱', '6': '𝟲', '7': '𝟳', '8': '𝟴', '9': '𝟵'
        }
        return ''.join(bold_map.get(char, char) for char in text)
    
    def _shorten_video_for_llm(self, video_bytes, max_duration=10):
        """
        Create a shortened version of video for LLM analysis (max 10 seconds)
        
        Args:
            video_bytes (bytes): Original video bytes
            max_duration (int): Maximum duration in seconds
            
        Returns:
            bytes: Shortened video bytes, or original if shortening fails
        """
        try:
            # Create temporary files
            with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_input:
                temp_input.write(video_bytes)
                temp_input_path = temp_input.name
            
            with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_output:
                temp_output_path = temp_output.name
            
            # Use ffmpeg to create 10-second clip from the beginning
            cmd = [
                'ffmpeg', '-y',  # -y to overwrite output file
                '-i', temp_input_path,
                '-t', str(max_duration),  # Duration limit
                '-c:v', 'libx264',  # Video codec
                '-c:a', 'aac',      # Audio codec
                '-movflags', '+faststart',  # Optimize for streaming
                temp_output_path
            ]
            
            print(f"🎬 Shortening video to {max_duration} seconds for LLM analysis...")
            
            # Run ffmpeg
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Read the shortened video
                with open(temp_output_path, 'rb') as f:
                    shortened_bytes = f.read()
                
                print(f"✅ Video shortened successfully")
                return shortened_bytes
            else:
                print(f"⚠️ ffmpeg failed, using original video: {result.stderr}")
                return video_bytes
                
        except Exception as e:
            print(f"⚠️ Video shortening failed, using original: {e}")
            return video_bytes
        finally:
            # Clean up temporary files
            try:
                if 'temp_input_path' in locals():
                    os.unlink(temp_input_path)
                if 'temp_output_path' in locals():
                    os.unlink(temp_output_path)
            except:
                pass
    
    def _download_media(self, media_url):
        """
        Download media from URL and convert to format needed by Bedrock
        For videos, creates a 10-second clip for LLM analysis
        
        Args:
            media_url (str): URL of the media file
            
        Returns:
            tuple: (media_bytes, media_type) where media_type is 'image' or 'video'
        """
        try:
            response = requests.get(media_url)
            response.raise_for_status()
            
            # Check if it's a video file
            if media_url.lower().endswith(('.mp4', '.mov', '.avi', '.webm')):
                # For videos, shorten to 10 seconds for LLM analysis
                original_bytes = response.content
                shortened_bytes = self._shorten_video_for_llm(original_bytes, max_duration=10)
                return shortened_bytes, 'video'
            else:
                # For images, process with PIL
                image = Image.open(io.BytesIO(response.content))
                
                # Convert to RGB if needed
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                
                # Convert to bytes
                img_buffer = io.BytesIO()
                image.save(img_buffer, format='PNG')
                img_buffer.seek(0)
                
                return img_buffer.getvalue(), 'image'
            
        except Exception as e:
            print(f"Error downloading media: {e}")
            return None, None
    
    def generate_caption_and_hashtags(self, media_url):
        """
        Generate both caption and hashtags in a single AI call
        
        Args:
            media_url (str): URL of the media to analyze
            
        Returns:
            dict: {'kaomoji': str, 'hashtags': [str, str, str]} or {'kaomoji': '', 'hashtags': []}
        """
        try:
            # Download and prepare media
            media_bytes, media_type = self._download_media(media_url)
            if not media_bytes:
                return {'kaomoji': '', 'hashtags': []}
            
            # Enhanced prompt for kaomoji, two fun facts, and niche hashtags
            prompt = """Analyze this visual content as a learned connoisseur and return a JSON object with:
            1. A kaomoji (text ascii emoticon) that relates to an element in the content; make it creative and fitting, not generic.
            2. A curious, not widely known fun fact about something related to what you see (aesthetic movement, technique, cultural reference, art history, etc.) - write as an expert sharing insider knowledge; write it in a concise and engaging way, not acknowledging the video nor talking about it nor of its object, but simply sharing a fact, with dates, names, and details. The more obscure the better.
            3. A SECOND related but different fun fact on the same theme - this should complement the first fact but offer new information. Make it equally fascinating and obscure.
            4. Exactly 3 niche hashtags focused on specific aesthetic movements, art techniques, or visual culture concepts

            Return ONLY a valid JSON object in this exact format:
            {
            "kaomoji": "your_kaomoji_here",
            "fun_fact": "First fascinating, lesser-known fact about the visual elements, techniques, or cultural context you observe",
            "fun_fact_followup": "Second related but different fascinating fact that complements the first",
            "hashtags": ["niche_aesthetic1", "specific_technique2", "cultural_movement3"]
            }

            Focus on obscure aesthetic movements, specific art techniques, visual culture theory, and niche artistic concepts. Make hashtags highly specific and cultured. Do not include # symbols in hashtags."""
            
            # Create message content for Nova
            if media_type == 'video':
                message_content = [
                    {"text": prompt},
                    {
                        "video": {
                            "format": "mp4",
                            "source": {
                                "bytes": media_bytes
                            }
                        }
                    }
                ]
            else:  # image
                message_content = [
                    {"text": prompt},
                    {
                        "image": {
                            "format": "png",
                            "source": {
                                "bytes": media_bytes
                            }
                        }
                    }
                ]
            
            # Create conversation format for Nova
            conversation = [{
                "role": "user",
                "content": message_content
            }]
            
            print(f"🤖 Generating caption and hashtags for {media_type}...")
            
            # Call the Nova API
            response = self.bedrock_runtime.converse(
                modelId=self.model_id,
                messages=conversation,
                inferenceConfig={
                    "maxTokens": 500,
                    "temperature": 0.7,
                    "topP": 0.9
                }
            )
            
            # Extract response text
            model_response = response["output"]["message"]["content"][0]["text"]
            
            print(f"✅ AI Response: {model_response[:100]}...")
            
            # Parse JSON response
            try:
                result = json.loads(model_response.strip())
                
                # Validate structure
                if 'kaomoji' in result and 'hashtags' in result and 'fun_fact' in result and 'fun_fact_followup' in result:
                    # Ensure hashtags is a list of exactly 3 items
                    hashtags = result['hashtags'][:3] if isinstance(result['hashtags'], list) else []
                    
                    return {
                        'kaomoji': str(result['kaomoji']),
                        'fun_fact': str(result['fun_fact']),
                        'fun_fact_followup': str(result['fun_fact_followup']),
                        'hashtags': hashtags
                    }
                else:
                    print("❌ Invalid JSON structure from AI")
                    return {'kaomoji': '', 'fun_fact': '', 'fun_fact_followup': '', 'hashtags': []}
                    
            except json.JSONDecodeError as e:
                print(f"❌ Failed to parse AI response as JSON: {e}")
                return {'kaomoji': '', 'fun_fact': '', 'fun_fact_followup': '', 'hashtags': []}
            
        except Exception as e:
            print(f"❌ Error generating content: {e}")
            return {'kaomoji': '', 'fun_fact': '', 'fun_fact_followup': '', 'hashtags': []}
    
    def format_caption_for_platform(self, kaomoji, fun_fact, hashtags, platform):
        """
        Format caption with fun fact and hashtags for specific platform
        
        Args:
            kaomoji (str): Base kaomoji caption
            fun_fact (str): Curious fun fact about the content
            hashtags (list): List of hashtag strings
            platform (str): Platform name
            
        Returns:
            str: Formatted caption with fun fact and hashtags
        """
        if not kaomoji and not fun_fact and not hashtags:
            return ""
        
        # Build the content parts
        content_parts = []
        if kaomoji:
            content_parts.append(kaomoji)
        if fun_fact:
            content_parts.append(fun_fact)
        
        main_content = '\n\n'.join(content_parts)
        hashtags_text = ' '.join([f"#{tag}" for tag in hashtags]) if hashtags else ""
        
        if platform == 'instagram':
            # Instagram: kaomoji + newline + fun_fact + double newline + hashtags
            if hashtags_text:
                return f"{main_content}\n\n{hashtags_text}" if main_content else hashtags_text
            else:
                return main_content
            
        elif platform == 'tiktok':
            # TikTok: kaomoji + newline + fun_fact + space + hashtags, limited to 150 chars
            if hashtags_text:
                full_text = f"{main_content} {hashtags_text}" if main_content else hashtags_text
            else:
                full_text = main_content
            return full_text[:147] + "..." if len(full_text) > 150 else full_text
            
        elif platform == 'tumblr':
            # Tumblr: kaomoji + newline + fun_fact (hashtags handled separately as tags)
            return main_content
            
        elif platform == 'bluesky':
            # Bluesky: kaomoji + newline + fun_fact + double newline + hashtags (with facets)
            # Bluesky has a 300 character limit, so we need to be more careful
            if hashtags_text:
                full_text = f"{main_content}\n\n{hashtags_text}" if main_content else hashtags_text
            else:
                full_text = main_content
            
            # If too long, try just kaomoji + hashtags
            if len(full_text) > 300:
                if kaomoji and hashtags_text:
                    fallback_text = f"{kaomoji}\n\n{hashtags_text}"
                    if len(fallback_text) <= 300:
                        return fallback_text
                # If still too long, just kaomoji
                if kaomoji and len(kaomoji) <= 300:
                    return kaomoji
                # Last resort: just hashtags
                if hashtags_text and len(hashtags_text) <= 300:
                    return hashtags_text
                # If everything is too long, return empty
                return ""
            
            return full_text
            
        else:
            # Default: kaomoji + newline + fun_fact + space + hashtags
            if hashtags_text:
                return f"{main_content} {hashtags_text}" if main_content else hashtags_text
            else:
                return main_content
    
    def get_bluesky_facets(self, full_text, hashtags):
        """
        Generate Bluesky facets for hashtags
        
        Args:
            full_text (str): Complete text with hashtags
            hashtags (list): List of hashtag strings
            
        Returns:
            list: Bluesky facets for hashtags
        """
        if not hashtags:
            return []
            
        facets = []
        
        # Find the start of hashtags section (after double newline)
        hashtag_start = full_text.find('\n\n')
        if hashtag_start == -1:
            return facets
            
        byte_offset = len(full_text[:hashtag_start + 2].encode('utf-8'))
        
        for tag in hashtags:
            word = f"#{tag}"
            word_bytes = word.encode('utf-8')
            word_length = len(word_bytes)
            end_byte_offset = byte_offset + word_length
            
            facets.append({
                "index": {"byteStart": byte_offset, "byteEnd": end_byte_offset},
                "features": [{
                    "$type": "app.bsky.richtext.facet#tag",
                    "tag": tag
                }]
            })
            
            byte_offset += word_length + 1  # +1 for the space
        
        return facets


# Function for content queue generation (used during media upload)
def generate_content_captions(media_url):
    """
    Generate captions for all platforms using simplified AI approach
    Used only during media upload to pre-generate all caption data
    
    Args:
        media_url (str): URL of the media
        
    Returns:
        dict: Captions formatted for each platform
    """
    generator = CaptionGenerator()
    
    # Single AI call for kaomoji, both fun facts, and hashtags
    ai_result = generator.generate_caption_and_hashtags(media_url)
    kaomoji = ai_result['kaomoji']
    fun_fact = ai_result['fun_fact']
    fun_fact_followup = ai_result['fun_fact_followup']
    hashtags = ai_result['hashtags']
    
    # Create Instagram caption with engagement hook (bold CTA)
    hashtags_text = ' '.join([f"#{tag}" for tag in hashtags]) if hashtags else ""
    cta_text = "Comment FUN FACT to receive another didactic fun fact in your DMs!"
    bold_cta = generator.to_bold_unicode(cta_text)
    #placeholder until API messaging facebook access is approved
    bold_cta = ""
    instagram_caption = f"{kaomoji}\n\n{fun_fact}\n\n{bold_cta}"
    if hashtags_text:
        instagram_caption += f"\n\n{hashtags_text}"
    
    # Same hashtags across all platforms
    return {
        'base_caption': kaomoji,
        'fun_fact': fun_fact,
        'fun_fact_followup': fun_fact_followup,
        'instagram': instagram_caption,
        'tiktok': generator.format_caption_for_platform(kaomoji, fun_fact, hashtags, 'tiktok'),
        'tumblr': generator.format_caption_for_platform(kaomoji, fun_fact, hashtags, 'tumblr'),
        'bluesky': generator.format_caption_for_platform(kaomoji, fun_fact, hashtags, 'bluesky'),
        'hashtags': {
            'instagram': hashtags,
            'tiktok': hashtags,
            'tumblr': hashtags,
            'bluesky': hashtags
        }
    }
