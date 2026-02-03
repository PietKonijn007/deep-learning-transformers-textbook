# HTML Build System - Multi-Book Architecture

This directory contains the LaTeX to HTML conversion system for two books:
1. **Deep Learning and Transformers** (Technical Deep Dive)
2. **Deep Learning and LLMs for Technical Leaders** (Strategic Guide)

## Quick Start

### Convert Deep Tech Book (36 chapters)

```bash
python3 html-build/convert_to_html.py
```

Outputs to: `nodejs-version/public/chapters/deeptech/`

### Convert Leadership Book (21 chapters)

```bash
python3 html-build/convert_leadership_final.py
```

Outputs to: `nodejs-version/public/chapters/leadership/`

### Run Locally

```bash
cd nodejs-version
npm install
node server.js
```

Visit: http://localhost:3000

## Architecture

### Multi-Book System

The application serves both books through a single Node.js server:

```
nodejs-version/public/
├── book-selector.html       # Landing page - choose your book
├── deeptech.html           # Deep tech book interface
├── leadership.html         # Leadership book interface
├── deeptech-app.js         # Deep tech book logic
├── leadership-app.js       # Leadership book logic
├── styles.css              # Shared styles
└── chapters/
    ├── deeptech/          # 36 HTML chapters (from chapters/*.tex)
    ├── leadership/        # 21 HTML chapters (from leadership-book/chapters/*.tex)
    └── diagrams/          # Shared diagrams (PNG + SVG)
```

### Path Resolution

Both books use relative paths in HTML (`../diagrams/...`) which are converted to absolute paths (`/chapters/diagrams/...`) by JavaScript when content is loaded dynamically.

## Conversion Scripts

### `convert_to_html.py` - Deep Tech Book

**Source**: `chapters/*.tex` (36 chapters)  
**Output**: `nodejs-version/public/chapters/deeptech/`

Features:
- Converts all LaTeX environments (theorem, definition, example, etc.)
- Processes TikZ diagrams → SVG
- Handles tables, figures, equations
- Updates paths for multi-book structure

### `convert_leadership_final.py` - Leadership Book

**Source**: `leadership-book/chapters/*.tex` (21 chapters)  
**Output**: `nodejs-version/public/chapters/leadership/`

Features:
- All features from `convert_to_html.py` PLUS:
- Converts `tcolorbox` → styled divs (keypoint, example, caution)
- Converts `fbox/parbox` → formula boxes
- Converts `\includegraphics` → `<img>` tags
- Removes LaTeX spacing commands (`\vspace`, `\hspace`, `\noindent`)
- Handles PNG diagrams from leadership-book

## Deployment

### Vercel (Recommended)

```bash
cd nodejs-version
vercel deploy
```

Configuration in `vercel.json`:
- Node.js runtime
- Express.js server
- Static file serving from `public/`
- Proper routing for both books

### Other Platforms

The `nodejs-version/` folder is a complete Express.js application that can be deployed to:
- Heroku
- Railway
- Render
- Any Node.js hosting platform

## Development Workflow

1. **Edit LaTeX source**:
   - Deep tech: `chapters/*.tex`
   - Leadership: `leadership-book/chapters/*.tex`

2. **Run conversion script**:
   ```bash
   python3 html-build/convert_to_html.py              # Deep tech
   python3 html-build/convert_leadership_final.py     # Leadership
   ```

3. **Test locally**:
   ```bash
   cd nodejs-version
   node server.js
   ```

4. **Deploy**:
   ```bash
   cd nodejs-version
   vercel deploy
   ```

## Key Features

### LaTeX Support

Both scripts support:
- ✅ All theorem environments (theorem, lemma, corollary, proposition)
- ✅ Definition, example, exercise, solution, proof
- ✅ Tables with booktabs
- ✅ Figures with captions
- ✅ Equations (inline and display)
- ✅ Code blocks (lstlisting, verbatim)
- ✅ Lists (itemize, enumerate)

### Leadership Book Additional Support

- ✅ `tcolorbox` with title and color options
- ✅ `fbox/parbox` for formula boxes
- ✅ `\includegraphics` for PNG diagrams
- ✅ Automatic path correction for diagrams

### Diagram Handling

- **Deep Tech**: TikZ diagrams converted to SVG
- **Leadership**: PNG diagrams from `leadership-book/chapters/diagrams/`
- **Shared**: All diagrams in `nodejs-version/public/chapters/diagrams/`

## Files in This Directory

- `convert_to_html.py` - Deep tech book conversion (MAIN SCRIPT)
- `convert_leadership_final.py` - Leadership book conversion (MAIN SCRIPT)
- `CONVERSION_SCRIPT_CHANGES.md` - Documentation of conversion features
- `BUILD_INSTRUCTIONS.md` - Detailed build instructions
- `QUICKSTART.md` - Quick reference guide
- `README.md` - This file

## Troubleshooting

### Diagrams Not Showing

1. Check diagrams exist in `nodejs-version/public/chapters/diagrams/`
2. Leadership book uses PNG, deep tech uses SVG
3. Hard refresh browser (Cmd+Shift+R or Ctrl+Shift+R)
4. Check browser console for 404 errors

### Conversion Errors

1. Check LaTeX source files exist
2. Verify Python 3 is installed
3. Check output directory permissions
4. Review error messages for specific issues

### Math Not Rendering

1. Check internet connection (MathJax loads from CDN)
2. Open browser console for errors
3. Verify MathJax script tag in HTML

## Legacy Directories (Not Used)

- `chapters/` (root) - Old output location, now uses `nodejs-version/public/chapters/deeptech/`
- `docs/` - Old GitHub Pages deployment
- `output/` - Old build directory

## Next Steps

See `QUICKSTART.md` for quick reference commands and `BUILD_INSTRUCTIONS.md` for detailed information.
