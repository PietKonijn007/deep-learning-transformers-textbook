# Build Instructions

## Quick Start

To build the HTML version of the textbook:

```bash
cd html-build
python3 convert_to_html.py
```

This will:
1. Convert all LaTeX chapters to HTML
2. Generate the index page
3. Copy CSS and JavaScript files
4. **Automatically fix algorithm formatting**
5. Output everything to `html-build/output/`

## What Gets Fixed Automatically

### Algorithm Blocks
LaTeX pseudocode commands are automatically converted to properly formatted HTML:
- `\KwIn{...}` → Input declarations
- `\KwOut{...}` → Output declarations
- `\For`, `\While`, `\If` → Control structures with indentation
- `\Return` → Return statements
- `\KwTo` → "to" keyword

### Code Blocks
LaTeX `lstlisting` environments are converted to HTML `<pre><code>` blocks.

### Math Equations
All math is preserved for MathJax rendering using `$...$` delimiters.

## Output Structure

```
html-build/output/
├── index.html              # Main table of contents
├── chapters/
│   ├── preface.html
│   ├── notation.html
│   ├── chapter01_linear_algebra.html
│   ├── chapter02_calculus_optimization.html
│   └── ...
├── css/
│   └── style.css          # Includes algorithm styles
└── js/
    └── main.js
```

## CSS Styles

The CSS file (`html-build/css/style.css`) is automatically synced from `docs/css/style.css` and includes:
- Algorithm box styling
- Algorithm indentation
- Code block formatting
- Math equation display
- Responsive design
- Print styles

## Viewing the Output

After building, open `html-build/output/index.html` in your browser.

## Troubleshooting

### Algorithms not rendering correctly
The algorithm fix is now integrated into the build process. If you see issues:
1. Check that `html-build/css/style.css` has the algorithm styles
2. Verify the conversion script includes the `fix_algorithms()` function
3. Run the standalone fix: `python3 fix_algorithms.py` from the html-build directory

### Missing CSS styles
If styles are missing, copy from the working version:
```bash
cp docs/css/style.css html-build/css/style.css
```

### Math not rendering
Ensure MathJax is loading. Check the browser console for errors.

## Development Workflow

1. Edit LaTeX source files in `chapters/`
2. Run `python3 convert_to_html.py` from `html-build/`
3. Check output in `html-build/output/`
4. Copy to `docs/` for GitHub Pages deployment if needed

## Deployment

To deploy to GitHub Pages:
```bash
# After building
cp -r html-build/output/* docs/
git add docs/
git commit -m "Update HTML version"
git push
```
