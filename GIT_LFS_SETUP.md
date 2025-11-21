# Git LFS Setup Guide

## What is Git LFS?
Git Large File Storage (LFS) is perfect for your use case! It:
- ✅ **Free for public repos** (1GB storage, 1GB bandwidth/month)
- ✅ **Handles large files** without bloating git history
- ✅ **Automatic cleanup** - files are stored separately
- ✅ **Perfect for videos** that get deleted after processing

## Installation

### macOS (using Homebrew)
```bash
brew install git-lfs
```

### Alternative Installation
If brew is slow, download directly from: https://git-lfs.github.io/

## Setup Steps

### 1. Install Git LFS in your repository
```bash
git lfs install
```

### 2. Track video files (already configured in .gitattributes)
```bash
git lfs track "media/*.mp4"
git lfs track "media/*.mov" 
git lfs track "media/*.avi"
git lfs track "media/*.webm"
```

### 3. Add and commit the .gitattributes file
```bash
git add .gitattributes
git commit -m "🎬 Add Git LFS tracking for video files"
git push
```

## How It Works

### For Your Workflow:
1. **Upload videos** → Git LFS stores them efficiently
2. **GitHub Actions processes** → Downloads files as needed
3. **Files get deleted** → LFS handles cleanup automatically
4. **No repository bloat** → History stays clean

### Storage Limits:
- **Free tier**: 1GB storage + 1GB bandwidth/month
- **Perfect for ~20 videos** since they get deleted after processing
- **Bandwidth resets monthly**

## Benefits for Your Use Case

✅ **No more HTTP 400 errors** - Large files handled properly  
✅ **Fast git operations** - Repository stays lightweight  
✅ **Automatic cleanup** - Deleted files don't bloat history  
✅ **GitHub Actions compatible** - Works seamlessly with workflows  
✅ **Cost effective** - Free for your usage pattern  

## Testing
After setup, upload a test video to `media/` folder and check:
```bash
git lfs ls-files  # Shows LFS-tracked files
```

Your automated posting system will work perfectly with Git LFS! 🚀
