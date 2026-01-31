# Workflow Summary - Simplified Build Process

## Overview

The build process has been streamlined so that **one command** handles everything:

```bash
python3 html-build/convert_to_html.py
```

This single command now:
1. ✅ Converts all LaTeX chapters to HTML
2. ✅ Updates `chapters/` (Vercel deployment)
3. ✅ Updates `nodejs-version/public/chapters/` (Node.js dev)
4. ✅ Updates `docs/chapters/` (GitHub Pages)
5. ✅ Updates `app.js` in root (Vercel deployment)
6. ✅ Updates `nodejs-version/public/app.js` (Node.js dev)
7. ✅ Updates `nodejs-version/server.js` (API endpoint)
8. ✅ Fixes algorithm formatting
9. ✅ Copies TEX source files to docs

## Why Two Locations?

### Root Directory (Production)
```
app.js
index.html
styles.css
chapters/*.html
```
- **Purpose**: Vercel deployment
- **Why**: Vercel deploys from root by default
- **Updated by**: `convert_to_html.py` script

### nodejs-version/public/ (Development)
```
nodejs-version/public/app.js
nodejs-version/public/index.html
nodejs-version/public/styles.css
nodejs-version/public/chapters/*.html
```
- **Purpose**: Local development and testing
- **Why**: Organized structure, includes Node.js server
- **Updated by**: `convert_to_html.py` script

## Single Source of Truth

The **CHAPTERS array** in `html-build/convert_to_html.py` is the single source of truth:

```python
CHAPTERS = [
    ("preface", "Preface"),
    ("notation", "Notation and Conventions"),
    ("chapter01_linear_algebra", "Chapter 1: Linear Algebra for Deep Learning"),
    # ... all chapters ...
    ("chapter34_dsl_agents", "Chapter 34: DSL and Agent Systems"),
]
```

When you add a chapter here, the script automatically:
- Generates HTML for all output locations
- Updates the menu in `app.js` files
- Updates the API endpoint in `server.js`
- Assigns the correct Part (I-X) based on chapter number

## Adding a New Chapter - Complete Workflow

### 1. Create LaTeX Source
```bash
vim chapters/chapter35_new_topic.tex
```

### 2. Update CHAPTERS Array
Edit `html-build/convert_to_html.py`:
```python
CHAPTERS = [
    # ... existing chapters ...
    ("chapter35_new_topic", "Chapter 35: New Topic"),
]
```

### 3. Run Conversion (Does Everything)
```bash
python3 html-build/convert_to_html.py
```

### 4. Test Locally
```bash
python3 -m http.server 8000
# Open http://localhost:8000
```

### 5. Commit and Deploy
```bash
git add .
git commit -m "Add chapter 35: New Topic"
git push
```

That's it! No manual syncing needed.

## What Gets Updated Automatically

| File | Location | Updated By | Purpose |
|------|----------|------------|---------|
| `chapters/*.html` | Root | Script | Vercel deployment |
| `app.js` | Root | Script | Vercel deployment |
| `index.html` | Root | Manual* | Vercel deployment |
| `styles.css` | Root | Manual* | Vercel deployment |
| `nodejs-version/public/chapters/*.html` | Dev | Script | Local testing |
| `nodejs-version/public/app.js` | Dev | Script | Local testing |
| `nodejs-version/public/index.html` | Dev | Manual* | Local testing |
| `nodejs-version/public/styles.css` | Dev | Manual* | Local testing |
| `nodejs-version/server.js` | Dev | Script | API endpoint |
| `docs/chapters/*.html` | Docs | Script | GitHub Pages |
| `docs/chapters/*.tex` | Docs | Script | Reference |

\* Manual updates to `index.html` and `styles.css` still need to be copied from `nodejs-version/public/` to root, but this is rare.

## Benefits of This Approach

1. **No Manual Syncing**: Script handles all synchronization
2. **Single Source of Truth**: CHAPTERS array is the only place to add chapters
3. **Automatic Menu Updates**: Chapter list in app.js updated automatically
4. **Consistent**: All locations always in sync
5. **Fast**: One command does everything
6. **Safe**: Can't forget to update a location

## When to Manually Sync

Only when updating `index.html` or `styles.css`:

```bash
# After editing nodejs-version/public/index.html or styles.css
cp nodejs-version/public/index.html index.html
cp nodejs-version/public/styles.css styles.css
git add index.html styles.css
git commit -m "Update UI"
git push
```

Or use the sync script:
```bash
./sync-to-root.sh
```

## Architecture Decision

**Why not deploy from nodejs-version/?**
- Vercel deploys from root by default
- Changing this requires complex configuration
- Current approach is simple and works reliably
- Root deployment is standard for static sites

**Why keep nodejs-version/?**
- Organized development structure
- Local Node.js server for testing
- Clear separation of concerns
- Easy to understand and maintain

## Summary

The improved workflow means:
- ✅ Add chapter to CHAPTERS array
- ✅ Run `python3 html-build/convert_to_html.py`
- ✅ Everything is updated automatically
- ✅ Commit and push
- ✅ Done!

No more manual syncing of chapter lists. No more forgetting to update a file. One command, everything updated.
