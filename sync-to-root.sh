#!/bin/bash
# Sync multi-book structure from nodejs-version to root for Vercel deployment

set -e  # Exit on error

echo "🔄 Syncing multi-book structure to root for Vercel deployment..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Copy main HTML files
echo -e "${BLUE}📄 Copying main HTML files...${NC}"
cp nodejs-version/public/index.html index.html
cp nodejs-version/public/deeptech.html deeptech.html
cp nodejs-version/public/leadership.html leadership.html
echo -e "${GREEN}   ✓ HTML files copied${NC}"

# Copy JavaScript files
echo -e "${BLUE}📜 Copying JavaScript files...${NC}"
cp nodejs-version/public/deeptech-app.js deeptech-app.js
cp nodejs-version/public/leadership-app.js leadership-app.js
echo -e "${GREEN}   ✓ JavaScript files copied${NC}"

# Sync chapter directories
echo -e "${BLUE}📚 Syncing chapter directories...${NC}"

# Remove old chapter structure if exists
rm -rf chapters/deeptech chapters/leadership chapters/diagrams

# Copy new structure
cp -r nodejs-version/public/chapters/deeptech chapters/deeptech
cp -r nodejs-version/public/chapters/leadership chapters/leadership
cp -r nodejs-version/public/chapters/diagrams chapters/diagrams

echo -e "${GREEN}   ✓ Deep tech chapters: $(ls chapters/deeptech/*.html | wc -l | tr -d ' ') files${NC}"
echo -e "${GREEN}   ✓ Leadership chapters: $(ls chapters/leadership/*.html | wc -l | tr -d ' ') files${NC}"
echo -e "${GREEN}   ✓ Diagrams: $(ls chapters/diagrams/*.{png,svg} 2>/dev/null | wc -l | tr -d ' ') files${NC}"

echo ""
echo -e "${GREEN}✅ Sync complete!${NC}"
echo ""
echo "Next steps:"
echo "  1. Review changes: git status"
echo "  2. Commit: git add -A && git commit -m 'Sync multi-book structure'"
echo "  3. Push: git push origin main"
