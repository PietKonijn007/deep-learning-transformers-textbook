#!/bin/bash
# Sync nodejs-version/public files to root for Vercel deployment

set -e  # Exit on error

echo "🔄 Syncing nodejs-version/public to root directory..."
echo ""

# Sync core application files
echo "📦 Syncing core files..."
cp nodejs-version/public/app.js app.js
echo "  ✓ app.js"

cp nodejs-version/public/index.html index.html
echo "  ✓ index.html"

cp nodejs-version/public/styles.css styles.css
echo "  ✓ styles.css"

# Sync chapters to nodejs-version first (from source)
echo ""
echo "📚 Syncing chapters from source to nodejs-version..."
cp chapters/*.html nodejs-version/public/chapters/ 2>/dev/null || echo "  ⚠ No HTML files in chapters/ to sync"

# Count files
APP_SIZE=$(wc -l < app.js | tr -d ' ')
CHAPTERS_COUNT=$(ls -1 chapters/*.html 2>/dev/null | wc -l | tr -d ' ')
CHAPTERS_IN_APP=$(grep -c "id: 'chapter" app.js || echo "0")

echo ""
echo "✅ Sync complete!"
echo ""
echo "📊 Summary:"
echo "  • app.js: $APP_SIZE lines"
echo "  • Chapters in app.js: $CHAPTERS_IN_APP"
echo "  • HTML chapters: $CHAPTERS_COUNT files"
echo ""
echo "🚀 Ready to commit and deploy!"
echo ""
echo "Next steps:"
echo "  git add app.js index.html styles.css chapters/"
echo "  git commit -m 'Sync updated files to root'"
echo "  git push"
