# Conversion Script Changes for Multi-Book Support

## Overview

This document explains the changes needed to `convert_to_html.py` to support converting both books with the same script.

## Current Script

**File**: `html-build/convert_to_html.py`

- Hardcoded chapter list
- Hardcoded source directory (`chapters/`)
- Hardcoded output directories
- Single book only

## New Script

**File**: `html-build/convert_to_html_multi.py`

- Book configurations with metadata
- Command-line arguments
- Multiple source directories
- Book-specific output subdirectories

## Key Changes Needed

### 1. Make Functions Accept Parameters

Current functions are hardcoded. Need to parameterize them:

#### Before:
```python
def create_chapter_html(chapter_file, chapter_title, prev_chapter=None, next_chapter=None, output_dirs=None):
    # Hardcoded source
    latex_path = project_root / "chapters" / f"{chapter_file}.tex"
    
    # Hardcoded output
    for output_dir in output_dirs:
        output_path = output_dir / f"{chapter_file}.html"
```

#### After:
```python
def create_chapter_html(chapter_file, chapter_title, source_dir, output_dir, 
                       prev_chapter=None, next_chapter=None):
    # Parameterized source
    latex_path = project_root / source_dir / f"{chapter_file}.tex"
    
    # Parameterized output with book subdirectory
    output_path = output_dir / f"{chapter_file}.html"
```

### 2. Add Book Configuration

```python
BOOKS = {
    'deeptech': {
        'title': 'Deep Learning and Transformers',
        'subtitle': 'A Graduate-Level Course',
        'source_dir': 'chapters',
        'output_subdir': 'deeptech',
        'chapters': [
            ("preface", "Preface"),
            ("notation", "Notation and Conventions"),
            # ... 34 chapters total
        ]
    },
    'leadership': {
        'title': 'Deep Learning and LLMs for Technical Leaders',
        'subtitle': 'Strategic Guide for Engineering Leadership',
        'source_dir': 'leadership-book/chapters',
        'output_subdir': 'leadership',
        'chapters': [
            ("preface", "Preface"),
            ("chapter01_linear_algebra", "Chapter 1: Linear Algebra Essentials"),
            # ... 17 chapters + 4 bridges
        ]
    }
}
```

### 3. Add Command-Line Arguments

```python
import argparse

def main():
    parser = argparse.ArgumentParser(description='Convert LaTeX textbooks to HTML')
    parser.add_argument('--book', 
                       choices=['deeptech', 'leadership', 'all'], 
                       default='all',
                       help='Which book to convert (default: all)')
    parser.add_argument('--output-base', 
                       default='nodejs-version/public/chapters',
                       help='Base output directory')
    
    args = parser.parse_args()
```

### 4. Update Main Conversion Loop

```python
def main():
    # ... argument parsing ...
    
    # Determine which books to convert
    books_to_convert = []
    if args.book == 'all':
        books_to_convert = list(BOOKS.keys())
    else:
        books_to_convert = [args.book]
    
    project_root = Path(__file__).parent.parent
    
    for book_id in books_to_convert:
        config = get_book_config(book_id)
        
        print(f"\n📚 Converting: {config['title']}")
        
        # Define output directory for this book
        output_dir = project_root / args.output_base / config['output_subdir']
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Define source directory
        source_dir = project_root / config['source_dir']
        
        # Convert each chapter
        for i, (chapter_file, chapter_title) in enumerate(config['chapters']):
            prev_chapter = config['chapters'][i-1] if i > 0 else None
            next_chapter = config['chapters'][i+1] if i < len(config['chapters'])-1 else None
            
            create_chapter_html(
                chapter_file, 
                chapter_title,
                source_dir=config['source_dir'],
                output_dir=output_dir,
                prev_chapter=prev_chapter,
                next_chapter=next_chapter
            )
```

### 5. Update TikZ Diagram Processing

TikZ diagrams should be saved to book-specific diagram directories:

```python
def process_tikz_diagrams(latex_content, chapter_name, output_dir, book_id):
    """Extract and convert all TikZ diagrams in the content"""
    
    # Create diagrams directory for this book
    diagrams_dir = output_dir / "diagrams"
    diagrams_dir.mkdir(parents=True, exist_ok=True)
    
    # ... rest of logic ...
    
    # Save with book-specific path
    svg_filename = f"{book_id}_{chapter_name}_{diagram_hash}.svg"
```

### 6. Update HTML Template

The generated HTML should reference the correct paths:

```python
def create_chapter_html(...):
    # ... conversion logic ...
    
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{chapter_title} - {book_config['title']}</title>
    <link rel="stylesheet" href="../../styles.css">
    <!-- Note: Go up two levels from chapters/bookid/ to reach styles.css -->
    
    <!-- MathJax config -->
    ...
</head>
<body>
    <nav>
        <a href="../../book-selector.html">🏠 Home</a>
        <!-- Book-specific navigation -->
    </nav>
    
    <main>
        {html_content}
    </main>
</body>
</html>
"""
```

## Implementation Steps

### Step 1: Create New Script File

```bash
cp html-build/convert_to_html.py html-build/convert_to_html_multi.py
```

### Step 2: Add Book Configurations

Add the `BOOKS` dictionary at the top of the file.

### Step 3: Add Argument Parsing

Import `argparse` and add command-line argument handling.

### Step 4: Refactor Functions

Update all functions to accept source/output directories as parameters:
- `create_chapter_html()`
- `process_tikz_diagrams()`
- `read_latex_file()`
- Any other functions that reference paths

### Step 5: Update Main Loop

Modify `main()` to iterate over selected books and call conversion functions with book-specific parameters.

### Step 6: Test Conversion

```bash
# Test with one book first
python3 html-build/convert_to_html_multi.py --book deeptech

# Check output
ls -la nodejs-version/public/chapters/deeptech/

# Test with leadership book
python3 html-build/convert_to_html_multi.py --book leadership

# Check output
ls -la nodejs-version/public/chapters/leadership/

# Convert both
python3 html-build/convert_to_html_multi.py --book all
```

## Alternative Approach: Modify Existing Script

Instead of creating a new script, you could modify the existing one:

### Option A: Add Book Parameter to Existing Script

```python
# In convert_to_html.py

# Add at top
BOOK_CONFIGS = { ... }

# Modify main()
def main(book_id='deeptech'):
    config = BOOK_CONFIGS[book_id]
    CHAPTERS = config['chapters']
    source_dir = config['source_dir']
    # ... rest of logic
```

### Option B: Create Wrapper Script

```python
# In html-build/convert_both_books.py

import subprocess

books = ['deeptech', 'leadership']

for book in books:
    print(f"Converting {book}...")
    subprocess.run([
        'python3', 
        'html-build/convert_to_html.py',
        '--book', book
    ])
```

## Recommended Approach

**Create `convert_to_html_multi.py`** (new script) because:

1. Keeps original script intact (backward compatible)
2. Cleaner separation of concerns
3. Easier to test without breaking existing workflow
4. Can import functions from original script if needed

## Testing Checklist

After implementing changes:

- [ ] Script runs without errors
- [ ] Deep tech book converts successfully
- [ ] Leadership book converts successfully
- [ ] HTML files in correct subdirectories
- [ ] TikZ diagrams convert and save correctly
- [ ] Math renders correctly in generated HTML
- [ ] Navigation links work
- [ ] CSS paths correct (../../styles.css)
- [ ] Both books can be converted with `--book all`

## Usage Examples

```bash
# Convert only deep tech book
python3 html-build/convert_to_html_multi.py --book deeptech

# Convert only leadership book
python3 html-build/convert_to_html_multi.py --book leadership

# Convert both books
python3 html-build/convert_to_html_multi.py --book all

# Specify custom output directory
python3 html-build/convert_to_html_multi.py --book all --output-base docs/chapters

# Help
python3 html-build/convert_to_html_multi.py --help
```

## Troubleshooting

### Issue: Source files not found

**Check:**
- Source directory path in book config
- File exists: `leadership-book/chapters/chapter01_linear_algebra.tex`
- Working directory when running script

### Issue: Output files in wrong location

**Check:**
- Output base directory argument
- Book subdirectory in config
- Directory creation logic

### Issue: CSS not loading in generated HTML

**Check:**
- Relative path from chapter HTML to styles.css
- Should be: `../../styles.css` (up two levels from `chapters/bookid/`)

### Issue: TikZ diagrams not converting

**Check:**
- pdflatex installed
- pdf2svg or ImageMagick installed
- Diagram directory creation logic
- File permissions

## Next Steps

1. Review this document
2. Choose implementation approach
3. Implement changes to conversion script
4. Test with one book
5. Test with both books
6. Integrate into deployment workflow
