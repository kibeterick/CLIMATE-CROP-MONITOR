# 📤 Push Your Project to GitHub - Student Guide

## Why GitHub?
- ✅ Backup your project safely
- ✅ Share with professors and classmates
- ✅ Show your work to potential employers
- ✅ Version control (track all changes)
- ✅ Professional portfolio

## Prerequisites

### 1. Install Git (if not installed)
- Download from: https://git-scm.com/download/win
- Run installer with default settings
- Restart your computer after installation

### 2. Create GitHub Account (FREE)
- Go to: https://github.com/signup
- Use your student email for benefits
- Verify your email address

## Method 1: Automated (Easiest)

### Step 1: Run the Script
```cmd
push_to_github.bat
```

### Step 2: Create GitHub Repository
1. Go to: https://github.com/new
2. Repository name: `climate-crop-monitor`
3. Description: "Climate Crop Monitor - Academic Project for Kisii University"
4. Keep it **Public** (or Private if you prefer)
5. **DO NOT** check "Initialize with README"
6. Click "Create repository"

### Step 3: Copy Repository URL
- After creating, you'll see a URL like:
  ```
  https://github.com/YOUR_USERNAME/climate-crop-monitor.git
  ```
- Copy this URL

### Step 4: Enter URL in Script
- Paste the URL when the script asks
- Press Enter
- Wait for upload to complete

## Method 2: Manual (Step by Step)

### Step 1: Open Command Prompt
```cmd
cd "C:\Users\HP\Climate Crop Monitor (CCM)"
```

### Step 2: Initialize Git
```cmd
git init
```

### Step 3: Configure Git (First Time Only)
```cmd
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 4: Add All Files
```cmd
git add .
```

### Step 5: Create First Commit
```cmd
git commit -m "Initial commit - Climate Crop Monitor v1.1.1"
```

### Step 6: Create GitHub Repository
- Go to: https://github.com/new
- Repository name: `climate-crop-monitor`
- Click "Create repository"
- Copy the repository URL

### Step 7: Connect to GitHub
```cmd
git remote add origin https://github.com/YOUR_USERNAME/climate-crop-monitor.git
git branch -M main
git push -u origin main
```

### Step 8: Enter Credentials
- Username: Your GitHub username
- Password: Use **Personal Access Token** (not your password!)

## How to Get Personal Access Token

### Step 1: Go to GitHub Settings
- Click your profile picture (top right)
- Settings → Developer settings → Personal access tokens → Tokens (classic)

### Step 2: Generate New Token
- Click "Generate new token (classic)"
- Note: "Climate Crop Monitor Access"
- Expiration: 90 days (or custom)
- Select scopes: Check **repo** (all sub-options)
- Click "Generate token"

### Step 3: Copy Token
- Copy the token immediately (you won't see it again!)
- Use this as your password when pushing to GitHub

## Troubleshooting

### "Git is not recognized"
- Install Git from https://git-scm.com/download/win
- Restart computer
- Try again

### "Authentication failed"
- Use Personal Access Token, not your password
- Make sure token has 'repo' permissions

### "Remote origin already exists"
```cmd
git remote remove origin
git remote add origin YOUR_URL
git push -u origin main
```

### "Failed to push"
```cmd
git pull origin main --allow-unrelated-histories
git push -u origin main
```

## After Pushing Successfully

### 1. Verify on GitHub
- Go to your repository URL
- Check if all files are there
- README.md should display nicely

### 2. Add Repository Details
- Click "About" (gear icon)
- Add description: "Climate monitoring system for Kenyan farmers"
- Add topics: `django`, `python`, `agriculture`, `weather-api`, `kisii-university`
- Save changes

### 3. Make Repository Professional
- Add a nice description
- Enable Issues (for feedback)
- Add topics/tags
- Star your own repo!

## Future Updates

When you make changes to your project:

```cmd
git add .
git commit -m "Description of changes"
git push
```

## Useful Git Commands

```cmd
# Check status
git status

# See commit history
git log --oneline

# Create new branch
git checkout -b feature-name

# Switch branches
git checkout main

# Pull latest changes
git pull

# Clone repository elsewhere
git clone YOUR_REPO_URL
```

## Tips for Students

1. **Commit Often** - Save your progress regularly
2. **Write Clear Messages** - Describe what you changed
3. **Use Branches** - For experimental features
4. **Keep .env Secret** - Never commit sensitive data
5. **Update README** - Keep documentation current

## Example Commit Messages

Good:
- "Add weather API integration"
- "Fix login redirect issue"
- "Update database models for v1.1"

Bad:
- "changes"
- "fix"
- "update"

## Share Your Project

After pushing to GitHub, share your repository:
- With professors: Send the GitHub URL
- On LinkedIn: Add to your projects
- On resume: Include GitHub link
- With classmates: They can clone and learn

## Repository URL Format

Your project will be at:
```
https://github.com/YOUR_USERNAME/climate-crop-monitor
```

Example:
```
https://github.com/aronsigei/climate-crop-monitor
```

---

## Need Help?

- GitHub Docs: https://docs.github.com
- Git Tutorial: https://git-scm.com/docs/gittutorial
- Ask your classmates or professors

**Remember:** Your project is now safely backed up and professionally presented on GitHub! 🎉