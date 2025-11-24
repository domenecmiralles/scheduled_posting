# 🚀 One-Click Deploy Instagram Webhook Server

## Easiest Option: Deploy via Railway Dashboard

### Step 1: Deploy with One Click
1. **Go to Railway**: https://railway.app/
2. **Sign up/Login** with your GitHub account
3. **Click "Deploy from GitHub repo"**
4. **Select this repository**: `domenecmiralles/scheduled_posting`
5. **Railway will automatically detect** your Python app and deploy it

### Step 2: Configure Environment Variables
After deployment, in Railway dashboard:

1. **Go to your deployed service**
2. **Click "Variables" tab**
3. **Add these environment variables**:

```
INSTAGRAM_ACCESS_TOKEN=EAAHrGvIG1mIBQPS6pDdIPf0wZB83jsCQ9lPZBOQtZCkvMr9ZAKncWH0dhL6BxoKvi359ReStvAXkz9BFEv7KzbQ7dBrCS5ZC37ZCt83p3DCi01akohdAfP1nScu3XyL2SxZCRmu94Vk1j6IMeK2wHdapPZBwETPU1ZA54ApCiw6ZBvNxlv8YswxDFpxrTfAj8hqiR0

INSTAGRAM_PAGE_ID=912765741916333

WEBHOOK_VERIFY_TOKEN=instagram_webhook_secret_2024
```

### Step 3: Get Your Webhook URL
1. **In Railway dashboard**, copy your app URL (something like `https://your-app-name.railway.app`)
2. **Your webhook endpoint** will be: `https://your-app-name.railway.app/webhook`

### Step 4: Configure Instagram Webhook
1. **Go to Facebook Developers Console**: https://developers.facebook.com/
2. **Select your app** → **Products** → **Webhooks**
3. **Add Subscription**:
   - **Callback URL**: `https://your-app-name.railway.app/webhook`
   - **Verify Token**: `instagram_webhook_secret_2024`
   - **Subscription Fields**: Check `comments`
4. **Click "Verify and Save"**

### Step 5: Test Your Deployment
1. **Visit health check**: `https://your-app-name.railway.app/health`
2. **Should return**: `{"status": "healthy", "service": "Instagram Webhook Server"}`
3. **Comment "FUN FACT"** on one of your Instagram posts
4. **Check if you receive a DM** with educational content!

## Alternative: Manual Terminal Commands

If you prefer terminal commands, run these **in your terminal** (not in this chat):

```bash
# Login to Railway (opens browser)
railway login

# Initialize and deploy
railway init
railway up

# Add environment variables
railway variables set INSTAGRAM_ACCESS_TOKEN=EAAHrGvIG1mIBQPS6pDdIPf0wZB83jsCQ9lPZBOQtZCkvMr9ZAKncWH0dhL6BxoKvi359ReStvAXkz9BFEv7KzbQ7dBrCS5ZC37ZCt83p3DCi01akohdAfP1nScu3XyL2SxZCRmu94Vk1j6IMeK2wHdapPZBwETPU1ZA54ApCiw6ZBvNxlv8YswxDFpxrTfAj8hqiR0

railway variables set INSTAGRAM_PAGE_ID=912765741916333

railway variables set WEBHOOK_VERIFY_TOKEN=instagram_webhook_secret_2024
```

## 🎯 What Happens Next

Once deployed and configured:

1. **Your Instagram posts** will have the engagement hook: "Comment FUN FACT to receive another didactic fun fact in your DMs!"
2. **When users comment "FUN FACT"**, Instagram sends a webhook to your deployed server
3. **Your server automatically sends a DM** with the stored educational fun fact
4. **Users get instant educational content**, boosting engagement and followers!

## 🔧 Troubleshooting

- **Health check fails**: Check Railway logs for errors
- **Webhook verification fails**: Ensure verify token matches exactly
- **DMs not sending**: Verify your Instagram token has `pages_messaging` permission
- **No webhook events**: Check Facebook webhook subscription is active

## 🎉 Success!

Your Instagram engagement automation is now live and will automatically:
- ✅ Detect "FUN FACT" comments
- ✅ Send educational DMs instantly  
- ✅ Track all interactions
- ✅ Boost engagement and followers

Ready to grow your Instagram following with automated educational content! 🚀
