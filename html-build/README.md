# HTML Build for Deep Learning and Transformers Textbook

This folder contains the HTML version of the textbook with proper mathematical formula rendering using MathJax.

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
✅ **Code Highlighting** - Python code blocks properly formatted  
✅ **Fast Loading** - Optimized for quick page loads

## Building the HTML Version

### Option 1: Python Script (Recommended - Works Now!)

```bash
python3 convert_to_html.py
```

This will:
1. Create the `output/` directory
2. Convert all LaTeX chapters to HTML
3. Generate a beautiful index page with navigation
4. Copy CSS and JavaScript files
5. Configure MathJax with all your custom macros

### Option 2: Using pandoc (Alternative)

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
├── build-html.sh            # Alternative build script
├── css/
│   └── style.css           # Beautiful styling
├── js/
│   └── main.js             # Interactive features
└── output/                 # Generated HTML (gitignored)
    ├── index.html          # Main entry point
    ├── chapters/           # Individual chapter HTML files
    ├── css/                # Copied stylesheets
    └── js/                 # Copied JavaScript
```

## Customization

### Change Styles

Edit `css/style.css` to customize:
- Colors and fonts
- Layout and spacing
- Box styles for definitions, theorems, etc.

### Modify Conversion

Edit `convert_to_html.py` to:
- Add more LaTeX command conversions
- Change HTML structure
- Add new features

## Deployment Options

### GitHub Pages

1. Copy `output/` contents to a `docs/` folder in your repo root
2. Enable GitHub Pages in repository settings
3. Select `docs/` as the source
4. Your book is live at `https://username.github.io/repo-name/`

### Netlify/Vercel

1. Drag and drop the `output/` folder to Netlify or Vercel
2. Your site is live instantly!

### Custom Server

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
