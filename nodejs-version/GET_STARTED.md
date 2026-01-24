# Getting Started in 5 Minutes

## Prerequisites Check

Do you have Node.js installed?

```bash
node --version
```

If you see a version number (14.0.0 or higher), you're good to go! 

If not, download from [nodejs.org](https://nodejs.org/)

## Step 1: Navigate to the Directory

```bash
cd nodejs-version
```

## Step 2: Install Dependencies

```bash
npm install
```

This will take about 10-30 seconds.

## Step 3: Start the Server

**Option A: Quick Start (Easiest)**
```bash
./start.sh
```

**Option B: Manual Start**
```bash
npm start
```

**Option C: Development Mode (Auto-reload)**
```bash
npm run dev
```

## Step 4: Open Your Browser

Navigate to: **http://localhost:3000**

That's it! You should see the textbook interface.

## First Steps in the App

1. **Browse Chapters**: Click any chapter in the left sidebar
2. **Search**: Type in the search box to filter chapters
3. **Toggle Dark Mode**: Click the 🌙 icon
4. **Navigate**: Use the ← → arrow keys on your keyboard
5. **View TOC**: Click the 📑 button to see chapter sections

## Keyboard Shortcuts

- `←` Previous chapter
- `→` Next chapter
- `Esc` Close TOC overlay

## Troubleshooting

### "Port 3000 is already in use"

Use a different port:
```bash
PORT=8080 npm start
```

Then open: http://localhost:8080

### "npm: command not found"

You need to install Node.js first:
- Download from [nodejs.org](https://nodejs.org/)
- Install it
- Restart your terminal
- Try again

### "Cannot find module 'express'"

Run the install command:
```bash
npm install
```

### Chapters not loading

Make sure you're in the `nodejs-version` directory and that the parent directory contains `docs/chapters/` with HTML files.

## What's Next?

### Learn More
- Read [README.md](README.md) for full documentation
- Check [FEATURES.md](FEATURES.md) for all features
- See [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for tips

### Customize
- Edit `public/styles.css` to change colors
- Modify `public/app.js` to add features
- Update `server.js` to change API behavior

### Deploy
- See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- Deploy to Heroku, Vercel, or any Node.js host

## Quick Tips

1. **Bookmark chapters**: Each chapter has a unique URL you can bookmark
2. **Share links**: Copy the URL to share a specific chapter
3. **Use keyboard shortcuts**: Much faster than clicking
4. **Try dark mode**: Great for reading at night
5. **Mobile friendly**: Works great on phones and tablets

## Need Help?

1. Check the documentation files in this directory
2. Review the code comments
3. Test locally before deploying
4. Open an issue on GitHub

## Common Tasks

### Change the port
```bash
PORT=8080 npm start
```

### Stop the server
Press `Ctrl+C` in the terminal

### Restart the server
```bash
npm start
```

### Update dependencies
```bash
npm update
```

### Check for security issues
```bash
npm audit
```

## Success!

If you can see the textbook in your browser, you're all set! 

Enjoy reading the Deep Learning and Transformers textbook in this modern, fast, and beautiful interface.

---

**Time to get started: < 5 minutes**
**Difficulty: Easy**
**Requirements: Node.js 14+**
