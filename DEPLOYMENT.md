# Deployment Guide

## Current Deployment Structure

The site is deployed from the **repository root** to Vercel at `deeplearning.hofkensvermeulen.be`.

### Active Files (Deployed)
```
/
├── index.html          # Main page
├── app.js             # JavaScript
├── styles.css         # Styles
├── chapters/          # All chapter HTML files
├── css/               # Additional CSS
└── js/                # Additional JS
```

### Backup/Archive
- `nodejs-version/` - Backup copy of the site (not deployed)
- `html-build/` - LaTeX to HTML conversion scripts

## Workflow

### 1. Update LaTeX Chapters

Edit your LaTeX files in `chapters/`:
```bash
vim chapters/chapter01_linear_algebra.tex
```

### 2. Convert to HTML

Run the conversion script:
```bash
python html-build/convert_to_html.py
```

This will:
- Convert all LaTeX chapters to HTML
- Output directly to repository root
- Update `chapters/`, `index.html`, etc.

### 3. Deploy

Commit and push:
```bash
git add index.html chapters/ styles.css app.js
git commit -m "docs: Update chapter content"
git push origin main
```

Vercel will automatically deploy within 1-2 minutes.

## Mobile Menu

The site includes a mobile-responsive sidebar menu:
- **Desktop**: Sidebar always visible on the left
- **Mobile**: Hamburger menu button (☰) in top-left corner
- **Button**: Blue square with three lines, tapping opens sidebar

## Troubleshooting

### Changes not appearing on mobile
1. Clear mobile browser cache
2. Try incognito/private mode
3. Hard refresh (pull down to refresh)

### Vercel not deploying
1. Check Vercel dashboard for deployment status
2. Verify `vercel.json` is in repository root
3. Manually trigger redeploy in Vercel dashboard

### Conversion script errors
1. Ensure you're in repository root when running
2. Check that LaTeX files exist in `chapters/`
3. Verify Python dependencies are installed
