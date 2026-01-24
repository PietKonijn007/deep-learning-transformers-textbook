# Quick Start Guide

## Generate HTML Version

Simply run:

```bash
python3 convert_to_html.py
```

This will:
1. Create the `output/` directory
2. Convert all LaTeX chapters to HTML
3. Generate a beautiful index page with navigation
4. Copy CSS and JavaScript files

## View the Result

Open `output/index.html` in your web browser:

```bash
# On macOS
open output/index.html

# On Linux
xdg-open output/index.html

# Or just double-click the file
```

## Features

✅ **Beautiful Math Rendering** - All equations render perfectly using MathJax  
✅ **Responsive Design** - Works on desktop, tablet, and mobile  
✅ **Easy Navigation** - Jump between chapters with navigation links  
✅ **Styled Content** - Definitions, theorems, examples, and exercises are clearly distinguished  
✅ **Code Highlighting** - Python code blocks are properly formatted  
✅ **Fast Loading** - Optimized for quick page loads  

## Customization

### Change Styles

Edit `css/style.css` to customize:
- Colors and fonts
- Layout and spacing
- Dark mode (optional)

### Modify Conversion

Edit `convert_to_html.py` to:
- Add more LaTeX command conversions
- Change HTML structure
- Add new features

## Deployment

To deploy online:

### GitHub Pages

1. Copy `output/` contents to a `docs/` folder in your repo root
2. Enable GitHub Pages in repository settings
3. Select `docs/` as the source

### Netlify/Vercel

1. Drag and drop the `output/` folder to Netlify or Vercel
2. Your site is live!

### Custom Server

Upload the `output/` folder contents to any web server.

## Troubleshooting

**Math not rendering?**
- Check your internet connection (MathJax loads from CDN)
- Open browser console for errors

**Missing chapters?**
- Ensure LaTeX files exist in `../chapters/`
- Check file names match those in `convert_to_html.py`

**Styling issues?**
- Clear browser cache
- Check that `css/style.css` was copied to `output/css/`
