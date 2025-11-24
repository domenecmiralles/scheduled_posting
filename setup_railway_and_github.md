# 🚀 Complete Railway & GitHub Setup Guide

## Step 1: Set Railway Environment Variables

### Go to your Railway project:
https://railway.com/project/f47884c7-d0f6-407a-96fc-07948bf9515b/service/5d84c9a8-90d6-4dab-a3a5-9d1bbc127638/variables?environmentId=4cefc02a-3ee6-47a1-a4f1-bd3bd3857d86

### Add these 3 environment variables:



## Step 2: Add GitHub Secrets

### Go to your GitHub repository:
https://github.com/domenecmiralles/scheduled_posting/settings/secrets/actions


```

## Step 3: Generate Your Railway Public Domain

### You're in the right place! In the Networking section:
1. **Change the port from 8080 to 5000** (your Flask app runs on port 5000)
2. **Click "Generate Domain"** button (under Public Networking)
3. **Railway will create a public URL** like: `https://scheduled-posting-production-xxxx.up.railway.app`
4. **Copy this URL** - this is your webhook server address
5. **Your webhook endpoint** will be: `https://your-generated-domain.railway.app/webhook`

### Test your deployment:
Visit: `https://your-generated-domain.railway.app/health`
Should return: `{"status": "healthy", "service": "Instagram Webhook Server"}`

## Step 4: Configure Instagram Webhook

### Go to Facebook Developers Console:
https://developers.facebook.com/apps/539975938922082/webhooks/

### Add Webhook Subscription:
1. **Click "Add Subscription"**
2. **Callback URL**: `https://your-app-name.railway.app/webhook`
3. **Verify Token**: `instagram_webhook_secret_2024`
4. **Subscription Fields**: Check `comments`
5. **Click "Verify and Save"**

## Step 5: Test Everything

### 5.1 Test Railway Deployment
Visit: `https://your-app-name.railway.app/health`
Should return: `{"status": "healthy", "service": "Instagram Webhook Server"}`

### 5.2 Test GitHub Actions
1. **Go to**: https://github.com/domenecmiralles/scheduled_posting/actions
2. **Click "Renew Facebook Access Token"**
3. **Click "Run workflow"** → **Run workflow**
4. **Check logs** to verify it works

### 5.3 Test Instagram DM Automation
1. **Comment "FUN FACT"** on one of your Instagram posts
2. **Check if you receive a DM** with educational content
3. **Check Railway logs** for webhook activity

## 🎉 Success Indicators

✅ Railway app responds at `/health` endpoint
✅ GitHub Action runs without errors
✅ Instagram webhook verification succeeds
✅ Test comment triggers automatic DM
✅ Railway logs show webhook events

## 🚀 What Happens Next

Once everything is set up:

1. **Your Instagram posts** will have engagement hooks
2. **Users comment "FUN FACT"** → **Instant educational DM**
3. **Token renews automatically** every 2 weeks
4. **Railway environment updates** automatically
5. **System runs forever** without maintenance

Your Instagram engagement automation is ready to boost your following! 🎉
