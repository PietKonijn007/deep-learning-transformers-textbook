# Lulu Print-Ready Configuration

## Changes Implemented

### 1. Document Class
- **Changed from**: `oneside` → **to**: `twoside`
- **Purpose**: Enables double-sided printing with alternating gutter margins

### 2. Stock Size (with Bleed)
- **Size**: 6.08" × 8.52" (437.76 × 613.44 pts)
- **Calculation**: A5 (5.83" × 8.27") + 0.125" bleed on all sides
- **Command**: `\setstocksize{8.52in}{6.08in}`

### 3. Trim Size
- **Size**: 5.83" × 8.27" (standard A5)
- **Command**: `\settrimmedsize{8.27in}{5.83in}{*}`

### 4. Trim Marks
- **Bleed**: 0.125" on all sides
- **Command**: `\settrims{0.125in}{0.125in}`

### 5. Margins (Double-Sided with Gutter)
For 696-773 pages, Lulu recommends 0.75" gutter:

- **Inner margin** (binding side): 1.25" (0.5" base + 0.75" gutter)
- **Outer margin**: 0.7" (for readability and chapter numbers)
- **Top margin**: 0.7"
- **Bottom margin**: 0.8"

**Behavior**: 
- Odd pages (right-hand): Inner margin on LEFT (binding side)
- Even pages (left-hand): Inner margin on RIGHT (binding side)

### 6. Current Page Count
- **Pages**: 773 (increased from 696 due to larger inner margin)
- **File size**: 2.69 MB

## Lulu Requirements Checklist

### ✅ Completed
- [x] Double-sided layout (`twoside`)
- [x] Bleed added (0.125" all sides)
- [x] Stock size set to A5 + bleed (6.08" × 8.52")
- [x] Trim size set to A5 (5.83" × 8.27")
- [x] Trim marks configured
- [x] Gutter margins for 700+ pages (0.75")
- [x] Alternating inner/outer margins
- [x] Fonts embedded (Latin Modern, Type 1 format)
- [x] All PNG source images at 300 DPI
- [x] Vector graphics used in PDF (ideal for print)
- [x] PDF version 1.7 (compatible with Lulu)
- [x] File size under limit (2.6 MB)

**Verification Status**: Run `./verify_lulu_compliance.sh` - All automated checks pass ✅

### ⚠️ Needs Manual Verification
- [ ] **Visual inspection**: Open PDF and check:
  - Chapter numbers fit properly on outer margins
  - Text doesn't extend into bleed area (0.125" from edge)
  - Gutter margins look appropriate on facing pages
  - No content cut off at page edges

- [ ] **Test print**: Consider ordering a proof copy from Lulu before full production run

## How to Verify (Automated)

Run the verification script:
```bash
./verify_lulu_compliance.sh
```

This checks:
- Page size with bleed
- Page count limits
- Font embedding
- Image resolution
- PDF version compatibility
- File size limits

## Page Count Impact

The addition of gutter margins increased the page count:
- **Before**: 696 pages (symmetric margins)
- **After**: 773 pages (asymmetric margins with gutter)
- **Increase**: 77 pages (11% increase)

This is expected and acceptable for print production.

## Next Steps

1. **Verify image resolution** (see commands above)
2. **Visual inspection**: Check a few pages to ensure:
   - Chapter numbers fit properly on outer margins
   - Text doesn't extend into bleed area
   - Gutter margins look appropriate
3. **Test print**: Consider ordering a proof copy from Lulu
4. **Final PDF export**: Use `pdflatex` with proper settings (already configured)

## Reverting Changes

If you need to revert to the previous layout:

```latex
% Change line 1:
\documentclass[10pt,oneside,a5paper]{memoir}

% Replace lines 60-73 with:
\setlrmarginsandblock{0.7in}{0.7in}{*}
\setulmarginsandblock{0.7in}{0.8in}{*}
\checkandfixthelayout
```

## Additional Notes

- The current configuration meets Lulu's technical requirements
- Page count increase is normal for double-sided printing with gutter
- All fonts are embedded (Latin Modern Type 1 fonts)
- Hyperlinks are preserved but set to black for print
