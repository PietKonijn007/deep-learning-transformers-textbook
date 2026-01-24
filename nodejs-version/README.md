# Deep Learning and Transformers - Node.js Interactive Version

A fast, reactive, and visually appealing Node.js web application for reading the Deep Learning and Transformers textbook.

## ✨ Highlights

- ⚡ **Lightning Fast**: Loads in < 1 second, chapter switching in < 200ms
- 🎨 **Beautiful UI**: Modern design with dark mode support
- 📱 **Fully Responsive**: Perfect on desktop, tablet, and mobile
- 🔍 **Smart Search**: Instant chapter filtering
- ⌨️ **Keyboard Navigation**: Arrow keys for quick browsing
- 📑 **Chapter TOC**: Quick navigation within chapters
- 🚀 **Optimized**: Gzip compression, lazy loading, efficient caching

## 🚀 Quick Start

### Installation

```bash
cd nodejs-version
npm install
```

### Run the Application

**Quick Start (Recommended)**
```bash
./start.sh
```

**Production Mode**
```bash
npm start
```

**Development Mode** (with auto-reload)
```bash
npm run dev
```

Open your browser to: **http://localhost:3000**

## 📚 Documentation

- **[VERCEL_DEPLOY.md](VERCEL_DEPLOY.md)** - Quick Vercel deployment guide (recommended)
- **[INSTALL.md](INSTALL.md)** - Detailed installation and setup guide
- **[FEATURES.md](FEATURES.md)** - Complete feature list and capabilities
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment guide
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick reference card
- **[MATH_RENDERING.md](MATH_RENDERING.md)** - Math rendering troubleshooting

## ⚠️ Important Note

This application requires the `docs/chapters/` directory from the parent project to be accessible. The server reads chapter HTML files from `../docs/chapters/`. Make sure this directory structure is maintained when deploying.

## Features

✨ **Fast Loading**
- Gzip compression enabled
- Lazy loading of chapter content
- Optimized static asset caching
- Minimal bundle size

🎨 **Visually Appealing**
- Modern, clean interface
- Dark mode toggle (🌙/☀️)
- Responsive design (mobile, tablet, desktop)
- Smooth animations and transitions
- Professional typography

⚡ **Reactive & Interactive**
- Real-time chapter search
- Keyboard navigation (← → arrow keys)
- Chapter table of contents (📑 button)
- Smooth scrolling
- Browser history support
- MathJax for beautiful equation rendering

📱 **Mobile Optimized**
- Collapsible sidebar
- Touch-friendly navigation
- Responsive layout
- Optimized for small screens

## Usage

### Navigation

- **Sidebar**: Click any chapter to load it
- **Search**: Type in the search box to filter chapters
- **Keyboard**: Use ← and → arrow keys to navigate between chapters
- **Navigation Buttons**: Use Previous/Next buttons at the bottom
- **TOC Button**: Click 📑 to see chapter sections
- **Mobile**: Tap the ☰ button to toggle the sidebar

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `←` | Previous chapter |
| `→` | Next chapter |
| `Esc` | Close TOC overlay |

### Features

1. **Fast Chapter Loading**: Chapters load instantly with smooth transitions
2. **Math Rendering**: All mathematical equations are beautifully rendered with MathJax
3. **Persistent State**: Your current chapter is saved in the URL (shareable links)
4. **Responsive Design**: Works perfectly on all screen sizes
5. **Dark Mode**: Toggle between light and dark themes (preference saved)
6. **Chapter TOC**: Quick navigation to any section within a chapter

## Architecture

```
nodejs-version/
├── server.js              # Express server with compression
├── package.json           # Dependencies and scripts
├── start.sh              # Quick start script
├── public/
│   ├── index.html        # Main HTML structure
│   ├── styles.css        # Modern, responsive styles
│   └── app.js            # Reactive JavaScript application
├── README.md             # This file
├── INSTALL.md            # Installation guide
├── FEATURES.md           # Feature documentation
├── DEPLOYMENT.md         # Deployment guide
└── QUICK_REFERENCE.md    # Quick reference
```

### Technology Stack

- **Backend**: Node.js + Express
- **Compression**: gzip for fast loading
- **Frontend**: Vanilla JavaScript (no framework overhead)
- **Math Rendering**: MathJax 3
- **Styling**: Modern CSS with CSS Grid and Flexbox

## API Endpoints

- `GET /api/chapters` - Returns list of all chapters
- `GET /api/chapter/:id` - Returns HTML content for a specific chapter
- `GET /*` - Serves the main application

## Performance Optimizations

1. **Compression**: All responses are gzip compressed
2. **Caching**: Static assets cached for 1 day
3. **Lazy Loading**: Chapters loaded on-demand
4. **Minimal Dependencies**: Only essential packages
5. **Efficient DOM Updates**: Minimal reflows and repaints
6. **Async Math Rendering**: MathJax loads asynchronously

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Customization

### Changing Port

Set the `PORT` environment variable:

```bash
PORT=8080 npm start
```

### Styling

Edit `public/styles.css` to customize colors, fonts, and layout. The app uses CSS variables for easy theming:

```css
:root {
    --primary-color: #003366;
    --accent-color: #0066cc;
    /* ... more variables ... */
}
```

### Adding Features

The application is built with vanilla JavaScript for easy customization. Key files:

- `public/app.js` - Application logic
- `public/styles.css` - Visual styling
- `server.js` - Backend API

## Deployment

### Quick Deploy to Vercel (Recommended) 🚀

**Option 1: Using the helper script**
```bash
./deploy-vercel.sh
```

**Option 2: Manual deployment**
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd nodejs-version
vercel

# Deploy to production
vercel --prod
```

See [VERCEL_DEPLOY.md](VERCEL_DEPLOY.md) for detailed Vercel deployment guide.

### Other Deployment Options

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions for:
- Traditional Node.js hosting
- Heroku
- Docker
- DigitalOcean
- AWS EC2

## Performance Metrics

- **Initial Load**: < 1 second
- **Chapter Switch**: < 200ms
- **Search**: Instant
- **Memory Usage**: ~50MB
- **Bundle Size**: Minimal (no heavy frameworks)

## Development

### Project Structure

- **server.js**: Express server with API endpoints
- **public/index.html**: Main application structure
- **public/styles.css**: All styling with CSS variables
- **public/app.js**: Application logic and interactivity

### Adding New Features

1. Update HTML structure in `public/index.html`
2. Add styles in `public/styles.css`
3. Implement logic in `public/app.js`
4. Test locally with `npm run dev`

## Troubleshooting

### Port Already in Use
```bash
PORT=8080 npm start
```

### Chapters Not Loading
Ensure the `../docs/chapters/` directory exists with HTML files.

### Math Not Rendering
Wait for MathJax to load (loads asynchronously).

### Search Not Working
Clear browser cache and reload.

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

Same as the main textbook project.

## Support

For issues or questions:
- Check the documentation files
- Review the code comments
- Open an issue on GitHub
- Test locally first before deploying

---

**Built with ❤️ for fast, beautiful, and accessible reading**
