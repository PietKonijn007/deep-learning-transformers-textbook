# HTML Build for Deep Learning and Transformers Textbook

This folder contains the HTML version of the textbook with proper mathematical formula rendering using MathJax.

## Building the HTML Version

### Option 1: Using make4ht (Recommended)

```bash
# Install tex4ht if not already installed
# On macOS with MacTeX: already included
# On Ubuntu: sudo apt-get install tex4ht

# Build HTML
make4ht main.tex "mathjax,html5"
```

### Option 2: Using pandoc

```bash
# Install pandoc if needed
# On macOS: brew install pandoc

# Build HTML
./build-html.sh
```

### Option 3: Using our custom Python converter

```bash
# Install dependencies
pip install -r requirements.txt

# Build HTML
python convert_to_html.py
```

## Viewing the HTML

After building, open `index.html` in your web browser. All mathematical formulas will render beautifully using MathJax.

## Features

- ✅ Full MathJax support for LaTeX math
- ✅ Responsive design for mobile and desktop
- ✅ Syntax highlighting for code blocks
- ✅ Navigation between chapters
- ✅ Table of contents
- ✅ Dark mode support (optional)

## File Structure

```
html-build/
├── index.html              # Main entry point
├── chapters/               # Individual chapter HTML files
├── css/                    # Stylesheets
├── js/                     # JavaScript for interactivity
└── assets/                 # Images and other assets
```
