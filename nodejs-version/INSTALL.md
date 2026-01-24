# Installation & Setup Guide

## Prerequisites

- **Node.js** version 14.0.0 or higher
- **npm** (comes with Node.js)

### Check if Node.js is installed

```bash
node --version
npm --version
```

If not installed, download from [nodejs.org](https://nodejs.org/)

## Installation Steps

### 1. Navigate to the nodejs-version directory

```bash
cd nodejs-version
```

### 2. Install dependencies

```bash
npm install
```

This will install:
- `express` - Fast web server
- `compression` - Gzip compression for faster loading
- `nodemon` - Auto-reload during development (dev only)

### 3. Start the application

**Option A: Quick Start (Recommended)**

```bash
./start.sh
```

**Option B: Production Mode**

```bash
npm start
```

**Option C: Development Mode (with auto-reload)**

```bash
npm run dev
```

### 4. Open in browser

Navigate to: **http://localhost:3000**

## Troubleshooting

### Port already in use

If port 3000 is already in use, specify a different port:

```bash
PORT=8080 npm start
```

### Permission denied on start.sh

Make the script executable:

```bash
chmod +x start.sh
```

### Dependencies not installing

Clear npm cache and try again:

```bash
npm cache clean --force
npm install
```

### Chapter content not loading

Make sure you're running the server from the `nodejs-version` directory and that the parent directory contains the `docs/chapters/` folder with HTML files.

## Features Overview

### 🎨 Dark Mode
Click the moon/sun icon in the sidebar to toggle between light and dark themes. Your preference is saved automatically.

### 🔍 Search
Type in the search box to filter chapters by title. Search is instant and case-insensitive.

### ⌨️ Keyboard Shortcuts
- **← Left Arrow**: Previous chapter
- **→ Right Arrow**: Next chapter

### 📱 Mobile Support
- Tap the ☰ button to show/hide the sidebar
- Swipe-friendly navigation
- Responsive layout adapts to screen size

### 🔗 Shareable Links
Each chapter has a unique URL (e.g., `#chapter01_linear_algebra`). Share links to specific chapters!

## Performance Features

- **Gzip Compression**: All content is compressed for faster loading
- **Lazy Loading**: Chapters load only when requested
- **Caching**: Static assets cached for optimal performance
- **Smooth Scrolling**: Hardware-accelerated animations
- **Optimized Math Rendering**: MathJax loads asynchronously

## Customization

### Change Theme Colors

Edit `public/styles.css` and modify the CSS variables:

```css
:root {
    --primary-color: #003366;
    --accent-color: #0066cc;
    /* ... more colors ... */
}
```

### Change Port

Set the PORT environment variable:

```bash
export PORT=8080
npm start
```

Or edit `server.js` and change the default port.

## Production Deployment

### Deploy to Heroku

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Deploy
git push heroku main

# Open
heroku open
```

### Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Deploy to any Node.js host

1. Upload the `nodejs-version` folder
2. Run `npm install --production`
3. Start with `npm start`
4. Configure your web server to proxy to the Node.js port

## System Requirements

- **RAM**: 256MB minimum
- **Disk**: 50MB for application + dependencies
- **CPU**: Any modern processor
- **Browser**: Chrome, Firefox, Safari, Edge (latest versions)

## Support

For issues or questions:
1. Check this guide first
2. Review the main README.md
3. Check the GitHub repository issues
4. Ensure all dependencies are installed correctly

## License

Same as the main textbook project.
