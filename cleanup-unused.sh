#!/bin/bash
# Clean up unused files from the repository

set -e

echo "🧹 Cleaning up unused files..."
echo ""
echo "⚠️  This will remove old scripts and documentation files."
echo "Press Ctrl+C to cancel, or Enter to continue..."
read

# Remove old fix scripts
echo "Removing old fix scripts..."
rm -f fix_algorithms.py fix_algorithms_clean.py fix_algorithms_final.py fix_algorithms_v2.py remove_roi_content.py
echo "  ✓ Old Python scripts removed"

# Remove test files
echo "Removing test files..."
rm -f test_chapters.js
echo "  ✓ Test files removed"

# Remove old documentation
echo "Removing old documentation..."
rm -f ALGORITHM_FIX_SUMMARY.md BUILD_SYSTEM_FIXED.md CONVERSION_COMPLETE.md
rm -f DEPLOYMENT_STATUS.md HTML_DEPLOYMENT_STRUCTURE.md RENDERING_SYNC_SUMMARY.md
rm -f SOLUTIONS_GUIDE.md UPDATES_IMPLEMENTED.md
echo "  ✓ Old documentation removed"

# Remove LaTeX auxiliary files
echo "Removing LaTeX auxiliary files..."
rm -f *.aux *.log *.out *.toc texput.* test_part4.* main_simple.* main_pro_test.pdf
rm -f chapters/*.aux
echo "  ✓ LaTeX auxiliary files removed"

# Remove cleanup list
rm -f .cleanup-list.txt

echo ""
echo "✅ Cleanup complete!"
echo ""
echo "📊 Kept important files:"
echo "  • main_pro.pdf (final PDF)"
echo "  • main_pro.tex (LaTeX source)"
echo "  • chapters/*.tex (chapter sources)"
echo "  • chapters/*.html (deployed HTML)"
echo "  • app.js, index.html, styles.css (deployed web app)"
echo "  • nodejs-version/ (development version)"
echo "  • html-build/ (build tools)"
echo ""
echo "🚀 Repository is now cleaner!"
