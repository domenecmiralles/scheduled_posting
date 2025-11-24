# 🚀 Deploy Instagram Webhook Server - Simple Guide

## Step 1: Deploy to Railway (Easiest Option)

### 1.1 Install Railway CLI
```bash
npm install -g @railway/cli
```

### 1.2 Login and Deploy
```bash
# Login to Railway
railway login

# Initialize project
railway init

# Deploy your webhook server
railway up
```

### 1.3 Set Environment Variables on Railway
After deployment, add these environment variables in Railway dashboard:

```
INSTAGRAM_ACCESS_TOKEN=EAAHrGvIG1mIBQPS6pDdIPf0wZB83jsCQ9lPZBOQtZCkvMr9ZAKncWH0dhL6BxoKvi359ReStvAXkz9BFEv7KzbQ7dBrCS5ZC37ZCt83p3DCi01akohdAfP1nScu3XyL2SxZCRmu94Vk1j6IMeK2wHdapPZBwETPU1ZA54ApCiw6ZBvNxlv8YswxDFpxrTfAj8hqiR0
INSTAGRAM_PAGE_ID=912765741916333
WEBHOOK_VERIFY_TOKEN=your_secret_verify_token_123
```

## Step 2: Configure Instagram Webhook

### 2.1 Go to Facebook Developers Console
1. Visit: https://developers.facebook.com/
2. Select your app
3. Go to **Products** → **Webhooks**

### 2.2 Add Webhook
1. Click **Add Subscription**
2. **Callback URL**: `https://your-railway-app.railway.app/webhook`
3. **Verify Token**: `your_secret_verify_token_123` (same as environment variable)
4. **Subscription Fields**: Check `comments`
5. Click **Verify and Save**

## Step 3: Test Your Deployment

### 3.1 Check Health Endpoint
Visit: `https://your-railway-app.railway.app/health`
Should return: `{"status": "healthy", "service": "Instagram Webhook Server"}`

### 3.2 Test DM Automation
1. Post content with your scheduled posting system
2. Comment "FUN FACT" on your Instagram post
3. Check if you receive a DM with the fun fact followup
4. Monitor Railway logs for webhook activity

## Alternative: One-Click Deploy Options

### Option A: Render
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

1. Connect your GitHub repo
2. Set build command: `pip install -r webhook_requirements.txt`
3. Set start command: `python instagram_webhook.py`
4. Add environment variables

### Option B: Heroku
```bash
# Create Procfile
echo "web: python instagram_webhook.py" > Procfile

# Deploy to Heroku
heroku create your-webhook-app
git push heroku main
heroku config:set INSTAGRAM_ACCESS_TOKEN=your_token
heroku config:set INSTAGRAM_PAGE_ID=912765741916333
heroku config:set WEBHOOK_VERIFY_TOKEN=your_secret_token
```

## 🎯 What Happens After Deployment

1. **Users see your posts** with "Comment FUN FACT to receive another didactic fun fact in your DMs!"
2. **Users comment "FUN FACT"**
3. **Instagram sends webhook** to your deployed server
4. **Server detects comment** and looks up the stored fun_fact_followup
5. **Server sends DM** with educational content
6. **User receives instant DM** with curated fun fact
7. **Engagement and followers increase!**

## 🔧 Troubleshooting

### Common Issues:
- **Webhook not receiving events**: Check Facebook webhook configuration
- **DMs not sending**: Verify `pages_messaging` permission
- **Server not responding**: Check Railway/deployment logs

### Debug Commands:
```bash
# Check Railway logs
railway logs

# Test webhook locally first
python instagram_webhook.py
# Then use ngrok to expose: ngrok http 5000
```

## 🎉 Success Indicators

✅ Health endpoint returns 200 OK
✅ Facebook webhook verification succeeds  
✅ Test comment triggers DM
✅ Logs show webhook events
✅ Users receive educational DMs automatically

Your Instagram engagement automation is ready to boost your following! 🚀
