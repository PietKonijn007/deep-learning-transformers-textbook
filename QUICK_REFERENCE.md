# Quick Reference Card

## 📄 Print-Ready PDF

**File**: `main_pro_memoir.pdf`  
**Status**: ✅ Ready for Lulu upload  
**Format**: A5 with bleed (6.08" × 8.52")  
**Pages**: 773  
**Size**: 2.6 MB

## 🚀 Quick Actions

### Upload to Lulu
1. Go to [Lulu.com](https://www.lulu.com)
2. Create New Project → Trade Book → A5
3. Upload `main_pro_memoir.pdf`
4. Follow Lulu's wizard

### Verify Compliance
```bash
./verify_lulu_compliance.sh
```

### Recompile PDF
```bash
pdflatex -interaction=nonstopmode main_pro_memoir.tex
```

### Check PDF Info
```bash
pdfinfo main_pro_memoir.pdf
```

## 📐 Specifications

| Item | Value |
|------|-------|
| Trim Size | 5.83" × 8.27" (A5) |
| Stock Size | 6.08" × 8.52" (with bleed) |
| Bleed | 0.125" all sides |
| Inner Margin | 1.25" (with 0.75" gutter) |
| Outer Margin | 0.7" |
| Top Margin | 0.7" |
| Bottom Margin | 0.8" |
| Layout | Double-sided (twoside) |

## 📋 Checklist

- [x] Double-sided layout configured
- [x] Bleed added (0.125" all sides)
- [x] Gutter margins set (0.75" for 700+ pages)
- [x] All fonts embedded (50/50)
- [x] Vector graphics used
- [x] Page size correct (437.76 × 613.44 pts)
- [x] PDF version compatible (1.7)
- [x] File size under limit (2.6 MB)
- [ ] Visual inspection completed
- [ ] Test print ordered

## 📚 Documentation

- `PRINT_READY_SUMMARY.md` - Overview and next steps
- `LULU_PRINT_READY.md` - Technical details
- `LAYOUT_COMPARISON.md` - Before/after comparison
- `verify_lulu_compliance.sh` - Automated checks

## 🔧 Configuration File

**Source**: `main_pro_memoir.tex`

Key settings:
```latex
\documentclass[10pt,twoside,a5paper]{memoir}
\setstocksize{8.52in}{6.08in}           % Stock with bleed
\settrimmedsize{8.27in}{5.83in}{*}      % A5 trim
\settrims{0.125in}{0.125in}             % Bleed
\setlrmarginsandblock{1.25in}{0.7in}{*} % Inner/outer
\setulmarginsandblock{0.7in}{0.8in}{*}  % Top/bottom
```

## ⚠️ Important Notes

1. **Gutter alternates**: Left on odd pages, right on even pages
2. **Page count increased**: From 696 to 773 (11% increase)
3. **No manual changes needed**: PDF is ready as-is
4. **Proof copy recommended**: Order one before full production

## 🆘 Troubleshooting

**Lulu rejects PDF?**
- Check error message from Lulu
- Run `./verify_lulu_compliance.sh`
- Verify page size: `pdfinfo main_pro_memoir.pdf`

**Need to revert?**
- Change line 1: `\documentclass[10pt,oneside,a5paper]{memoir}`
- Replace margin settings with symmetric layout
- See `LULU_PRINT_READY.md` for details

**Compilation errors?**
- Check `main_pro_memoir.log`
- Ensure all chapter files exist
- Verify LaTeX packages installed

## 📞 Support

- **Lulu Help**: https://help.lulu.com
- **Book Creation Guide**: https://help.lulu.com/en/support/solutions/articles/64000234733
- **LaTeX Issues**: Check `.log` file

---

**Last Updated**: February 8, 2026  
**Version**: Print-ready with double-sided layout and bleed
