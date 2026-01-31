# Quick Maintenance Guide

## Adding a New Chapter

### 1. Create LaTeX Source
```bash
vim chapters/chapter35_new_topic.tex
```

### 2. Update Conversion Script
Edit `html-build/convert_to_html.py`:
```python
CHAPTERS = [
    # ... existing chapters ...
    ("chapter35_new_topic", "Chapter 35: New Topic"),
]
```

### 3. Generate HTML (Automatically Updates All Locations)
```bash
python3 html-build/convert_to_html.py
```

This single command:
- ✅ Converts TEX to HTML
- ✅ Updates `chapters/` (Vercel deployment)
- ✅ Updates `nodejs-version/public/chapters/` (Node.js dev)
- ✅ Updates `docs/chapters/` (GitHub Pages)
- ✅ Copies TEX source to `docs/chapters/`
- ✅ Fixes algorithm formatting

### 4. Update Chapter Lists in App
Edit `nodejs-version/public/app.js`:
```javascript
state.chapters = [
    // ... existing chapters ...
    { id: 'chapter35_new_topic', title: 'Chapter 35: New Topic', part: 'Part XI: New Section' },
];
```

### 5. Sync App Files to Root
```bash
cp nodejs-version/public/app.js app.js
cp nodejs-version/public/index.html index.html
cp nodejs-version/public/styles.css styles.css
```

Or use the sync script:
```bash
./sync-to-root.sh
```

### 6. Commit and Deploy
```bash
git add .
git commit -m "Add chapter 35: New Topic"
git push
```

## Updating Existing Chapter Content

### Update Chapter Content
```bash
# 1. Edit LaTeX source
vim chapters/chapter01_linear_algebra.tex

# 2. Regenerate HTML (updates all locations automatically)
python3 html-build/convert_to_html.py

# 3. Commit
git add chapters/chapter01_linear_algebra.*
git add nodejs-version/public/chapters/chapter01_linear_algebra.html
git add docs/chapters/chapter01_linear_algebra.*
git commit -m "Update chapter 1 content"
git push
```

## Updating Application Files (app.js, index.html, styles.css)

### Update Styles
```bash
# 1. Edit source
vim nodejs-version/public/styles.css

# 2. Sync to root
cp nodejs-version/public/styles.css styles.css

# 3. Commit
git add styles.css nodejs-version/public/styles.css
git commit -m "Update styles"
git push
```

### Update Application Logic
```bash
# 1. Edit source
vim nodejs-version/public/app.js

# 2. Sync to root
cp nodejs-version/public/app.js app.js

# 3. Commit
git add app.js nodejs-version/public/app.js
git commit -m "Update application logic"
git push
```

## One-Command Workflow

### Regenerate Everything
```bash
# Regenerate all HTML files and update all locations
python3 html-build/convert_to_html.py

# Sync app files to root
./sync-to-root.sh

# Commit everything
git add .
git commit -m "Regenerate all HTML files"
git push
```

## Testing Locally

### Static Server (Matches Production)
```bash
python3 -m http.server 8000
# Open http://localhost:8000
```

### Node.js Server (Development)
```bash
cd nodejs-version
npm start
# Open http://localhost:3000
```

## Troubleshooting

### Menu doesn't show new chapters
```bash
# Check if app.js has the new chapters
grep "chapter35" app.js

# If not, sync from nodejs-version
./sync-to-root.sh
git add app.js
git commit -m "Sync app.js with new chapters"
git push
```

### Styles not updating
```bash
# Sync styles
./sync-to-root.sh
git add styles.css
git commit -m "Update styles"
git push
```

### Chapter content not showing
```bash
# Check if HTML file exists
ls chapters/chapter35_new_topic.html

# If not, regenerate
python3 html-build/convert_to_html.py

# Sync to nodejs-version
cp chapters/*.html nodejs-version/public/chapters/

# Commit
git add chapters/ nodejs-version/public/chapters/
git commit -m "Update chapter HTML files"
git push
```

## File Locations

| Purpose | Source | Deployed |
|---------|--------|----------|
| Application logic | `nodejs-version/public/app.js` | `app.js` |
| Main page | `nodejs-version/public/index.html` | `index.html` |
| Styles | `nodejs-version/public/styles.css` | `styles.css` |
| Chapters | `chapters/*.html` | `chapters/*.html` |

## Important Commands

```bash
# Sync all files to root
./sync-to-root.sh

# Generate HTML from LaTeX
python3 html-build/convert_to_html.py

# Clean up old files
./cleanup-unused.sh

# Test locally
python3 -m http.server 8000

# Check deployment
git log --oneline -5
```

## Deployment Checklist

- [ ] Update LaTeX source in `chapters/`
- [ ] Run `python3 html-build/convert_to_html.py`
- [ ] Update `nodejs-version/public/app.js` if adding chapters
- [ ] Run `./sync-to-root.sh`
- [ ] Test locally with `python3 -m http.server 8000`
- [ ] Commit: `git add . && git commit -m "..."`
- [ ] Push: `git push`
- [ ] Verify at https://deeplearning.hofkensvermeulen.be/

## Getting Help

- **Deployment Architecture:** See [DEPLOYMENT_ARCHITECTURE.md](DEPLOYMENT_ARCHITECTURE.md)
- **Full README:** See [README.md](README.md)
- **Node.js Version:** See [nodejs-version/README.md](nodejs-version/README.md)
