# Multi-Book Architecture

## Overview

This document describes the architecture changes to support serving both the Deep Tech book and the Leadership book from a single Node.js application.

## Architecture Changes

### 1. Landing Page (`book-selector.html`)

**New file**: `public/book-selector.html`

- Serves as the main entry point
- Presents users with two book options:
  - **Deep Learning & Transformers**: Technical Deep Dive (34 chapters)
  - **Deep Learning & LLMs for Technical Leaders**: Strategic Guide (17 chapters)
- Modern card-based design with hover effects
- Links to `deeptech.html` and `leadership.html`

### 2. Book-Specific Apps

**Rename existing files**:
- `index.html` → `deeptech.html`
- `app.js` → `deeptech-app.js`

**Create new files**:
- `leadership.html` (similar structure to deeptech.html)
- `leadership-app.js` (adapted for leadership chapters)

### 3. Directory Structure

```
nodejs-version/
├── public/
│   ├── book-selector.html          # NEW: Landing page
│   ├── deeptech.html                # RENAMED from index.html
│   ├── deeptech-app.js              # RENAMED from app.js
│   ├── leadership.html              # NEW: Leadership book app
│   ├── leadership-app.js            # NEW: Leadership book logic
│   ├── styles.css                   # SHARED: Same styles for both
│   └── chapters/
│       ├── deeptech/                # NEW: Deep tech chapters
│       │   ├── preface.html
│       │   ├── chapter01_linear_algebra.html
│       │   └── ... (34 chapters total)
│       └── leadership/              # NEW: Leadership chapters
│           ├── preface.html
│           ├── chapter01_linear_algebra.html
│           ├── bridge_I_to_II.html
│           └── ... (17 chapters + bridges)
```

### 4. Server API Changes

**Updated `server.js`**:

#### New Endpoint: `/api/books`
Returns list of available books:
```json
[
  {
    "id": "deeptech",
    "title": "Deep Learning and Transformers",
    "subtitle": "Technical Deep Dive",
    "description": "...",
    "chapterCount": 34,
    "parts": 10
  },
  {
    "id": "leadership",
    "title": "Deep Learning and LLMs for Technical Leaders",
    "subtitle": "Strategic Guide for Engineering Leadership",
    "description": "...",
    "chapterCount": 17,
    "parts": 5
  }
]
```

#### Updated Endpoint: `/api/chapters/:bookId`
- Changed from `/api/chapters` to `/api/chapters/:bookId`
- Returns chapter list for specific book
- Supports both `deeptech` and `leadership`

#### Updated Endpoint: `/api/chapter/:bookId/:chapterId`
- Changed from `/api/chapter/:id` to `/api/chapter/:bookId/:chapterId`
- Fetches chapter content from book-specific subdirectory
- Example: `/api/chapter/deeptech/chapter01_linear_algebra`

### 5. HTML Conversion Script

**New file**: `html-build/convert_to_html_multi.py`

Features:
- Command-line argument to specify which book to convert
- Book configurations with source and output directories
- Supports: `--book deeptech`, `--book leadership`, or `--book all`
- Generates HTML to book-specific subdirectories

Book configurations:
```python
BOOKS = {
    'deeptech': {
        'source_dir': 'chapters',
        'output_subdir': 'deeptech',
        'chapters': [...]  # 34 chapters
    },
    'leadership': {
        'source_dir': 'leadership-book/chapters',
        'output_subdir': 'leadership',
        'chapters': [...]  # 17 chapters + bridges
    }
}
```

Usage:
```bash
# Convert both books
python3 html-build/convert_to_html_multi.py --book all

# Convert only deep tech book
python3 html-build/convert_to_html_multi.py --book deeptech

# Convert only leadership book
python3 html-build/convert_to_html_multi.py --book leadership
```

## Implementation Steps

### Step 1: Update Server
✅ Modified `server.js` with multi-book API endpoints

### Step 2: Create Landing Page
✅ Created `book-selector.html` with book selection UI

### Step 3: Rename Existing Files
- [ ] Rename `public/index.html` → `public/deeptech.html`
- [ ] Rename `public/app.js` → `public/deeptech-app.js`
- [ ] Update script reference in `deeptech.html`

### Step 4: Create Leadership App
- [ ] Copy `deeptech.html` → `leadership.html`
- [ ] Copy `deeptech-app.js` → `leadership-app.js`
- [ ] Update book-specific references (title, API calls, etc.)

### Step 5: Update Conversion Script
- [ ] Complete `convert_to_html_multi.py` implementation
- [ ] Import conversion functions from original script
- [ ] Test conversion for both books

### Step 6: Convert Both Books
- [ ] Run conversion script for deep tech book
- [ ] Run conversion script for leadership book
- [ ] Verify generated HTML files

### Step 7: Update Routing
- [ ] Update `vercel.json` to serve `book-selector.html` as index
- [ ] Test all routes locally
- [ ] Deploy to Vercel

## Shared Resources

The following resources are shared between both books:
- `styles.css` - Same styling for consistent look
- MathJax configuration - Same math rendering
- Navigation components - Similar UI patterns
- Diagram directories - Can be shared or separate

## Benefits

1. **Single Deployment**: One app serves both books
2. **Shared Infrastructure**: Common styling, MathJax, server logic
3. **Easy Navigation**: Users can switch between books
4. **Maintainable**: Clear separation of book-specific content
5. **Scalable**: Easy to add more books in the future

## Future Enhancements

1. **Cross-Book Links**: Link related chapters between books
2. **Progress Tracking**: Track reading progress per book
3. **Search**: Search across both books or within one
4. **Comparison View**: Side-by-side chapter comparison
5. **Unified TOC**: Combined table of contents with filters

## Testing Checklist

- [ ] Landing page loads correctly
- [ ] Both book apps load correctly
- [ ] Chapter navigation works in both books
- [ ] API endpoints return correct data
- [ ] MathJax renders in both books
- [ ] Mobile responsive design works
- [ ] Dark mode works (if implemented)
- [ ] PDF downloads work for both books
- [ ] GitHub links point to correct locations

## Deployment Notes

1. Ensure all HTML files are generated before deployment
2. Update Vercel configuration to serve `book-selector.html` as root
3. Test all routes after deployment
4. Update README with new structure
5. Update documentation links
