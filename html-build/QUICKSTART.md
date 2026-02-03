# Quick Start Guide - Multi-Book System

## Overview

This system generates HTML versions of two books:
1. **Deep Tech Book**: "Deep Learning and Transformers" (36 chapters)
2. **Leadership Book**: "Deep Learning and LLMs for Technical Leaders" (21 chapters)

Both books are served through a single Node.js application with a book selector landing page.

## Generate HTML Versions

### Deep Tech Book (Technical Deep Dive)

```bash
python3 html-build/convert_to_html.py
```

This generates 36 chapters to:
- `nodejs-version/public/chapters/deeptech/`
- Includes TikZ diagrams converted to SVG

### Leadership Book (Strategic Guide)

```bash
python3 html-build/convert_leadership_final.py
```

This generates 21 chapters to:
- `nodejs-version/public/chapters/leadership/`
- Includes PNG diagrams from leadership-book
- Converts tcolorbox, fbox/parbox, and all LaTeX environments

## Run Locally

```bash
cd nodejs-version
npm install
node server.js
```

Then open: http://localhost:3000

You'll see:
- **Book Selector**: Choose between Deep Tech or Leadership book
- **Deep Tech Book**: http://localhost:3000/deeptech.html
- **Leadership Book**: http://localhost:3000/leadership.html

## Directory Structure

```
nodejs-version/public/
├── book-selector.html       # Landing page
├── deeptech.html           # Deep tech book interface
├── leadership.html         # Leadership book interface
├── deeptech-app.js         # Deep tech book logic
├── leadership-app.js       # Leadership book logic
├── styles.css              # Shared styles
└── chapters/
    ├── deeptech/          # 36 HTML chapters
    ├── leadership/        # 21 HTML chapters
    └── diagrams/          # Shared diagrams (PNG + SVG)
```

## Features

✅ **Two Complete Books** - Technical deep dive and strategic leadership guide  
✅ **Beautiful Math Rendering** - MathJax for all equations  
✅ **Responsive Design** - Works on desktop, tablet, and mobile  
✅ **Interactive Navigation** - Sidebar with chapter list and search  
✅ **Styled Content** - Definitions, theorems, examples, key points, cautions  
✅ **Diagrams** - PNG for leadership book, SVG for deep tech book  
✅ **Fast Loading** - Compression and caching enabled  

## Conversion Scripts

### `convert_to_html.py` (Deep Tech Book)
- Converts 36 chapters from `chapters/*.tex`
- Processes TikZ diagrams to SVG
- Outputs to `nodejs-version/public/chapters/deeptech/`
- Updates paths for multi-book structure

### `convert_leadership_final.py` (Leadership Book)
- Converts 21 chapters from `leadership-book/chapters/*.tex`
- Handles tcolorbox → styled divs
- Handles fbox/parbox → formula boxes
- Converts \includegraphics to <img> tags
- Outputs to `nodejs-version/public/chapters/leadership/`

## Deployment

### Vercel (Recommended)

```bash
cd nodejs-version
vercel deploy
```

The `vercel.json` configuration is already set up for:
- Node.js runtime
- Static file serving
- Proper routing

### Other Platforms

The `nodejs-version/` folder is a complete Express.js app that can be deployed to:
- Heroku
- Railway
- Render
- Any Node.js hosting platform

## Troubleshooting

**Diagrams not showing?**
- Check that diagrams exist in `nodejs-version/public/chapters/diagrams/`
- Leadership book uses PNG files
- Deep tech book uses SVG files
- Hard refresh browser (Cmd+Shift+R or Ctrl+Shift+R)

**Math not rendering?**
- Check internet connection (MathJax loads from CDN)
- Open browser console for errors

**Missing chapters?**
- Run the appropriate conversion script
- Check that LaTeX source files exist
- Verify output directory structure

**Styling issues?**
- Clear browser cache
- Check that `styles.css` exists in `nodejs-version/public/`

## Development Workflow

1. **Edit LaTeX source** in `chapters/` or `leadership-book/chapters/`
2. **Run conversion script** to regenerate HTML
3. **Test locally** with `node server.js`
4. **Deploy** when ready

## File Locations

- **Deep Tech LaTeX**: `chapters/*.tex`
- **Leadership LaTeX**: `leadership-book/chapters/*.tex`
- **Deep Tech HTML**: `nodejs-version/public/chapters/deeptech/*.html`
- **Leadership HTML**: `nodejs-version/public/chapters/leadership/*.html`
- **Diagrams**: `nodejs-version/public/chapters/diagrams/`
- **Conversion Scripts**: `html-build/convert_*.py`
