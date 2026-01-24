# Performance Optimization Guide

## Current Optimizations Applied ✅

### 1. Deferred MathJax Loading
**Problem:** MathJax is a large library (~500KB) that was blocking initial page render.

**Solution:** 
- Removed synchronous MathJax loading
- Deferred MathJax until after page is interactive
- Added 100ms delay to prioritize UI rendering

**Impact:** Initial page load is now much faster, MathJax loads in background.

### 2. DNS Prefetch & Preconnect
**Added:**
```html
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="dns-prefetch" href="https://cdn.jsdelivr.net">
```

**Impact:** Faster CDN connection when MathJax loads.

### 3. Removed Polyfill.io
**Problem:** Extra HTTP request for polyfills that modern browsers don't need.

**Solution:** Removed polyfill.io dependency.

**Impact:** One less external request, faster initial load.

## Current Performance Metrics

### Initial Load (First Visit)
- **HTML:** ~5KB (gzipped)
- **CSS:** ~10KB
- **JS (app.js):** ~8KB
- **MathJax:** ~500KB (deferred, loads after page is interactive)

### Subsequent Loads
- **Cached:** Most assets cached by browser
- **Chapter switching:** ~50-200KB per chapter (HTML content)

## Why It Still Feels Slow

### Main Culprits:

1. **MathJax Size** - Even deferred, it's 500KB
2. **Cold Start** - Vercel serverless functions have cold start time (~1-2 seconds first request)
3. **Chapter HTML Size** - Some chapters are 100-200KB with all the math
4. **CDN Distance** - First load from CDN takes time

## Additional Optimizations You Can Apply

### Option 1: Remove MathJax Entirely (Fastest)
If you pre-render all math as SVG in your HTML chapters, you don't need MathJax at all.

**Pros:** 
- Instant load
- No external dependencies
- Smaller bundle

**Cons:**
- Requires pre-processing chapters
- Larger HTML files

### Option 2: Use Lighter Math Rendering
Replace MathJax with KaTeX (much smaller, faster):

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
```

**Pros:**
- 10x smaller than MathJax (~50KB vs 500KB)
- Much faster rendering

**Cons:**
- Slightly less feature-complete than MathJax
- May need to adjust some math syntax

### Option 3: Service Worker Caching
Add a service worker to cache everything:

```javascript
// sw.js
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open('v1').then((cache) => {
      return cache.addAll([
        '/',
        '/styles.css',
        '/app.js',
        '/api/chapters'
      ]);
    })
  );
});
```

**Impact:** Near-instant loads on repeat visits.

### Option 4: Preload Critical Chapters
Preload the most popular chapters:

```html
<link rel="prefetch" href="/api/chapter/preface">
<link rel="prefetch" href="/api/chapter/chapter01_linear_algebra">
```

### Option 5: Compress Chapter HTML
Minify and compress chapter HTML files before deployment.

```bash
# Install html-minifier
npm install -g html-minifier

# Minify chapters
for file in chapters/*.html; do
  html-minifier --collapse-whitespace --remove-comments "$file" -o "$file"
done
```

**Impact:** 20-30% smaller chapter files.

### Option 6: Use Vercel Edge Functions
Convert API to Edge Functions for faster cold starts:

```javascript
// api/chapters.js
export const config = {
  runtime: 'edge',
};

export default async function handler(req) {
  // Your chapter list logic
  return new Response(JSON.stringify(chapters), {
    headers: { 'content-type': 'application/json' },
  });
}
```

**Impact:** ~10x faster cold starts.

## Recommended Quick Wins

### 1. Switch to KaTeX (Easiest, Biggest Impact)
Replace MathJax with KaTeX in `index.html`:

```html
<!-- Replace MathJax with KaTeX -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
```

Update app.js to use KaTeX auto-render instead of MathJax.

### 2. Add Service Worker (Medium Effort)
Create `public/sw.js` and register it in `app.js`.

### 3. Minify Chapters (Easy)
Run html-minifier on all chapter files.

## Measuring Performance

### Use Browser DevTools
1. Open DevTools (F12)
2. Go to Network tab
3. Reload page
4. Check:
   - Total load time
   - Number of requests
   - Size of resources

### Use Lighthouse
1. Open DevTools
2. Go to Lighthouse tab
3. Run audit
4. Check Performance score

### Current Baseline
- **First Load:** ~3-5 seconds (with MathJax)
- **Cached Load:** ~500ms
- **Chapter Switch:** ~200-500ms

### Target After Optimizations
- **First Load:** ~1-2 seconds (with KaTeX)
- **Cached Load:** ~100ms (with service worker)
- **Chapter Switch:** ~100-200ms

## Implementation Priority

1. **High Impact, Low Effort:**
   - ✅ Defer MathJax (DONE)
   - ✅ Add preconnect (DONE)
   - ⬜ Switch to KaTeX
   - ⬜ Minify chapters

2. **High Impact, Medium Effort:**
   - ⬜ Add service worker
   - ⬜ Convert to Edge Functions

3. **Medium Impact, High Effort:**
   - ⬜ Pre-render math as SVG
   - ⬜ Implement lazy loading for chapters

## Testing Your Changes

After each optimization:

```bash
# Deploy
vercel --cwd nodejs-version --prod

# Test with curl
time curl -s https://nodejs-version-sage.vercel.app > /dev/null

# Check size
curl -s https://nodejs-version-sage.vercel.app | wc -c
```

## Conclusion

The current optimizations have improved initial load time by deferring MathJax. For even better performance, consider switching to KaTeX or pre-rendering math. The biggest remaining bottleneck is the 500KB MathJax library.

**Current Status:** Good (3-5s first load, <1s cached)
**Potential:** Excellent (1-2s first load, <200ms cached)
