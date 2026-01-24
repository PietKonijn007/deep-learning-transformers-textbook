# Vercel Deployment Checklist ✅

Use this checklist to ensure a smooth deployment to Vercel.

## Pre-Deployment

- [ ] All chapter HTML files are in `../docs/chapters/`
- [ ] `npm install` runs without errors
- [ ] `npm start` works locally
- [ ] Test at least 3 chapters load correctly
- [ ] Dark mode toggle works
- [ ] Search functionality works
- [ ] Mobile view looks good

## Git Setup

- [ ] Code is committed to Git
- [ ] Repository is pushed to GitHub/GitLab/Bitbucket
- [ ] Repository is public or you have Vercel access

## Vercel Account

- [ ] Created account at [vercel.com](https://vercel.com)
- [ ] Connected Git provider (GitHub/GitLab/Bitbucket)

## Deployment Method

Choose one:

### Method A: Vercel Dashboard (Easiest)
- [ ] Go to [vercel.com/new](https://vercel.com/new)
- [ ] Import your repository
- [ ] Set root directory to `nodejs-version`
- [ ] Click Deploy
- [ ] Wait for deployment to complete

### Method B: Vercel CLI
- [ ] Install CLI: `npm install -g vercel`
- [ ] Login: `vercel login`
- [ ] Navigate to `nodejs-version` directory
- [ ] Run: `vercel`
- [ ] Follow prompts
- [ ] Deploy to production: `vercel --prod`

### Method C: Helper Script
- [ ] Run: `./deploy-vercel.sh`
- [ ] Choose option 1 (preview) or 2 (production)

## Post-Deployment

- [ ] Visit your Vercel URL
- [ ] Test homepage loads
- [ ] Test at least 5 different chapters
- [ ] Test search functionality
- [ ] Test dark mode toggle
- [ ] Test on mobile device
- [ ] Test keyboard navigation (← →)
- [ ] Check math equations render correctly
- [ ] Test TOC button (📑)

## Optional Enhancements

- [ ] Add custom domain in Vercel settings
- [ ] Set up environment variables (if needed)
- [ ] Enable automatic deployments on Git push
- [ ] Add deployment badge to README

## Troubleshooting

If chapters don't load:
- [ ] Check Vercel function logs
- [ ] Verify `docs/chapters/` directory structure
- [ ] Check server.js path resolution
- [ ] Test API endpoints: `/api/chapters` and `/api/chapter/preface`

If build fails:
- [ ] Check Vercel build logs
- [ ] Verify package.json is correct
- [ ] Test `npm install` locally
- [ ] Check Node.js version compatibility

## Success Criteria

✅ Deployment successful when:
- Homepage loads in < 2 seconds
- All chapters are accessible
- Search works
- Dark mode toggles
- Mobile view is responsive
- Math renders correctly
- No console errors

## Share Your Deployment

Once deployed, share your URL:
- Format: `https://your-project.vercel.app`
- Share with team/users
- Add to documentation
- Update README with live link

---

**Need Help?**
- See [VERCEL_DEPLOY.md](VERCEL_DEPLOY.md) for detailed guide
- Check [Vercel Docs](https://vercel.com/docs)
- Review deployment logs in Vercel dashboard
