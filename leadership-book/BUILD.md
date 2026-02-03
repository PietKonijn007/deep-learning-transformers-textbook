# Building the Leadership Book

## Prerequisites

### Required
- **LaTeX Distribution**: 
  - macOS: `brew install --cask mactex` or `brew install --cask basictex`
  - Ubuntu/Debian: `sudo apt-get install texlive-full`
  - Windows: Install MiKTeX or TeX Live

### Recommended
- **Inkscape** (for optimal SVG rendering):
  - macOS: `brew install inkscape`
  - Ubuntu/Debian: `sudo apt-get install inkscape`
  - Windows: Download from https://inkscape.org/

## Quick Build

```bash
cd leadership-book
./compile.sh
```

This will:
1. Clean previous build artifacts
2. Run pdflatex three times (for references and TOC)
3. Generate `main.pdf`

## Manual Build

If you prefer to build manually:

```bash
cd leadership-book

# First pass
pdflatex main.tex

# Process bibliography (if needed)
bibtex main

# Second pass (resolve references)
pdflatex main.tex

# Third pass (finalize)
pdflatex main.tex
```

## SVG Support

The book uses SVG diagrams for high-quality graphics. LaTeX handles SVGs in two ways:

### Option 1: Direct SVG (with svg package)
The `main.tex` includes `\usepackage{svg}` which requires:
- Inkscape installed
- Shell escape enabled: `pdflatex -shell-escape main.tex`

### Option 2: Convert SVG to PDF (recommended for production)
Convert SVGs to PDFs first for faster compilation:

```bash
cd chapters/diagrams
for file in *.svg; do
    inkscape "$file" --export-pdf="${file%.svg}.pdf"
done
```

Then update `main.tex` to use PDFs instead of SVGs.

## Troubleshooting

### SVG Not Rendering
**Problem**: Diagrams don't appear in PDF

**Solutions**:
1. Install Inkscape: `brew install inkscape`
2. Enable shell escape: `pdflatex -shell-escape main.tex`
3. Or convert SVGs to PDF manually (see above)

### Missing Packages
**Problem**: LaTeX complains about missing packages

**Solution**: Install the full TeX Live distribution:
```bash
# macOS
brew install --cask mactex

# Ubuntu
sudo apt-get install texlive-full
```

### Compilation Errors
**Problem**: Build fails with errors

**Solution**: Check `main.log` for details:
```bash
tail -50 main.log
```

Common issues:
- Missing `\end{...}` tags
- Unclosed math environments
- Invalid LaTeX commands

## Output Files

After successful compilation:
- `main.pdf` - The final book (this is what you want!)
- `main.aux` - Auxiliary file (can be deleted)
- `main.log` - Compilation log (useful for debugging)
- `main.toc` - Table of contents data (can be deleted)
- `main.out` - Hyperref data (can be deleted)

## Clean Build

To remove all build artifacts:

```bash
rm -f main.aux main.log main.out main.toc main.pdf
```

Or use the compile script which cleans automatically.

## HTML Conversion

To convert to HTML for web deployment:

```bash
# Using pandoc
pandoc main.tex -o main.html --mathjax

# Or use a dedicated LaTeX to HTML converter
make4ht main.tex
```

Note: HTML conversion may require additional setup and post-processing for optimal results.

## Continuous Build

For development, you can use `latexmk` for automatic recompilation:

```bash
# Install latexmk
brew install latexmk  # macOS

# Watch and auto-compile
latexmk -pdf -pvc main.tex
```

This will watch for file changes and automatically recompile.

## Checking Output

### Page Count
```bash
pdfinfo main.pdf | grep Pages
```

### File Size
```bash
ls -lh main.pdf
```

### View PDF
```bash
open main.pdf  # macOS
xdg-open main.pdf  # Linux
```

## Production Build Checklist

Before final release:
- [ ] All chapters included in `main.tex`
- [ ] All diagrams present in `chapters/diagrams/`
- [ ] Bibliography file (`references.bib`) complete
- [ ] No compilation warnings
- [ ] Page count ~100 pages
- [ ] All cross-references working
- [ ] Table of contents accurate
- [ ] Hyperlinks functional
- [ ] PDF metadata correct (title, author)

## Performance Tips

- **First build**: May take 2-3 minutes (SVG conversion)
- **Subsequent builds**: 30-60 seconds
- **Use PDF diagrams**: Convert SVGs once, compile faster
- **Parallel compilation**: Use `latexmk -pdf -pvc` for development

## Getting Help

If you encounter issues:
1. Check `main.log` for error messages
2. Verify all prerequisites are installed
3. Try a clean build: `rm -f *.aux *.log *.out *.toc && ./compile.sh`
4. Check that all diagram files exist in `chapters/diagrams/`
