# Deployment Architecture

## Overview

This repository contains a Deep Learning and Transformers textbook with multiple output formats:
1. **PDF** - LaTeX compiled textbook (main_pro.pdf)
2. **Static HTML** - Interactive web version deployed to Vercel
3. **Source Materials** - LaTeX source files and build tools

## Directory Structure

```
.
├── chapters/                    # LaTeX source files for all chapters
│   ├── chapter01_*.tex         # Chapter 1-34 source files
│   ├── chapter01_*.html        # Generated HTML (for reference)
│   ├── preface.tex
│   └── notation.tex
│
├── html-build/                  # HTML generation tools
│   └── convert_to_html.py      # Main conversion script (TEX → HTML)
│
├── docs/                        # GitHub Pages deployment (legacy)
│   └── chapters/               # Copy of generated HTML files
│
├── nodejs-version/              # Node.js development version (NOT DEPLOYED)
│   ├── public/                 # Source files for web app
│   │   ├── app.js             # Main application logic
│   │   ├── index.html         # Main HTML template
│   │   ├── styles.css         # Application styles
│   │   └── chapters/          # Chapter HTML files
│   ├── server.js              # Local development server
│   └── package.json           # Node.js dependencies
│
├── ROOT FILES (DEPLOYED TO VERCEL)
│   ├── app.js                 # Main application (copied from nodejs-version/public/)
│   ├── index.html             # Main page (copied from nodejs-version/public/)
│   ├── styles.css             # Styles (copied from nodejs-version/public/)
│   ├── chapters/              # Chapter HTML files (symlinked or copied)
│   ├── css/                   # Additional CSS
│   ├── js/                    # Additional JS
│   └── vercel.json            # Vercel deployment configuration
│
└── tasks/                      # Chapter writing tasks and guides
```

## Deployment Flow

### What Gets Deployed to Vercel

**Vercel deploys from the ROOT directory**, not from `nodejs-version/`.

The deployment includes:
- `index.html` - Main application page
- `app.js` - Application logic with chapter definitions
- `styles.css` - Application styles
- `chapters/*.html` - All chapter HTML files
- `css/` - Additional stylesheets
- `js/` - Additional JavaScript files

### Critical Files for Deployment

1. **app.js** (ROOT)
   - Contains the chapter list array (36 items: preface + notation + 34 chapters)
   - Handles navigation, rendering, and chapter loading
   - **MUST be kept in sync with nodejs-version/public/app.js**

2. **index.html** (ROOT)
   - Main application shell
   - Loads app.js with cache-busting
   - **MUST be kept in sync with nodejs-version/public/index.html**

3. **styles.css** (ROOT)
   - Application styling including sidebar, navigation, dark mode
   - **MUST be kept in sync with nodejs-version/public/styles.css**

4. **chapters/*.html** (ROOT)
   - Individual chapter HTML files
   - Generated from LaTeX using `html-build/convert_to_html.py`
   - **MUST be kept in sync with nodejs-version/public/chapters/**

## Development Workflow

### Adding New Chapters

1. **Create LaTeX source**
   ```bash
   # Add new chapter file
   vim chapters/chapter35_new_topic.tex
   ```

2. **Update conversion script**
   ```bash
   # Edit html-build/convert_to_html.py
   # Add new chapter to CHAPTERS list
   ```

3. **Generate HTML**
   ```bash
   python3 html-build/convert_to_html.py
   ```

4. **Update chapter lists in BOTH locations**
   ```bash
   # Edit nodejs-version/public/app.js - add chapter to state.chapters array
   # Edit nodejs-version/server.js - add chapter to /api/chapters endpoint
   ```

5. **Sync to root directory**
   ```bash
   cp nodejs-version/public/app.js app.js
   cp nodejs-version/public/index.html index.html
   cp nodejs-version/public/styles.css styles.css
   cp chapters/*.html nodejs-version/public/chapters/
   ```

6. **Commit and push**
   ```bash
   git add .
   git commit -m "Add chapter 35: New Topic"
   git push
   ```

### Local Development

**Option 1: Node.js Server (Recommended for development)**
```bash
cd nodejs-version
npm install
npm start
# Open http://localhost:3000
```

**Option 2: Static Server (Matches production)**
```bash
# From root directory
python3 -m http.server 8000
# Open http://localhost:8000
```

## File Synchronization

### Critical: Keep These Files in Sync

The following files MUST be identical between `nodejs-version/public/` and root:

| Root File | Source File | Purpose |
|-----------|-------------|---------|
| `app.js` | `nodejs-version/public/app.js` | Application logic |
| `index.html` | `nodejs-version/public/index.html` | Main page |
| `styles.css` | `nodejs-version/public/styles.css` | Styles |
| `chapters/*.html` | `chapters/*.html` | Chapter content |

### Sync Script (Recommended)

Create a sync script to avoid manual copying:

```bash
#!/bin/bash
# sync-to-root.sh

echo "Syncing nodejs-version/public to root..."
cp nodejs-version/public/app.js app.js
cp nodejs-version/public/index.html index.html
cp nodejs-version/public/styles.css styles.css
echo "✓ Core files synced"

echo "Syncing chapters..."
cp chapters/*.html nodejs-version/public/chapters/
echo "✓ Chapters synced"

echo "All files synced successfully!"
```

## Vercel Configuration

### vercel.json (Root)

```json
{
  "version": 2,
  "cleanUrls": true,
  "trailingSlash": false
}
```

This configuration:
- Serves static files from root directory
- Enables clean URLs (no .html extension needed)
- Removes trailing slashes

### Deployment Triggers

Vercel automatically deploys when:
- Commits are pushed to `main` branch
- Pull requests are created (preview deployments)

## Common Issues and Solutions

### Issue: Menu doesn't show new chapters

**Cause**: Root `app.js` not updated with new chapters

**Solution**:
```bash
cp nodejs-version/public/app.js app.js
git add app.js
git commit -m "Update app.js with new chapters"
git push
```

### Issue: Styles not updating

**Cause**: Root `styles.css` not synced

**Solution**:
```bash
cp nodejs-version/public/styles.css styles.css
git add styles.css
git commit -m "Update styles"
git push
```

### Issue: Chapter content not showing

**Cause**: Chapter HTML files not in root `chapters/` directory

**Solution**:
```bash
cp chapters/*.html nodejs-version/public/chapters/
git add chapters/
git commit -m "Update chapter HTML files"
git push
```

## Architecture Decisions

### Why Two Locations?

1. **nodejs-version/public/** - Development source of truth
   - Organized structure for development
   - Includes Node.js server for local testing
   - Clear separation of concerns

2. **Root directory** - Deployment target
   - Vercel deploys from root by default
   - Simpler deployment configuration
   - Matches GitHub Pages structure

### Why Not Deploy from nodejs-version/?

- Vercel's default behavior is to deploy from root
- Changing this requires additional configuration
- Current structure works with minimal config
- Maintains compatibility with GitHub Pages

## Maintenance Checklist

When updating the application:

- [ ] Update LaTeX source in `chapters/`
- [ ] Run `html-build/convert_to_html.py` to generate HTML
- [ ] Update `nodejs-version/public/app.js` with new chapters
- [ ] Update `nodejs-version/server.js` with new chapters (if using API)
- [ ] Copy updated files to root: `app.js`, `index.html`, `styles.css`
- [ ] Copy chapter HTML files to `nodejs-version/public/chapters/`
- [ ] Test locally with `npm start` or static server
- [ ] Commit and push to trigger Vercel deployment
- [ ] Verify deployment at production URL

## URLs

- **Production**: https://[your-vercel-url].vercel.app
- **GitHub Repository**: https://github.com/PietKonijn007/deep-learning-transformers-textbook
- **Local Development**: http://localhost:3000 (Node.js) or http://localhost:8000 (static)

## Contact

For questions about the deployment architecture, refer to this document or check the commit history for recent changes.
