# HTML Build System

This directory contains the LaTeX to HTML conversion system for the Deep Learning and Transformers textbook.

## Quick Start

To convert LaTeX chapters to HTML and deploy:

```bash
python html-build/convert_to_html.py
```

This will:
1. Convert all LaTeX chapters to HTML
2. Output files to the **repository root** (where Vercel deploys from)
3. Update chapters in the `chapters/` directory
4. Update `index.html`, `styles.css`, and `app.js`

## Deployment Structure

The site is deployed from the **repository root**:
- `index.html` - Main page
- `chapters/` - All chapter HTML files
- `styles.css` - Styles
- `app.js` - JavaScript
- `css/` and `js/` - Additional assets

## After Running the Script

After converting chapters, commit and push:

```bash
git add index.html chapters/ styles.css app.js
git commit -m "docs: Update HTML chapters"
git push origin main
```

Vercel will automatically deploy the changes.

## Old Folders (Removed)

- `output/` - Old output directory (removed)
- `docs/` - Old GitHub Pages directory (removed)
- `nodejs-version/public/` - Backup copy (kept but not used for deployment)

## Files in This Directory

- `convert_to_html.py` - Main conversion script
- `fix_algorithms.py` - Algorithm formatting fixes
- `BUILD_INSTRUCTIONS.md` - Detailed build instructions
- `QUICKSTART.md` - Quick reference guide
