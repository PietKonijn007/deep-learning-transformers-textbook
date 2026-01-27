#!/bin/bash
# Build script for Vercel deployment
# Ensures chapter HTML files are accessible to the API

echo "Copying chapter files for Vercel deployment..."

# Create chapters directory in api folder
mkdir -p api/chapters

# Copy all chapter HTML files
cp -r public/chapters/*.html api/chapters/

echo "✓ Chapter files copied to api/chapters/"
echo "Files copied: $(ls api/chapters/*.html | wc -l)"
