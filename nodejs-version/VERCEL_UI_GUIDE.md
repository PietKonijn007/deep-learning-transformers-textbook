# Vercel Dashboard Deployment - UI Guide

## Issue: nodejs-version folder not showing in directory picker

If you don't see `nodejs-version` in the Vercel directory picker, follow these steps:

## Solution: Configure Root Directory Manually

### Step 1: Select Root Repository
In the "Root Directory" dialog:
- ✅ Select `deep-learning-transformers-textbook` (the root)
- ❌ Don't try to select a subdirectory
- Click **Continue**

### Step 2: Configure Project Settings
On the next screen, you'll see "Configure Project":

1. **Framework Preset**: Select "Other" (or leave as detected)

2. **Root Directory**: 
   - Click "Edit" next to Root Directory
   - Type: `nodejs-version`
   - Or click the folder icon and navigate to `nodejs-version`

3. **Build Command**: Leave empty (or `npm install`)

4. **Output Directory**: Leave empty

5. **Install Command**: `npm install` (should be auto-detected)

### Step 3: Environment Variables (Optional)
Skip this for now - no environment variables needed.

### Step 4: Deploy
Click **Deploy** button and wait 1-2 minutes.

## Alternative: Use CLI Instead

If the UI is giving you trouble, the CLI is much simpler:

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Navigate to nodejs-version
cd nodejs-version

# Deploy
vercel

# Deploy to production
vercel --prod
```

## Visual Guide

```
Your Repository Structure:
├── chapters/
├── docs/
├── html-build/
├── nodejs-version/     ← This is what you want to deploy
│   ├── server.js
│   ├── package.json
│   ├── public/
│   └── vercel.json
├── tasks/
└── README.md

In Vercel UI:
1. Select root: deep-learning-transformers-textbook
2. Click Continue
3. Set "Root Directory" to: nodejs-version
4. Click Deploy
```

## Why This Happens

Vercel's directory picker sometimes doesn't show all folders, especially if:
- The folder was recently added
- There are many folders in the repo
- The UI is caching an old view

The solution is to select the root and then manually specify the subdirectory.

## Verification

After deployment, verify these URLs work:
- `https://your-project.vercel.app` → Homepage
- `https://your-project.vercel.app/api/chapters` → Chapter list JSON
- `https://your-project.vercel.app/api/chapter/preface` → Preface HTML

## Still Having Issues?

### Option 1: Use Vercel CLI (Recommended)
```bash
cd nodejs-version
vercel
```
This is the most reliable method!

### Option 2: Check Git
Make sure nodejs-version is committed and pushed:
```bash
git status
git add nodejs-version/
git commit -m "Add nodejs-version for deployment"
git push origin main
```

### Option 3: Try Vercel CLI to Link
```bash
cd nodejs-version
vercel link
# This creates a .vercel directory
# Then deploy:
vercel --prod
```

## Success!

Once deployed, you'll get a URL like:
`https://your-project-name.vercel.app`

Test it and enjoy your deployed textbook! 🎉
