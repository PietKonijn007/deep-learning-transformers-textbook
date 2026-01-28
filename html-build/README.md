# HTML Build System

This directory contains the LaTeX to HTML conversion system for the Deep Learning and Transformers textbook.

## Quick Start

To convert LaTeX chapters to HTML:

```bash
python html-build/convert_to_html.py
```

This will:
1. Convert all LaTeX chapters to HTML
2. Output chapter files to `chapters/` directory in repository root
3. **Does NOT modify** `index.html`, `app.js`, or `styles.css`

**Important:** The conversion script only updates chapter HTML files. The main site files (`index.html`, `app.js`, `styles.css`) are maintained separately and should not be overwritten.

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
git add chapters/
git commit -m "docs: Update chapter content"
git push origin main
```

**Note:** Only commit the `chapters/` directory. Do not commit changes to `index.html`, `app.js`, or `styles.css` unless you've intentionally modified them.

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
