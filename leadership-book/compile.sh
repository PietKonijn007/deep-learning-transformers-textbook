#!/bin/bash

# Compile script for Leadership Book
# This script compiles the LaTeX source to PDF

echo "================================================"
echo "Compiling Leadership Book"
echo "================================================"
echo ""

# Check if pdflatex is available
if ! command -v pdflatex &> /dev/null; then
    echo "Error: pdflatex not found. Please install a LaTeX distribution."
    echo "  macOS: brew install --cask mactex"
    echo "  Ubuntu: sudo apt-get install texlive-full"
    exit 1
fi

# Check if Inkscape is available for SVG conversion (optional but recommended)
if ! command -v inkscape &> /dev/null; then
    echo "Warning: Inkscape not found. SVG diagrams may not render optimally."
    echo "  Install: brew install inkscape (macOS) or sudo apt-get install inkscape (Ubuntu)"
    echo "  Continuing anyway..."
    echo ""
fi

# Clean previous build artifacts
echo "Cleaning previous build..."
rm -f main.aux main.log main.out main.toc main.pdf

# First pass
echo "Running pdflatex (first pass)..."
pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Error in first pass. Check main.log for details."
    tail -20 main.log
    exit 1
fi

# Run bibtex if references exist
if [ -f "references.bib" ]; then
    echo "Running bibtex..."
    bibtex main > /dev/null 2>&1
fi

# Second pass
echo "Running pdflatex (second pass)..."
pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1

# Third pass (for references)
echo "Running pdflatex (third pass)..."
pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1

if [ -f "main.pdf" ]; then
    echo ""
    echo "================================================"
    echo "✓ Success! PDF generated: main.pdf"
    echo "================================================"
    
    # Show file size
    SIZE=$(du -h main.pdf | cut -f1)
    echo "File size: $SIZE"
    
    # Count pages
    if command -v pdfinfo &> /dev/null; then
        PAGES=$(pdfinfo main.pdf | grep Pages | awk '{print $2}')
        echo "Pages: $PAGES"
    fi
    
    echo ""
    echo "To view: open main.pdf"
else
    echo ""
    echo "================================================"
    echo "✗ Error: PDF not generated"
    echo "================================================"
    echo "Check main.log for errors:"
    tail -30 main.log
    exit 1
fi
