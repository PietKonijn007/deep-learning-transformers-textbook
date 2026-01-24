# Deploy to Vercel - Quick Guide

## Prerequisites
- Vercel account (free at [vercel.com](https://vercel.com))
- Git repository (GitHub, GitLab, or Bitbucket)

## Method 1: Deploy via Vercel Dashboard (Recommended)

### Step 1: Push to Git
```bash
# If not already in a git repo
git init
git add .
git commit -m "Ready for Vercel deployment"

# Push to GitHub/GitLab/Bitbucket
git remote add origin your-repo-url
git push -u origin main
```

### Step 2: Import to Vercel
1. Go to [vercel.com/new](https://vercel.com/new)
2. Click "Import Project"
3. Select your Git repository
4. Configure project:
   - **Framework Preset**: Other
   - **Root Directory**: `nodejs-version`
   - **Build Command**: (leave empty)
   - **Output Directory**: (leave empty)
   - **Install Command**: `npm install`

### Step 3: Deploy
1. Click "Deploy"
2. Wait for deployment to complete (usually 1-2 minutes)
3. Your app will be live at `https://your-project.vercel.app`

## Method 2: Deploy via Vercel CLI

### Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

### Step 2: Login
```bash
vercel login
```

### Step 3: Deploy
```bash
# Navigate to the nodejs-version directory
cd nodejs-version

# Deploy
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? (select your account)
# - Link to existing project? No
# - What's your project's name? (enter a name)
# - In which directory is your code located? ./
```

### Step 4: Production Deployment
```bash
# After testing, deploy to production
vercel --prod
```

## Important Notes

### Directory Structure
The deployment expects this structure:
```
nodejs-version/
├── server.js          # Express server
├── package.json       # Dependencies
├── vercel.json        # Vercel configuration
├── public/            # Static files
│   ├── index.html
│   ├── app.js
│   └── styles.css
└── ../docs/chapters/  # Chapter HTML files (parent directory)
```

### Environment Variables
If you need to set environment variables:

**Via Dashboard:**
1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add variables (e.g., `NODE_ENV=production`)

**Via CLI:**
```bash
vercel env add NODE_ENV production
```

### Custom Domain
1. Go to your project settings
2. Navigate to "Domains"
3. Add your custom domain
4. Update DNS records as instructed

## Troubleshooting

### Chapters Not Loading
If chapters aren't loading, verify:
1. The `docs/chapters/` directory is in the parent directory
2. All HTML files are present
3. Check Vercel function logs for errors

### Build Fails
```bash
# Test locally first
cd nodejs-version
npm install
npm start

# Check for errors
```

### View Logs
```bash
# Via CLI
vercel logs

# Or check the Vercel dashboard under "Deployments" > "Functions"
```

## Automatic Deployments

Once connected to Git:
- **Push to main branch** → Automatic production deployment
- **Push to other branches** → Automatic preview deployment
- Each PR gets its own preview URL

## Cost
- **Free tier includes:**
  - 100GB bandwidth/month
  - Unlimited deployments
  - Automatic HTTPS
  - Global CDN
  - Perfect for this textbook app!

## Next Steps

After deployment:
1. Test all chapters load correctly
2. Check mobile responsiveness
3. Share your URL!
4. Set up custom domain (optional)

## Support

- Vercel Docs: https://vercel.com/docs
- Vercel Support: https://vercel.com/support
- Check deployment logs in dashboard for errors
