# HTML Deployment Structure

## Overview
This document describes the consolidated HTML file structure for the Deep Learning and Transformers textbook.

## Single Source of Truth
All HTML files for deployment are maintained in **one location**:
```
nodejs-version/public/
├── chapters/          # All chapter HTML files (25 files)
├── css/              # Stylesheets
├── js/               # JavaScript files
└── index.html        # Main landing page
```

## Server Configuration
The Node.js/Express server (`nodejs-version/server.js`) serves:
- Static files from `public/` directory
- Chapter content via API endpoint: `/api/chapter/:id`
  - Reads from: `public/chapters/{chapterId}.html`

## Build Process
The conversion script (`html-build/convert_to_html.py`) generates HTML from LaTeX sources and outputs to:
1. **Primary**: `nodejs-version/public/` - Used for deployment
2. **Reference**: `output/` - Kept for local reference/testing

### Running the Build
```bash
python3 html-build/convert_to_html.py
```

This will:
- Convert all LaTeX chapters to HTML
- Remove LaTeX table commands (\\toprule, \\midrule, \\bottomrule)
- Generate proper HTML table structures
- Output to both locations simultaneously

## Vercel Deployment
Vercel deploys only the `nodejs-version/` directory, which contains:
- `server.js` - Express server
- `public/` - All static assets including HTML chapters
- `package.json` - Dependencies
- `vercel.json` - Deployment configuration

The deployment automatically serves files from `public/` and the API endpoints work correctly.

## Removed Directories
The following directories have been removed to eliminate duplication:
- ❌ `docs/chapters/` - Old location, no longer used
- ❌ `docs/css/` - Moved to `nodejs-version/public/css/`
- ❌ `docs/js/` - Moved to `nodejs-version/public/js/`
- ❌ `nodejs-version/chapters/` - Was duplicate, removed

## File Locations Summary

| Content Type | Location | Purpose |
|--------------|----------|---------|
| LaTeX Source | `chapters/*.tex` | Original textbook content |
| Build Script | `html-build/convert_to_html.py` | Converts LaTeX to HTML |
| Deployment HTML | `nodejs-version/public/chapters/*.html` | Served by Express/Vercel |
| Reference HTML | `output/chapters/*.html` | Local reference copy |
| Server | `nodejs-version/server.js` | Express server for deployment |

## Workflow

### Making Changes
1. Edit LaTeX files in `chapters/`
2. Run conversion script: `python3 html-build/convert_to_html.py`
3. Commit changes: `git add -A && git commit -m "..."`
4. Push to deploy: `git push`

### Vercel Auto-Deploy
When you push to the main branch:
1. Vercel detects the push
2. Deploys the `nodejs-version/` directory
3. Serves files from `public/`
4. Site updates automatically at `deeplearning.hofkensvermeule.be`

## Table Rendering Fix
The conversion script now properly handles LaTeX tables:
- ✅ Removes `\begin{table}`, `\end{table}` wrappers
- ✅ Removes booktabs commands (`\toprule`, `\midrule`, `\bottomrule`)
- ✅ Converts to clean HTML `<table>` structures
- ✅ Preserves MathJax expressions in table cells
- ✅ Handles both wrapped and standalone tabular environments

## Maintenance
- Keep HTML files only in `nodejs-version/public/`
- Run build script after any LaTeX changes
- The `output/` directory is for reference only
- Never manually edit HTML files - regenerate from LaTeX
