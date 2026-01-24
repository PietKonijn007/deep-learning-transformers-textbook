# Social Media Preview Setup

## What Was Added ✅

Your website now has professional social media preview cards for LinkedIn, Twitter, Facebook, and other platforms!

### 1. Open Graph Meta Tags
Added comprehensive Open Graph tags that LinkedIn and Facebook use:
- Title: "Deep Learning and Transformers - Interactive Textbook"
- Description: Comprehensive overview of the textbook
- Image: Custom 1200x630px preview image
- URL: https://deeplearning.hofkensvermeulen.be/

### 2. Twitter Card Meta Tags
Added Twitter-specific tags for beautiful Twitter previews:
- Card type: Large image summary
- Same title, description, and image as Open Graph

### 3. Preview Image (og-image.svg)
Created a professional 1200x630px social media preview image featuring:
- Gradient blue background (brand colors)
- Clear title and subtitle
- Key features highlighted
- Your domain name
- Professional, clean design

### 4. Favicon (favicon.svg)
Added a custom book icon favicon for browser tabs and bookmarks.

### 5. SEO Enhancements
- Author meta tag
- Keywords for search engines
- Canonical URL

## How to Test

### LinkedIn Preview
1. Go to [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/)
2. Enter: `https://deeplearning.hofkensvermeulen.be`
3. Click "Inspect"
4. You should see your preview image, title, and description

**Note:** LinkedIn caches previews. If you don't see the new image:
- Wait 24 hours for cache to clear
- Or use the Post Inspector to force a refresh

### Facebook Preview
1. Go to [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/)
2. Enter: `https://deeplearning.hofkensvermeulen.be`
3. Click "Debug"
4. Click "Scrape Again" to refresh cache

### Twitter Preview
1. Go to [Twitter Card Validator](https://cards-dev.twitter.com/validator)
2. Enter: `https://deeplearning.hofkensvermeulen.be`
3. Click "Preview card"

### Manual Test
View the meta tags directly:
```bash
curl -s https://deeplearning.hofkensvermeulen.be | grep -i "og:"
```

Or view the image:
```
https://deeplearning.hofkensvermeulen.be/og-image.svg
```

## What It Looks Like

When you share your link on LinkedIn, it will show:

```
┌─────────────────────────────────────────────┐
│                                             │
│  [Beautiful gradient image with title]     │
│                                             │
├─────────────────────────────────────────────┤
│ Deep Learning and Transformers -            │
│ Interactive Textbook                        │
│                                             │
│ Comprehensive graduate-level textbook      │
│ covering theory, mathematics, and          │
│ implementation of deep learning and        │
│ transformer architectures. 25 chapters...  │
│                                             │
│ deeplearning.hofkensvermeulen.be           │
└─────────────────────────────────────────────┘
```

## Customizing the Preview Image

If you want to change the preview image:

### Option 1: Edit the SVG
Edit `public/og-image.svg` to change:
- Colors
- Text
- Layout
- Add your photo or logo

### Option 2: Use a PNG/JPG
1. Create a 1200x630px image
2. Save as `public/og-image.png`
3. Update `index.html`:
   ```html
   <meta property="og:image" content="https://deeplearning.hofkensvermeulen.be/og-image.png">
   ```

### Design Tools
- [Canva](https://www.canva.com/) - Easy drag-and-drop
- [Figma](https://www.figma.com/) - Professional design
- [Photopea](https://www.photopea.com/) - Free Photoshop alternative

### Recommended Specs
- **Size:** 1200x630px (required for LinkedIn)
- **Format:** PNG, JPG, or SVG
- **File size:** Under 5MB
- **Aspect ratio:** 1.91:1
- **Text:** Large, readable fonts
- **Colors:** High contrast

## Cache Issues

If LinkedIn doesn't show your new image:

### Solution 1: Wait
LinkedIn caches previews for 7 days. Wait and it will update automatically.

### Solution 2: Force Refresh
1. Use [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/)
2. Enter your URL
3. Click "Inspect" - this forces LinkedIn to re-fetch

### Solution 3: Add Query Parameter
Share with a query parameter to bypass cache:
```
https://deeplearning.hofkensvermeulen.be/?v=2
```

## Verification Checklist

- [x] Open Graph tags added
- [x] Twitter Card tags added
- [x] Preview image created (1200x630px)
- [x] Favicon added
- [x] Meta description optimized
- [x] Canonical URL set
- [x] Author and keywords added

## Testing Checklist

- [ ] Test on LinkedIn Post Inspector
- [ ] Test on Facebook Sharing Debugger
- [ ] Test on Twitter Card Validator
- [ ] Share actual post on LinkedIn to verify
- [ ] Check mobile preview
- [ ] Verify image loads quickly

## Additional Resources

- [Open Graph Protocol](https://ogp.me/)
- [Twitter Cards Documentation](https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/abouts-cards)
- [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/)
- [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/)

## Current URLs

- **Website:** https://deeplearning.hofkensvermeulen.be
- **Preview Image:** https://deeplearning.hofkensvermeulen.be/og-image.svg
- **Favicon:** https://deeplearning.hofkensvermeulen.be/favicon.svg

## Support

If the preview still doesn't show:
1. Check that your domain is properly configured
2. Verify the image URL is accessible
3. Wait 24 hours for cache to clear
4. Use the debugging tools above to force refresh

---

**Your link will now look professional and engaging when shared on social media! 🎉**
