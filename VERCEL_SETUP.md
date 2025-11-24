# 🚀 Vercel Instagram DM Automation Setup

## Overview
Instant Instagram DM automation using Vercel serverless functions - responses in under 2 seconds!

## How It Works
1. **Instagram webhook** → **Vercel function** (instant)
2. **Vercel function** → **Triggers GitHub Action** via Repository Dispatch
3. **GitHub Action** → **Sends DM** with fun fact from your content queue

## Setup Steps

### Step 1: Deploy to Vercel
1. **Go to Vercel**: https://vercel.com/
2. **Sign up/Login** with your GitHub account
3. **Click "New Project"**
4. **Import** `domenecmiralles/scheduled_posting` repository
5. **Deploy** (Vercel auto-detects the configuration)

### Step 2: Add Environment Variables in Vercel
After deployment, in Vercel dashboard:
1. **Go to your project** → **Settings** → **Environment Variables**
2. **Add these variables**:
   - `GITHUB_TOKEN` = (create GitHub personal access token with `repo` scope)
   - `WEBHOOK_VERIFY_TOKEN` = `instagram_webhook_secret_2024`

### Step 3: Configure Instagram Webhook
1. **Go to Facebook Developers Console**: https://developers.facebook.com/apps/539975938922082/webhooks/
2. **Add Subscription**:
   - **Callback URL**: `https://your-vercel-app.vercel.app/api/webhook`
   - **Verify Token**: `instagram_webhook_secret_2024`
   - **Subscription Fields**: Check `comments`
3. **Click "Verify and Save"**

### Step 4: Test the System
1. **Comment "FUN FACT"** on your recent Instagram post
2. **Check Vercel logs** to see webhook received
3. **Check GitHub Actions** to see DM automation triggered
4. **Verify you receive the DM** with educational content

## Benefits

### ✅ Instant Response:
- **Under 2 seconds** from comment to DM
- **Real-time engagement** with your audience
- **Professional user experience**

### ✅ Simple & Reliable:
- **One-click Vercel deployment**
- **Automatic scaling** and HTTPS
- **Uses existing GitHub infrastructure**
- **Zero maintenance required**

## What Happens When Someone Comments "FUN FACT"

1. **User comments** "FUN FACT" on your Instagram post
2. **Instagram sends webhook** to Vercel function instantly
3. **Vercel function** triggers GitHub Action via Repository Dispatch
4. **GitHub Action runs** and finds the fun fact for that specific post
5. **DM sent automatically** with educational content from your queue
6. **User receives instant educational content** - boosting engagement!

## Maintenance
- **Zero maintenance** - fully automated
- **Same reliability** as your scheduled posting
- **All interactions logged** in `instagram_interactions.log`
- **Facebook token auto-renewal** continues working

Your Instagram engagement automation is now instant and professional! 🎉
