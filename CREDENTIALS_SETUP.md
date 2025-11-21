# 🔐 Complete API Credentials Setup Guide

This guide will walk you through setting up all API credentials needed for automatic posting to Instagram, TikTok, Tumblr, Bluesky, and AWS services.

## 📋 Overview

Your system needs credentials for:
- **Instagram Graph API** (Most complex - requires long-lived tokens)
- **TikTok Content Posting API**
- **Tumblr API**
- **Bluesky AT Protocol**
- **AWS** (S3 storage + Bedrock AI)

## 🚨 Important Security Note

**NEVER** hardcode credentials in your code files. Always use:
- **GitHub Secrets** for production (recommended)
- **Environment variables** for local development
- **`.env` files** for local testing (add to `.gitignore`)

---

## 1. 📸 Instagram Graph API Setup (Long-Lived Tokens)

### Prerequisites
- Facebook Developer Account
- Instagram Business Account (not personal)
- Facebook Page connected to Instagram account

### Step 1: Create Facebook App

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Click **"My Apps"** → **"Create App"**
3. Choose **"Business"** app type
4. Fill in app details:
   - **App Name**: "Your App Name"
   - **Contact Email**: Your email
   - **Business Account**: Select or create one

### Step 2: Configure App Permissions

1. In your app dashboard, go to **"App Review"** → **"Permissions and Features"**
2. Request these permissions:
   - `instagram_basic`
   - `instagram_content_publish`
   - `pages_show_list`
   - `pages_read_engagement`

### Step 3: Get App Credentials

1. Go to **"Settings"** → **"Basic"**
2. Copy your:
   - **App ID**
   - **App Secret** (click "Show")

### Step 4: Generate Long-Lived Access Token

#### Option A: Using Facebook Graph API Explorer (Recommended)

1. Go to [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
2. Select your app from dropdown
3. Click **"Generate Access Token"**
4. Select required permissions:
   - `instagram_basic`
   - `instagram_content_publish` 
   - `pages_show_list`
   - `pages_read_engagement`
5. Copy the **short-lived token**

#### Option B: Manual URL Method

Visit this URL (replace values):
```
https://www.facebook.com/v18.0/dialog/oauth?
  client_id={YOUR_APP_ID}&
  redirect_uri=https://localhost&
  scope=instagram_basic,instagram_content_publish,pages_show_list,pages_read_engagement&
  response_type=token
```

### Step 5: Exchange for Long-Lived Token

Use this API call (replace `{values}`):

```bash
curl -X GET "https://graph.facebook.com/v18.0/oauth/access_token?grant_type=fb_exchange_token&client_id={YOUR_APP_ID}&client_secret={YOUR_APP_SECRET}&fb_exchange_token={SHORT_LIVED_TOKEN}"
```

**Response will contain your 60-day long-lived user token.**

### Step 6: Get Page Access Token

```bash
curl -X GET "https://graph.facebook.com/v18.0/me/accounts?access_token={LONG_LIVED_USER_TOKEN}"
```

Find your Facebook page in the response and copy its `access_token`.

### Step 7: Get Instagram Business Account ID

```bash
curl -X GET "https://graph.facebook.com/v18.0/{PAGE_ID}?fields=instagram_business_account&access_token={PAGE_ACCESS_TOKEN}"
```

Copy the `instagram_business_account.id` - this is your **Instagram Page ID**.

### Step 8: Test Your Setup

```bash
curl -X GET "https://graph.facebook.com/v18.0/{912765741916333}?fields=id,username&access_token={EAAHrGvIG1mIBQEhsdgwWga7V7snvyDxNhkYAE5ruNaouYKuxzBOumbnHDqcRvcIWZAgQw1Ip7vDSnSDXVRjzJNXlWhXRP9JKITCSEsQtZAAhucoynZBW4XTZBZAtZCjNzxsUQtge0VymTBBRCF7PM1KLy58SX9UKoHDM1tOl2EZBXgYGOosSPHr1LD3alFI}"
```

Should return your Instagram account details.

### 📝 Instagram Credentials Summary

You now have:
- `INSTAGRAM_ACCESS_TOKEN` = Page Access Token (from Step 6)
- `INSTAGRAM_PAGE_ID` = Instagram Business Account ID (from Step 7)

---

## 2. 🎵 TikTok Content Posting API Setup

### Step 1: Apply for TikTok Developer Account

1. Go to [TikTok Developers](https://developers.tiktok.com/)
2. Sign up with your TikTok account
3. Complete business verification (may take 1-3 days)

### Step 2: Create App

1. Go to **"My Apps"** → **"Create an app"**
2. Fill in app details:
   - **App Name**: Your app name
   - **Category**: Content & Publishing
   - **Description**: Automated content posting

### Step 3: Add Content Posting API

1. In your app dashboard, click **"Add products"**
2. Select **"Content Posting API"**
3. Configure scopes:
   - `video.upload`
   - `video.publish`

### Step 4: Get Access Token

1. Go to **"Authorization"** tab
2. Generate access token with required scopes
3. Copy the **Access Token**

### 📝 TikTok Credentials Summary

You now have:
- `TIKTOK_ACCESS_TOKEN` = Your access token

---

## 3. 📝 Tumblr API Setup

### Step 1: Register Tumblr App

1. Go to [Tumblr API](https://www.tumblr.com/oauth/apps)
2. Click **"Register application"**
3. Fill in details:
   - **Application Name**: Your app name
   - **Application Website**: Your website/GitHub repo
   - **Application Description**: Automated posting
   - **Default callback URL**: `http://localhost`

### Step 2: Get App Credentials

After registration, copy:
- **OAuth Consumer Key**
- **OAuth Consumer Secret**

### Step 3: Get User Tokens

1. Use a tool like [Tumblr API Console](https://api.tumblr.com/console) or Postman
2. Authorize your app to get:
   - **OAuth Token**
   - **OAuth Token Secret**

### Step 4: Get Blog Name

Your blog name is your Tumblr username (e.g., if your blog is `myblog.tumblr.com`, use `myblog`)

### 📝 Tumblr Credentials Summary

You now have:
- `TUMBLR_CONSUMER_KEY` = OAuth Consumer Key
- `TUMBLR_CONSUMER_SECRET` = OAuth Consumer Secret  
- `TUMBLR_OAUTH_TOKEN` = OAuth Token
- `TUMBLR_OAUTH_TOKEN_SECRET` = OAuth Token Secret
- `TUMBLR_BLOG_NAME` = Your blog name

---

## 4. 🦋 Bluesky Setup

### Step 1: Create App Password

1. Log into [Bluesky](https://bsky.app/)
2. Go to **Settings** → **Privacy and Security**
3. Scroll to **App Passwords**
4. Click **"Add App Password"**
5. Name it (e.g., "Auto Posting Bot")
6. Copy the generated password

### 📝 Bluesky Credentials Summary

You now have:
- `BLUESKY_USERNAME` = Your Bluesky handle (e.g., `username.bsky.social`)
- `BLUESKY_PASSWORD` = App password (NOT your regular password)

---

## 5. ☁️ AWS Setup (S3 + Bedrock)

### Step 1: Create AWS Account

1. Go to [AWS Console](https://aws.amazon.com/)
2. Create account if you don't have one
3. Complete billing setup

### Step 2: Create IAM User

1. Go to **IAM** → **Users** → **Create user**
2. Username: `scheduled-posting-bot`
3. Select **"Attach policies directly"**
4. Add these policies:
   - `AmazonS3FullAccess`
   - `AmazonBedrockFullAccess`

### Step 3: Create Access Keys

1. Click on your new user
2. Go to **"Security credentials"** tab
3. Click **"Create access key"**
4. Choose **"Application running outside AWS"**
5. Copy:
   - **Access Key ID**
   - **Secret Access Key**

### Step 4: Create S3 Bucket

1. Go to **S3** → **Create bucket**
2. Bucket name: `your-unique-bucket-name`
3. Region: Choose closest to you
4. **Uncheck** "Block all public access" (needed for public URLs)
5. Create bucket

### Step 5: Configure Bucket for Public Access

1. Go to your bucket → **Permissions**
2. Edit **Bucket Policy** and add:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::YOUR-BUCKET-NAME/*"
        }
    ]
}
```

### 📝 AWS Credentials Summary

You now have:
- `AWS_ACCESS_KEY_ID` = Your access key ID
- `AWS_SECRET_ACCESS_KEY` = Your secret access key
- `S3_BUCKET` = Your bucket name

---

## 6. 🔧 Setting Up GitHub Secrets

### Step 1: Go to Repository Settings

1. Go to your GitHub repository
2. Click **"Settings"** tab
3. Go to **"Secrets and variables"** → **"Actions"**

### Step 2: Add All Secrets

Click **"New repository secret"** for each:

**Instagram:**
- Name: `INSTAGRAM_ACCESS_TOKEN`, Value: Your page access token
- Name: `INSTAGRAM_PAGE_ID`, Value: Your Instagram business account ID

**TikTok:**
- Name: `TIKTOK_ACCESS_TOKEN`, Value: Your TikTok access token

**Tumblr:**
- Name: `TUMBLR_CONSUMER_KEY`, Value: Your consumer key
- Name: `TUMBLR_CONSUMER_SECRET`, Value: Your consumer secret
- Name: `TUMBLR_OAUTH_TOKEN`, Value: Your OAuth token
- Name: `TUMBLR_OAUTH_TOKEN_SECRET`, Value: Your OAuth token secret
- Name: `TUMBLR_BLOG_NAME`, Value: Your blog name

**Bluesky:**
- Name: `BLUESKY_USERNAME`, Value: Your Bluesky handle
- Name: `BLUESKY_PASSWORD`, Value: Your app password

**AWS:**
- Name: `AWS_ACCESS_KEY_ID`, Value: Your AWS access key ID
- Name: `AWS_SECRET_ACCESS_KEY`, Value: Your AWS secret access key
- Name: `S3_BUCKET`, Value: Your S3 bucket name

---

## 7. 🛠️ Update Your Code Configuration

### Step 1: Fix config.py

Your `config.py` should use environment variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()

# AWS S3 Configuration
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
S3_BUCKET = os.getenv('S3_BUCKET', 'your-default-bucket')
S3_PATH = 'posts_insta'
S3_URL_BASE = f'https://{S3_BUCKET}.s3.amazonaws.com/{S3_PATH}/'

# Social Media API Configuration
INSTAGRAM_ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN')
INSTAGRAM_PAGE_ID = os.getenv('INSTAGRAM_PAGE_ID')
TIKTOK_ACCESS_TOKEN = os.getenv('TIKTOK_ACCESS_TOKEN')

# Tumblr API Configuration
TUMBLR_CONSUMER_KEY = os.getenv('TUMBLR_CONSUMER_KEY')
TUMBLR_CONSUMER_SECRET = os.getenv('TUMBLR_CONSUMER_SECRET')
TUMBLR_OAUTH_TOKEN = os.getenv('TUMBLR_OAUTH_TOKEN')
TUMBLR_OAUTH_TOKEN_SECRET = os.getenv('TUMBLR_OAUTH_TOKEN_SECRET')
TUMBLR_BLOG_NAME = os.getenv('TUMBLR_BLOG_NAME')

# Bluesky Configuration
BLUESKY_USERNAME = os.getenv('BLUESKY_USERNAME')
BLUESKY_PASSWORD = os.getenv('BLUESKY_PASSWORD')
```

### Step 2: Create .env for Local Testing

Create `.env` file (add to `.gitignore`):

```env
# Instagram
INSTAGRAM_ACCESS_TOKEN=your_instagram_token_here
INSTAGRAM_PAGE_ID=your_instagram_page_id_here

# TikTok
TIKTOK_ACCESS_TOKEN=your_tiktok_token_here

# Tumblr
TUMBLR_CONSUMER_KEY=your_tumblr_consumer_key_here
TUMBLR_CONSUMER_SECRET=your_tumblr_consumer_secret_here
TUMBLR_OAUTH_TOKEN=your_tumblr_oauth_token_here
TUMBLR_OAUTH_TOKEN_SECRET=your_tumblr_oauth_token_secret_here
TUMBLR_BLOG_NAME=your_blog_name_here

# Bluesky
BLUESKY_USERNAME=your_username.bsky.social
BLUESKY_PASSWORD=your_app_password_here

# AWS
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
S3_BUCKET=your_bucket_name_here
```

---

## 8. 🧪 Testing Your Setup

### Step 1: Test Locally

```bash
cd scheduled_posts
python main.py status
```

### Step 2: Test Each Platform

```bash
# Test Instagram
python -c "from platform_publishers import InstagramPublisher; print('Instagram OK' if InstagramPublisher().access_token else 'Instagram FAIL')"

# Test TikTok  
python -c "from platform_publishers import TikTokPublisher; print('TikTok OK' if TikTokPublisher().access_token else 'TikTok FAIL')"

# Test Tumblr
python -c "from platform_publishers import TumblrPublisher; print('Tumblr OK')"

# Test Bluesky
python -c "from platform_publishers import BlueskyPublisher; print('Bluesky OK' if BlueskyPublisher().client else 'Bluesky FAIL')"
```

### Step 3: Test GitHub Actions

1. Push your changes to GitHub
2. Go to **"Actions"** tab
3. Manually trigger a workflow to test

---

## 🔄 Token Refresh & Maintenance

### Instagram Token Refresh

Instagram tokens expire every 60 days. Set a calendar reminder to refresh:

```bash
# Exchange current long-lived token for new one
curl -X GET "https://graph.facebook.com/v18.0/oauth/access_token?grant_type=fb_exchange_token&client_id={APP_ID}&client_secret={APP_SECRET}&fb_exchange_token={CURRENT_LONG_LIVED_TOKEN}"
```

### Other Platforms

- **TikTok**: Tokens typically last 1 year
- **Tumblr**: OAuth tokens don't expire
- **Bluesky**: App passwords don't expire
- **AWS**: Access keys don't expire (but rotate regularly for security)

---

## 🚨 Troubleshooting

### Common Issues

**Instagram "Invalid Access Token"**
- Token expired (refresh every 60 days)
- Wrong permissions (need `instagram_content_publish`)
- Account not Business type

**TikTok "Forbidden"**
- App not approved for Content Posting API
- Missing required scopes
- Rate limit exceeded

**Tumblr "Unauthorized"**
- Wrong OAuth tokens
- App not authorized
- Blog name incorrect

**Bluesky "Authentication Failed"**
- Using regular password instead of app password
- Username format wrong (needs `.bsky.social`)

**AWS "Access Denied"**
- Wrong IAM permissions
- Bucket policy not set for public access
- Wrong region

### Getting Help

1. Check GitHub Actions logs for detailed errors
2. Test each platform individually
3. Verify all secrets are set correctly
4. Check platform API status pages

---

## ✅ Final Checklist

- [ ] Instagram long-lived token generated and tested
- [ ] TikTok access token obtained and tested
- [ ] Tumblr OAuth tokens configured and tested
- [ ] Bluesky app password created and tested
- [ ] AWS credentials and S3 bucket configured
- [ ] All GitHub Secrets added
- [ ] config.py updated to use environment variables
- [ ] Local .env file created (if testing locally)
- [ ] All platforms tested individually
- [ ] GitHub Actions workflow tested

Your automated posting system should now be fully configured! 🎉

---

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review platform-specific API documentation
3. Check GitHub Actions logs for detailed error messages
4. Ensure all tokens are current and have proper permissions
