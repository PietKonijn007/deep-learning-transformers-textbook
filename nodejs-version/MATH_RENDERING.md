# Math Rendering Guide

## How Math Rendering Works

The Node.js application uses **MathJax 3** to render mathematical equations beautifully in the browser.

## Configuration

### MathJax Setup

The application is configured to recognize:

**Inline Math:**
- `$...$` - Standard inline math
- `\(...\)` - Alternative inline math

**Display Math:**
- `$$...$$` - Display equations
- `\[...\]` - Alternative display equations

### Custom Macros

The following LaTeX macros are pre-configured:

**Sets:**
- `\R` → ℝ (real numbers)
- `\N` → ℕ (natural numbers)
- `\Z` → ℤ (integers)
- `\C` → ℂ (complex numbers)

**Vectors (bold):**
- `\vx` → **x**
- `\vy` → **y**
- `\vz` → **z**
- `\vh` → **h**
- `\vw` → **w**
- `\vb` → **b**
- `\vq` → **q**
- `\vk` → **k**
- `\vv` → **v**

**Matrices (bold):**
- `\mA` → **A**
- `\mB` → **B**
- `\mC` → **C**
- `\mW` → **W**
- `\mX` → **X**
- `\mY` → **Y**
- `\mQ` → **Q**
- `\mK` → **K**
- `\mV` → **V**
- `\mH` → **H**
- `\mI` → **I**
- `\mU` → **U**
- `\mM` → **M**

**Operations:**
- `\transpose` → ᵀ (transpose)
- `\norm{x}` → ||x|| (norm)
- `\abs{x}` → |x| (absolute value)

## Troubleshooting

### Math Not Rendering

**Problem:** Equations appear as raw LaTeX code (e.g., `$\vx \in \R^n$`)

**Solutions:**

1. **Wait for MathJax to Load**
   - MathJax loads asynchronously from a CDN
   - Wait 1-2 seconds after page load
   - Check browser console for "MathJax loaded and ready"

2. **Check Internet Connection**
   - MathJax loads from `cdn.jsdelivr.net`
   - Requires active internet connection
   - Check browser console for network errors

3. **Clear Browser Cache**
   ```
   Chrome: Ctrl+Shift+Delete (Cmd+Shift+Delete on Mac)
   Firefox: Ctrl+Shift+Delete (Cmd+Shift+Delete on Mac)
   Safari: Cmd+Option+E
   ```

4. **Disable Browser Extensions**
   - Some ad blockers may block CDN resources
   - Try disabling extensions temporarily
   - Whitelist `cdn.jsdelivr.net`

5. **Check Browser Console**
   - Open Developer Tools (F12)
   - Look for errors in Console tab
   - Common issues:
     - Network errors (CDN blocked)
     - JavaScript errors (conflicts)
     - CORS errors (rare)

### Slow Math Rendering

**Problem:** Math takes several seconds to render

**Causes:**
- Large chapters with many equations
- Slow internet connection
- Complex equations (matrices, aligned equations)

**Solutions:**
1. Wait for initial load (first chapter is slowest)
2. Subsequent chapters render faster (MathJax cached)
3. Use a faster internet connection
4. Close other browser tabs to free memory

### Math Rendering Errors

**Problem:** Some equations render incorrectly or show errors

**Common Issues:**

1. **Unmatched Delimiters**
   - Ensure every `$` has a matching `$`
   - Check for escaped `\$` in text

2. **Unsupported Commands**
   - Some LaTeX commands may not be supported
   - Check MathJax documentation for supported commands

3. **Nested Environments**
   - Complex nested structures may fail
   - Simplify equation structure if possible

## Performance Tips

### Faster Rendering

1. **Use Modern Browser**
   - Chrome, Firefox, Safari (latest versions)
   - Better JavaScript performance

2. **Enable Hardware Acceleration**
   - Chrome: Settings → Advanced → System → Use hardware acceleration
   - Firefox: Preferences → Performance → Use hardware acceleration

3. **Close Unused Tabs**
   - Free up browser memory
   - Improves rendering speed

4. **Disable Unnecessary Extensions**
   - Reduces browser overhead
   - Faster page loading

### Caching

MathJax caches:
- Font files (first load only)
- Rendered equations (per session)
- Configuration (per session)

After first chapter load, subsequent chapters render much faster.

## Testing Math Rendering

### Quick Test

1. Start the server: `npm start`
2. Open http://localhost:3000
3. Click "Chapter 1: Linear Algebra"
4. Wait 2-3 seconds
5. Check if equations render properly

### Expected Behavior

**Before Rendering:**
```
$\vx \in \R^n$
```

**After Rendering:**
**x** ∈ ℝⁿ (beautifully formatted)

### Console Verification

Open browser console (F12) and look for:
```
MathJax loaded and ready
MathJax rendering complete
```

## Advanced Configuration

### Custom MathJax Settings

Edit `public/index.html` to modify MathJax configuration:

```javascript
window.MathJax = {
    tex: {
        inlineMath: [['$', '$'], ['\\(', '\\)']],
        displayMath: [['$$', '$$'], ['\\[', '\\]']],
        // Add custom macros here
        macros: {
            mycommand: '{\\mathbf{#1}}',
            // ...
        }
    }
};
```

### Offline MathJax

For offline use, download MathJax locally:

1. Download MathJax from https://github.com/mathjax/MathJax/releases
2. Extract to `public/mathjax/`
3. Update `index.html`:
   ```html
   <script src="mathjax/es5/tex-mml-chtml.js"></script>
   ```

## Browser Compatibility

### Supported Browsers

✅ **Chrome/Edge 90+**
- Full support
- Best performance

✅ **Firefox 88+**
- Full support
- Good performance

✅ **Safari 14+**
- Full support
- Good performance

✅ **Mobile Browsers**
- iOS Safari 14+
- Chrome Mobile 90+
- May be slower on older devices

### Unsupported Browsers

❌ **Internet Explorer**
- Not supported
- Use Edge instead

❌ **Very Old Browsers**
- Chrome < 60
- Firefox < 60
- Safari < 12

## Common Math Patterns

### Inline Math
```
The vector $\vx \in \R^n$ has dimension $n$.
```

### Display Math
```
$$
\vh = \mW\vx + \vb
$$
```

### Matrices
```
$$
\mA = \begin{bmatrix}
a_{11} & a_{12} \\
a_{21} & a_{22}
\end{bmatrix}
$$
```

### Aligned Equations
```
$$
\begin{align}
y &= mx + b \\
  &= 2x + 3
\end{align}
$$
```

## Support

If math rendering still doesn't work:

1. Check all troubleshooting steps above
2. Verify internet connection
3. Try a different browser
4. Check browser console for errors
5. Open an issue with:
   - Browser version
   - Console errors
   - Screenshot of problem

## References

- [MathJax Documentation](https://docs.mathjax.org/)
- [LaTeX Math Symbols](https://www.overleaf.com/learn/latex/List_of_Greek_letters_and_math_symbols)
- [MathJax Configuration](https://docs.mathjax.org/en/latest/web/configuration.html)
