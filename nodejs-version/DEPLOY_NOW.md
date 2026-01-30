# 🚀 Deploy to Vercel NOW - 5 Minute Guide

The fastest way to get your Deep Learning & Transformers textbook online.

## Option 1: One-Command Deploy (Fastest) ⚡

```bash
cd nodejs-version
./deploy-vercel.sh
```

Choose option 1 for preview or option 2 for production. Done! 🎉

## Option 2: Manual Deploy (5 minutes) 📝

### Step 1: Install Vercel CLI (30 seconds)
```bash
npm install -g vercel
```

### Step 2: Login (30 seconds)
```bash
vercel login
```
Follow the browser prompt to authenticate.

### Step 3: Deploy (2 minutes)
```bash
cd nodejs-version
vercel
```

Answer the prompts:
- **Set up and deploy?** → Yes
- **Which scope?** → (select your account)
- **Link to existing project?** → No
- **Project name?** → (enter a name, e.g., "dl-transformers-book")
- **Directory?** → `./`

### Step 4: Go to Production (1 minute)
```bash
vercel --prod
```

**That's it!** Your app is live at `https://your-project.vercel.app` 🎉

## Option 3: Deploy via Vercel Dashboard (No CLI needed) 🖱️

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Step 2: Import to Vercel
1. Go to [vercel.com/new](https://vercel.com/new)
2. Click "Import Project"
3. Select your repository
4. **Important:** Select the root repository, then click Continue
5. On the "Configure Project" screen:
   - Click "Edit" next to **Root Directory**
   - Type: `nodejs-version`
   - Leave other settings as default
6. Click "Deploy"

**Note:** If you don't see `nodejs-version` in the folder picker, that's normal. Just select the root and manually type `nodejs-version` in the Root Directory field.

### Step 3: Wait
Deployment takes 1-2 minutes. You'll get a live URL when done!

**Having UI issues?** See [VERCEL_UI_GUIDE.md](VERCEL_UI_GUIDE.md) or use the CLI method instead (it's easier!).

## What Gets Deployed?

✅ Your Express server (server.js)
✅ All static files (HTML, CSS, JS)
✅ Chapter content from docs/chapters/
✅ Automatic HTTPS
✅ Global CDN
✅ Automatic compression

## After Deployment

### Test Your Site
Visit your Vercel URL and check:
- [ ] Homepage loads
- [ ] Chapters load (try 3-5 different ones)
- [ ] Search works
- [ ] Dark mode toggles
- [ ] Mobile view looks good

### Share Your URL
Your textbook is now live! Share it:
```
https://your-project.vercel.app
```

### Set Up Custom Domain (Optional)
1. Go to Vercel dashboard
2. Click your project
3. Go to "Settings" → "Domains"
4. Add your domain
5. Update DNS records as shown

## Automatic Updates

Once deployed via Git:
- **Push to main** → Automatic production deployment
- **Push to other branches** → Preview deployments
- **Pull requests** → Preview URLs for testing

## Cost

**FREE** for this project! Includes:
- 100GB bandwidth/month
- Unlimited deployments
- Automatic HTTPS
- Global CDN
- More than enough for a textbook!

## Troubleshooting

### "Command not found: vercel"
```bash
npm install -g vercel
# If that fails, try:
sudo npm install -g vercel
```

### Chapters not loading
Check that `docs/chapters/` exists in parent directory:
```bash
ls ../docs/chapters/
```

### Build fails
Test locally first:
```bash
npm install
npm start
```

### Need help?
- Check [VERCEL_DEPLOY.md](VERCEL_DEPLOY.md) for detailed guide
- Use [VERCEL_CHECKLIST.md](VERCEL_CHECKLIST.md) for step-by-step
- Visit [vercel.com/docs](https://vercel.com/docs)

## Quick Commands Reference

```bash
# Deploy to preview
vercel

# Deploy to production
vercel --prod

# Check deployments
vercel ls

# View logs
vercel logs

# Remove deployment
vercel rm your-deployment-url
```

---

**Ready? Let's deploy!** 🚀

Choose your method above and get your textbook online in 5 minutes!
