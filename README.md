# Scheduled Social Media Posting System

A clean, modular system for automated posting to Instagram, TikTok, Tumblr, and Bluesky using official APIs and GitHub Actions.

## 🎯 Features

- **4 Platform Support**: Instagram (Graph API), TikTok (Content Posting API), Tumblr, Bluesky
- **GitHub Actions Scheduling**: Monday-Friday 9 AM, Saturday-Sunday 4 PM (UK time)
- **Drag & Drop Upload**: Simply add files to `media/` folder via GitHub web interface
- **Automatic Processing**: GitHub → S3 → Delete workflow keeps repo clean
- **AI Captions**: Customizable LLM-generated captions and hashtags
- **Queue Management**: Smart content queue with random selection
- **Official APIs Only**: No risk of account bans

## 📁 Project Structure

```
scheduled_posts/
├── main.py                    # Main orchestrator (entry point)
├── config.py                  # All configuration settings
├── caption_generator.py       # AI captions & hashtags (customizable)
├── platform_publishers.py    # Social media posting logic
├── content_queue.py          # Queue management system
├── media_processor.py        # GitHub→S3→Delete handler
├── requirements.txt          # Python dependencies
├── content_queue.json        # Content posting queue
├── media_links.json          # Permanent S3 URL tracking
├── media/                    # Drop files here (auto-processed)
│   └── .gitkeep
└── .github/workflows/
    ├── process-media.yml     # Triggered on file upload
    └── scheduled-posting.yml # Scheduled posting times
```

## 🚀 Quick Start

### 1. Set Up API Credentials

Add these secrets to your GitHub repository (Settings → Secrets and variables → Actions):

**Required Secrets:**
- `AWS_ACCESS_KEY_ID` - Your AWS access key (used for S3 and Bedrock)
- `AWS_SECRET_ACCESS_KEY` - Your AWS secret key (used for S3 and Bedrock)
- `INSTAGRAM_ACCESS_TOKEN` - Instagram Graph API token
- `INSTAGRAM_PAGE_ID` - Instagram business account page ID
- `TIKTOK_ACCESS_TOKEN` - TikTok Content Posting API token

**Note:** AI captions are generated using AWS Bedrock Nova, which uses your existing AWS credentials - no additional API keys needed!

### 2. Upload Content

1. Go to your GitHub repository
2. Navigate to `scheduled_posts/media/`
3. Click "Add file" → "Upload files"
4. Drag and drop your images/videos
5. Commit the files

**Supported Formats:**
- **Images**: PNG, JPG, JPEG, GIF
- **Videos**: MP4, MOV, AVI

### 3. Automatic Processing

When you upload files:
1. **GitHub Actions** detects new files
2. **Processes** images (resize to 1080x1080) and videos
3. **Uploads** to S3 with public URLs
4. **Adds** to posting queue
5. **Deletes** original files from repo
6. **Updates** tracking files

### 4. Scheduled Posting

Content posts automatically:
- **Monday-Friday**: 9 AM UK time
- **Saturday-Sunday**: 4 PM UK time

Each post:
1. Selects random content from queue
2. Generates AI captions and hashtags
3. Posts to all platforms simultaneously
4. Marks content as posted
5. Updates queue status

## 🎨 Customizing Captions

Edit `caption_generator.py` to customize:

```python
# Change the AI model
self.model = "meta-llama/Llama-Vision-Free"

# Modify the prompt
prompt = "Your custom prompt here"

# Add new LLM provider
# Replace Together client with your preferred provider
```

## 📊 Platform-Specific Features

### Instagram
- **Images**: Posted as regular posts
- **Videos**: Posted as Reels
- **Hashtags**: 10 random hashtags
- **Rate Limit**: 200 requests/hour

### TikTok
- **Videos Only**: Images are skipped
- **Hashtags**: 5 random hashtags
- **Caption Limit**: 150 characters (auto-truncated)
- **Privacy**: Public by default

### Tumblr
- **Images & Videos**: Both supported
- **Hashtags**: 3 random hashtags as tags
- **Caption**: AI-generated text

### Bluesky
- **Images & Videos**: Both supported
- **Hashtags**: 3 random hashtags with facets
- **Caption**: AI-generated with proper hashtag linking

## 🔧 Manual Operations

### Check Queue Status
```bash
cd scheduled_posts
python main.py status
```

### Manual Posting
```bash
cd scheduled_posts
python main.py post
```

### Process Media Locally
```bash
cd scheduled_posts
python media_processor.py
```

## 📈 Monitoring

### GitHub Actions
- Go to "Actions" tab in your repository
- Monitor workflow runs and logs
- Check for any failures or errors

### Queue Status
- Check `content_queue.json` for pending items
- Check `media_links.json` for all uploaded content
- View GitHub Actions logs for posting results

## 🛠️ Troubleshooting

### Common Issues

**1. API Credentials Not Working**
- Verify all secrets are set in GitHub repository settings
- Check API token expiration dates
- Ensure Instagram account is Business type with connected Facebook page

**2. Files Not Processing**
- Check file formats are supported
- Ensure files are uploaded to `scheduled_posts/media/` folder
- Check GitHub Actions logs for processing errors

**3. Posting Failures**
- Check platform-specific rate limits
- Verify content meets platform requirements (video length, file size)
- Check API status pages for service outages

**4. Schedule Not Working**
- GitHub Actions may have delays during high usage
- Check cron schedule matches your timezone needs
- Use manual triggers for testing

### Getting Help

1. Check GitHub Actions logs for detailed error messages
2. Review platform API documentation for requirements
3. Test with manual triggers before relying on schedule
4. Monitor queue status regularly

## 🔒 Security

- All API keys stored as GitHub Secrets
- No credentials in code or repository
- S3 URLs are public but obscured
- Temporary files cleaned up automatically

## 📝 Maintenance

### Regular Tasks
- Monitor API rate limits and usage
- Clean up old queue items (automatic after 30 days)
- Update API tokens when they expire
- Review and update hashtag lists in `config.py`

### Updates
- Update Python dependencies in `requirements.txt`
- Modify posting schedule in `scheduled-posting.yml`
- Customize caption generation in `caption_generator.py`
- Add new platforms in `platform_publishers.py`

## 🎊 Benefits

- ✅ **Official APIs**: No account suspension risk
- ✅ **Automated**: Set it and forget it
- ✅ **Clean Code**: Modular, maintainable architecture
- ✅ **Free Hosting**: GitHub Actions (2,000 minutes/month)
- ✅ **Scalable**: Easy to add new platforms
- ✅ **Customizable**: Modify any component easily
- ✅ **Reliable**: Built-in error handling and recovery

Your content will now post automatically to all 4 platforms on schedule! 🚀
