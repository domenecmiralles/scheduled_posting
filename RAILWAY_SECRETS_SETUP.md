# 🔐 Railway Automatic Token Updates Setup

## Overview
This guide helps you set up automatic Railway environment variable updates when your Facebook token renews every 2 weeks.

## Step 1: Get Railway API Token

### 1.1 Generate Railway Token
1. **Go to Railway Dashboard**: https://railway.app/account/tokens
2. **Click "Create Token"**
3. **Name**: `GitHub Actions Token`
4. **Copy the token** (starts with `railway_`)

### 1.2 Get Railway Project Details
1. **Go to your deployed webhook project** in Railway
2. **In the URL**, note your project ID: `https://railway.app/project/[PROJECT_ID]`
3. **Click on your service** → **Settings** → **Environment**
4. **Note the Environment ID** from the URL: `https://railway.app/project/[PROJECT_ID]/service/[SERVICE_ID]?environmentId=[ENVIRONMENT_ID]`

## Step 2: Add GitHub Secrets

### 2.1 Go to GitHub Repository Settings
1. **Your repo**: https://github.com/domenecmiralles/scheduled_posting
2. **Settings** → **Secrets and variables** → **Actions**
3. **Click "New repository secret"**

### 2.2 Add These Secrets
Add each of these as separate secrets:

```
FACEBOOK_CLIENT_ID
Value: 539975938922082

FACEBOOK_CLIENT_SECRET
Value: 0146b058464a869b40d4607e4932f330

RAILWAY_TOKEN
Value: railway_your_token_here

RAILWAY_PROJECT_ID  
Value: your_project_id_here

RAILWAY_ENVIRONMENT_ID
Value: your_environment_id_here
```

## Step 3: How It Works

### Automatic Updates Every 2 Weeks:
1. **GitHub Action runs** (1st and 15th of each month)
2. **Renews Facebook token** using current token
3. **Updates GitHub secrets** with new token
4. **Updates Railway environment variables** with new token
5. **Your webhook server restarts** with new token automatically
6. **No manual intervention needed!**

## Step 4: Verify Setup

### 4.1 Test Manual Trigger
1. **Go to GitHub Actions**: https://github.com/domenecmiralles/scheduled_posting/actions
2. **Click "Renew Facebook Access Token"**
3. **Click "Run workflow"** → **Run workflow**
4. **Check logs** to verify both GitHub and Railway updates

### 4.2 Check Railway Environment
1. **Go to Railway project** → **Variables**
2. **Verify `INSTAGRAM_ACCESS_TOKEN`** is updated
3. **Check deployment logs** for restart confirmation

## 🎯 Benefits

### ✅ Complete Automation:
- **No manual token management** ever again
- **Railway environment stays in sync** with GitHub secrets
- **Webhook server automatically restarts** with new token
- **Full audit trail** in GitHub Actions logs

### ✅ Reliability:
- **Runs every 2 weeks** (well before 60-day expiration)
- **Multiple fallbacks** if one update fails
- **Logs all operations** for troubleshooting

## 🔧 Troubleshooting

### Common Issues:
- **Railway API fails**: Check `RAILWAY_TOKEN` is valid
- **Project not found**: Verify `RAILWAY_PROJECT_ID` is correct
- **Environment not found**: Check `RAILWAY_ENVIRONMENT_ID` matches

### Debug Steps:
1. **Check GitHub Actions logs** for specific error messages
2. **Verify Railway token permissions** in Railway dashboard
3. **Test Railway API manually** with curl command
4. **Check Railway deployment logs** for restart confirmation

## 🎉 Success Indicators

✅ GitHub Action completes without errors
✅ Railway environment variable updated
✅ Webhook server restarts automatically  
✅ Health endpoint still responds: `/health`
✅ DM automation continues working seamlessly

Your Instagram engagement automation now has **100% automated token management** across all platforms! 🚀
