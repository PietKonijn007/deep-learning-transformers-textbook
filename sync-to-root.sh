#!/bin/bash
# Sync multi-book structure from nodejs-version to root for Vercel deployment

set -e  # Exit on error

echo "🔄 Syncing multi-book structure to root for Vercel deployment..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if source directory exists
if [ ! -d "nodejs-version/public" ]; then
    echo -e "${RED}❌ Error: nodejs-version/public directory not found${NC}"
    exit 1
fi

# Copy main HTML files
echo -e "${BLUE}📄 Copying main HTML files...${NC}"
if [ -f "nodejs-version/public/index.html" ]; then
    cp nodejs-version/public/index.html index.html
else
    echo -e "${YELLOW}   ⚠ Warning: index.html not found${NC}"
fi

if [ -f "nodejs-version/public/deeptech.html" ]; then
    cp nodejs-version/public/deeptech.html deeptech.html
else
    echo -e "${YELLOW}   ⚠ Warning: deeptech.html not found${NC}"
fi

if [ -f "nodejs-version/public/leadership.html" ]; then
    cp nodejs-version/public/leadership.html leadership.html
else
    echo -e "${YELLOW}   ⚠ Warning: leadership.html not found${NC}"
fi
echo -e "${GREEN}   ✓ HTML files copied${NC}"

# Copy JavaScript files
echo -e "${BLUE}📜 Copying JavaScript files...${NC}"
if [ -f "nodejs-version/public/deeptech-app.js" ]; then
    cp nodejs-version/public/deeptech-app.js deeptech-app.js
else
    echo -e "${YELLOW}   ⚠ Warning: deeptech-app.js not found${NC}"
fi

if [ -f "nodejs-version/public/leadership-app.js" ]; then
    cp nodejs-version/public/leadership-app.js leadership-app.js
else
    echo -e "${YELLOW}   ⚠ Warning: leadership-app.js not found${NC}"
fi
echo -e "${GREEN}   ✓ JavaScript files copied${NC}"

# Sync chapter directories
echo -e "${BLUE}📚 Syncing chapter directories...${NC}"

# Create chapters directory if it doesn't exist
mkdir -p chapters

# Remove old chapter structure if exists
[ -d "chapters/deeptech" ] && rm -rf chapters/deeptech
[ -d "chapters/leadership" ] && rm -rf chapters/leadership
[ -d "chapters/diagrams" ] && rm -rf chapters/diagrams

# Copy new structure
if [ -d "nodejs-version/public/chapters/deeptech" ]; then
    cp -r nodejs-version/public/chapters/deeptech chapters/
    echo -e "${GREEN}   ✓ Deep tech chapters: $(ls chapters/deeptech/*.html 2>/dev/null | wc -l | tr -d ' ') files${NC}"
else
    echo -e "${YELLOW}   ⚠ Warning: deeptech chapters not found${NC}"
fi

if [ -d "nodejs-version/public/chapters/leadership" ]; then
    cp -r nodejs-version/public/chapters/leadership chapters/
    echo -e "${GREEN}   ✓ Leadership chapters: $(ls chapters/leadership/*.html 2>/dev/null | wc -l | tr -d ' ') files${NC}"
else
    echo -e "${YELLOW}   ⚠ Warning: leadership chapters not found${NC}"
fi

if [ -d "nodejs-version/public/chapters/diagrams" ]; then
    cp -r nodejs-version/public/chapters/diagrams chapters/
    DIAGRAM_COUNT=$(find chapters/diagrams -type f \( -name "*.png" -o -name "*.svg" \) 2>/dev/null | wc -l | tr -d ' ')
    echo -e "${GREEN}   ✓ Diagrams: ${DIAGRAM_COUNT} files${NC}"
else
    echo -e "${YELLOW}   ⚠ Warning: diagrams directory not found${NC}"
fi

echo ""
echo -e "${GREEN}✅ Sync complete!${NC}"
echo ""
echo "Next steps:"
echo "  1. Review changes: git status"
echo "  2. Commit: git add -A && git commit -m 'Sync multi-book structure'"
echo "  3. Push: git push origin main"
