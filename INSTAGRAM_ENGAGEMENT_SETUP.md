# Instagram Engagement Automation Setup Guide

## Overview
This system automatically detects "FUN FACT" comments on your Instagram posts and sends personalized DMs with additional fun facts.

## What's Been Implemented

### ✅ Phase 1: Core Infrastructure (COMPLETED)
- **Enhanced Caption Generation**: AI now generates two fun facts per post
- **New Instagram Caption Format**: 
  ```
  {kaomoji}
  
  {fun_fact}
  
  Comment FUN FACT to receive another didactic fun fact in your DMs!
  
  {hashtags}
  ```
- **Complete Queue Migration**: All existing 11 queue items now have complete caption data
- **Webhook Server**: Flask server ready to handle Instagram comment notifications
- **DM Automation**: System can send fun_fact_followup via DMs

### ✅ Phase 2: Performance Optimization (COMPLETED)
- **Zero VLM Calls During Posting**: All AI processing moved to upload time
- **Pre-generated Captions**: Complete platform-specific captions stored in queue
- **Faster Posting**: No AI delays during scheduled posts
- **Deterministic Workflow**: Posting is now pure data retrieval

### 📋 Current Queue Status
- **Total Items**: 11 videos
- **With Fun Facts**: 11/11 (100%)
- **Posted**: 2 items
- **Pending**: 9 items ready with engagement hooks

## Next Steps for Full Deployment

### 1. Instagram App Configuration
You need to configure your Instagram/Facebook app:

1. **Go to Facebook Developers Console**
2. **Add Webhook URL**: `https://your-domain.com/webhook`
3. **Set Verify Token**: Add `WEBHOOK_VERIFY_TOKEN` to your `.env`
4. **Subscribe to Events**: Enable `comments` field
5. **Request Permissions**: 
   - `instagram_basic`
   - `instagram_content_publish`
   - `pages_messaging`
   - `pages_read_engagement`

### 2. Deploy Webhook Server
Options for deployment:

#### Option A: Railway (Recommended)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up
```

#### Option B: Render
1. Connect your GitHub repo
2. Set build command: `pip install -r webhook_requirements.txt`
3. Set start command: `python instagram_webhook.py`

#### Option C: Heroku
```bash
# Create Procfile
echo "web: python instagram_webhook.py" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

### 3. Environment Variables
Add to your deployment platform:
```
INSTAGRAM_ACCESS_TOKEN=your_token
INSTAGRAM_PAGE_ID=your_page_id
WEBHOOK_VERIFY_TOKEN=your_verify_token
```

### 4. Test the System

#### Test Caption Generation
```bash
python -c "
from caption_generator import generate_content_captions
result = generate_content_captions('https://majindonpatch-public.s3.amazonaws.com/posts_insta/room_watertable_processed.mp4')
print('Instagram Caption:')
print(result['instagram'])
print('\nFun Fact Followup:')
print(result['fun_fact_followup'])
"
```

#### Test Webhook Server Locally
```bash
pip install -r webhook_requirements.txt
python instagram_webhook.py
```

Visit `http://localhost:5000/health` to verify it's running.

## How It Works

### 1. Posting Flow
1. **GitHub Actions** runs on schedule
2. **Selects random unposted content** from queue
3. **Generates captions** with engagement hook
4. **Posts to Instagram** with "Comment FUN FACT..." message
5. **Stores fun_fact_followup** for later DM use

### 2. Engagement Flow
1. **User comments "FUN FACT"** on your post
2. **Instagram webhook** notifies your server
3. **Server looks up** the fun_fact_followup for that post
4. **Sends DM** with the additional fun fact
5. **Logs interaction** for tracking

### 3. Data Structure
Each queue item now contains:
```json
{
  "id": 1,
  "filename": "video.mp4",
  "url": "https://s3-url...",
  "fun_fact": "First fact for public caption",
  "fun_fact_followup": "Second fact for DMs",
  "engagement_hook_used": true,
  "posting_results": {
    "instagram": {"id": "media_id"}
  }
}
```

## Files Created/Modified

### New Files
- `instagram_webhook.py` - Webhook server for comment handling
- `migrate_queue_fun_facts.py` - Migration script (one-time use)
- `webhook_requirements.txt` - Dependencies for webhook server
- `INSTAGRAM_ENGAGEMENT_SETUP.md` - This guide

### Modified Files
- `caption_generator.py` - Now generates two fun facts + engagement hook
- `content_queue.py` - Generates fun facts when adding new content
- `main.py` - Fallback logic for missing fun facts

## Monitoring & Analytics

### Interaction Logs
The system logs all DM interactions to `instagram_interactions.log`:
```json
{
  "timestamp": "2025-11-24T17:23:00",
  "user_id": "instagram_user_id",
  "media_id": "instagram_media_id", 
  "fun_fact_sent": "The fun fact that was sent...",
  "action": "fun_fact_dm_sent"
}
```

### Health Check
Monitor your webhook server: `GET /health`

## Troubleshooting

### Common Issues
1. **Webhook not receiving events**: Check Instagram app webhook configuration
2. **DMs not sending**: Verify `pages_messaging` permission
3. **Fun facts not found**: Check that posting_results contain Instagram media ID

### Debug Commands
```bash
# Check queue status
python main.py status

# Test webhook locally with ngrok
ngrok http 5000

# View interaction logs
tail -f instagram_interactions.log
```

## Future Enhancements
- Multi-stage DM funnels ("Reply MORE for another fact")
- Auto-replies to non-keyword comments
- Analytics dashboard
- Adaptive posting time optimization

## Security Notes
- Keep your access tokens secure
- Use HTTPS for webhook endpoints
- Validate webhook signatures (recommended for production)
- Rate limit DM sending to avoid Instagram limits
