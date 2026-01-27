# HTML Build for Deep Learning and Transformers Textbook

This folder contains the HTML conversion system for the textbook with proper mathematical formula rendering using MathJax.

## ✅ Quick Start

```bash
cd html-build
python3 convert_to_html.py
open output/index.html
```

That's it! Your HTML book is ready with beautiful math rendering.

## Features

✅ **Perfect Math Rendering** - All LaTeX equations render beautifully using MathJax  
✅ **Custom Macros** - All your custom commands (\\vx, \\mW, \\R, etc.) work perfectly  
✅ **Responsive Design** - Works on desktop, tablet, and mobile  
✅ **Easy Navigation** - Jump between chapters with navigation links  
✅ **Styled Content** - Definitions, theorems, examples clearly distinguished  
✅ **Algorithm Formatting** - Properly formatted pseudocode blocks  
✅ **Fast Loading** - Optimized for quick page loads

## Building the HTML Version

### Python Script (Recommended)

```bash
python3 convert_to_html.py
```

This will:
1. Create the `output/` directory
2. Convert all LaTeX chapters from `../chapters/` to HTML
3. Generate a beautiful index page with navigation
4. Copy CSS from `../docs/css/style.css`
5. Copy or create JavaScript files
6. Configure MathJax with all your custom macros
7. Fix algorithm formatting for proper display

### Alternative: Shell Script

```bash
./build-html.sh
```

Requires pandoc to be installed.

## Viewing the HTML

After building, open `output/index.html` in your web browser:

```bash
# On macOS
open output/index.html

# On Linux
xdg-open output/index.html

# Or just double-click the file
```

## File Structure

```
html-build/
├── convert_to_html.py      # Main conversion script
├── fix_algorithms.py        # Algorithm formatting helper
├── build-html.sh            # Alternative build script
├── requirements.txt         # Python dependencies
├── BUILD_INSTRUCTIONS.md    # Detailed build guide
├── QUICKSTART.md           # Quick reference
├── css/                    # Source CSS (not used, uses ../docs/css/)
├── js/                     # Source JS (not used, uses ../docs/js/)
└── output/                 # Generated HTML (gitignored)
    ├── index.html          # Main entry point
    ├── chapters/           # Individual chapter HTML files
    ├── css/                # Copied stylesheets
    └── js/                 # Copied JavaScript
```

## Customization

### Change Styles

The converter copies CSS from `../docs/css/style.css`. Edit that file to customize:
- Colors and fonts
- Layout and spacing
- Box styles for definitions, theorems, etc.
- Algorithm formatting

### Modify Conversion

Edit `convert_to_html.py` to:
- Add more LaTeX command conversions
- Change HTML structure
- Modify MathJax configuration
- Add new features

## Live Deployment

### Production Site

The textbook is live at: **https://deeplearning.hofkensvermeulen.be/**

### PDF Download

Download the complete PDF: **main_pro.pdf** (located in project root)

### Deployment Options

**GitHub Pages**
1. Copy `output/` contents to a `docs/` folder in your repo root
2. Enable GitHub Pages in repository settings
3. Select `docs/` as the source

**Netlify/Vercel**
1. Drag and drop the `output/` folder to Netlify or Vercel
2. Your site is live instantly!

**Custom Server**
Upload the `output/` folder contents to any web server.

## Technical Details

### MathJax Configuration

The converter automatically configures MathJax with:
- Inline math: `$...$` and `\(...\)`
- Display math: `$$...$$` and `\[...\]`
- All your custom macros from the LaTeX source
- Proper escaping and processing

### Supported LaTeX Features

✅ Chapters, sections, subsections  
✅ Equations (equation, align, align*)  
✅ Definitions, theorems, examples, exercises  
✅ Lists (itemize, enumerate)  
✅ Text formatting (bold, italic, code)  
✅ Code listings  
✅ Algorithms  
✅ Custom boxes (keypoint, implementation, caution)  

## Troubleshooting

**Math not rendering?**
- Check your internet connection (MathJax loads from CDN)
- Open browser console (F12) for errors
- Verify MathJax script loaded: look for "MathJax ready" in console

**Missing chapters?**
- Ensure LaTeX files exist in `../chapters/`
- Check file names match those in `convert_to_html.py`
- Run the converter again

**Styling issues?**
- Clear browser cache (Cmd+Shift+R or Ctrl+Shift+R)
- Check that `css/style.css` was copied to `output/css/`

**Broken navigation?**
- Verify all chapter files were generated
- Check relative paths in HTML files

## Additional Information

### Source Files Location

The converter reads LaTeX files from `../chapters/` directory:
- `preface.tex`
- `notation.tex`
- `chapter01_linear_algebra.tex` through `chapter23_best_practices.tex`

### Output Structure

Each chapter HTML file includes:
- Full MathJax configuration with custom macros (\\vx, \\mW, \\R, etc.)
- Navigation bar with all chapters
- Previous/Next chapter navigation
- Link back to table of contents
- Responsive CSS styling
- JavaScript for interactive features

### Algorithm Formatting

The converter includes automatic algorithm formatting:
- Converts LaTeX algorithm pseudocode to properly formatted HTML
- Handles control structures (for, while, if)
- Formats input/output specifications
- Preserves indentation and structure
- Look for "Fixed algorithms" messages in converter output

### CSS and JavaScript

- CSS is copied from `../docs/css/style.css` (not from local css/ folder)
- JavaScript is copied from `../docs/js/main.js` or created if missing
- Both are placed in `output/css/` and `output/js/` respectively

### Supported Theorem Environments

In addition to basic features, the converter supports:
- Theorems, Lemmas, Corollaries, Propositions
- Proofs (with optional titles)
- All with proper styling and formatting
