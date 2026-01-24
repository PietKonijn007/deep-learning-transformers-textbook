# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Browser                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                    index.html                          │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐  │  │
│  │  │  Sidebar    │  │   Content   │  │     TOC      │  │  │
│  │  │  Navigation │  │    Area     │  │   Overlay    │  │  │
│  │  └─────────────┘  └─────────────┘  └──────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
│                           │                                  │
│                           │ styles.css (Styling)             │
│                           │ app.js (Logic)                   │
│                           │                                  │
└───────────────────────────┼──────────────────────────────────┘
                            │
                            │ HTTP/HTTPS
                            │
┌───────────────────────────┼──────────────────────────────────┐
│                    Node.js Server                            │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                   server.js                          │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ │    │
│  │  │   Express    │  │ Compression  │  │  Static   │ │    │
│  │  │   Router     │  │  Middleware  │  │  Serving  │ │    │
│  │  └──────────────┘  └──────────────┘  └───────────┘ │    │
│  └─────────────────────────────────────────────────────┘    │
│                           │                                  │
└───────────────────────────┼──────────────────────────────────┘
                            │
                            │ File System
                            │
┌───────────────────────────┼──────────────────────────────────┐
│                    File System                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              ../docs/chapters/                       │    │
│  │  ┌──────────────────────────────────────────────┐   │    │
│  │  │  chapter01_linear_algebra.html               │   │    │
│  │  │  chapter02_calculus_optimization.html        │   │    │
│  │  │  chapter03_probability_information.html      │   │    │
│  │  │  ...                                          │   │    │
│  │  └──────────────────────────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
```

## Component Breakdown

### Frontend (Browser)

#### 1. HTML Structure (index.html)
```
┌─────────────────────────────────────┐
│           Main Container            │
│  ┌───────────┐  ┌────────────────┐ │
│  │  Sidebar  │  │  Main Content  │ │
│  │           │  │                │ │
│  │  Header   │  │  TOC Button    │ │
│  │  Toolbar  │  │  Content Area  │ │
│  │  Search   │  │  TOC Overlay   │ │
│  │  Chapters │  │  Nav Controls  │ │
│  │  Footer   │  │                │ │
│  └───────────┘  └────────────────┘ │
└─────────────────────────────────────┘
```

#### 2. CSS Architecture (styles.css)
```
CSS Variables (Theming)
    ├── Light Theme Colors
    └── Dark Theme Colors

Layout
    ├── Flexbox (Main Layout)
    ├── Grid (Feature Cards)
    └── Responsive (Media Queries)

Components
    ├── Sidebar
    ├── Content Area
    ├── Navigation
    ├── TOC Overlay
    └── Loading States

Animations
    ├── Transitions
    ├── Transforms
    └── Smooth Scrolling
```

#### 3. JavaScript Architecture (app.js)
```
State Management
    ├── chapters[]
    ├── currentChapterIndex
    └── searchTerm

Core Functions
    ├── init()
    ├── loadChapters()
    ├── loadChapter()
    ├── renderChapterList()
    └── generateChapterToc()

Event Handlers
    ├── Chapter Selection
    ├── Search Input
    ├── Navigation Buttons
    ├── Keyboard Shortcuts
    ├── Theme Toggle
    └── TOC Toggle

Utilities
    ├── showLoading()
    ├── hideLoading()
    ├── updateActiveChapter()
    └── updateNavigationButtons()
```

### Backend (Node.js)

#### Server Architecture (server.js)
```
Express Application
    │
    ├── Middleware
    │   ├── compression (gzip)
    │   └── static (caching)
    │
    ├── API Routes
    │   ├── GET /api/chapters
    │   └── GET /api/chapter/:id
    │
    └── Fallback Route
        └── GET * (serve index.html)
```

## Data Flow

### 1. Initial Page Load
```
Browser Request
    ↓
Server (index.html)
    ↓
Browser Renders
    ↓
app.js Initializes
    ↓
Fetch /api/chapters
    ↓
Render Chapter List
    ↓
Ready for Interaction
```

### 2. Chapter Loading
```
User Clicks Chapter
    ↓
Show Loading Indicator
    ↓
Fetch /api/chapter/:id
    ↓
Parse HTML Content
    ↓
Update DOM
    ↓
Render Math (MathJax)
    ↓
Generate TOC
    ↓
Hide Loading Indicator
    ↓
Update URL & History
```

### 3. Search Flow
```
User Types in Search
    ↓
Filter Chapters (Client-side)
    ↓
Update Sidebar Display
    ↓
Show/Hide Matching Chapters
```

## Performance Optimizations

### 1. Server-Side
```
Request
    ↓
Compression Middleware (gzip)
    ↓
Static File Caching (1 day)
    ↓
Response (Compressed & Cached)
```

### 2. Client-Side
```
Lazy Loading
    ├── Chapters loaded on-demand
    └── MathJax loaded async

Efficient Updates
    ├── Minimal DOM manipulation
    ├── Event delegation
    └── Debounced search

Caching
    ├── Browser cache (static assets)
    ├── LocalStorage (theme preference)
    └── History API (navigation state)
```

## State Management

### Application State
```javascript
state = {
    chapters: [
        { id, title, part },
        ...
    ],
    currentChapterIndex: number,
    searchTerm: string
}
```

### Persistent State
```
LocalStorage
    └── theme: 'light' | 'dark'

URL Hash
    └── #chapter-id

Browser History
    └── { chapterId, index }
```

## API Design

### Endpoints

#### GET /api/chapters
```
Response: Array<Chapter>
[
    {
        id: string,
        title: string,
        part: string
    },
    ...
]
```

#### GET /api/chapter/:id
```
Response: HTML string
<main>
    <h1>Chapter Title</h1>
    <p>Content...</p>
    ...
</main>
```

## Security Considerations

### Server
- No user authentication (public content)
- No database (stateless)
- No file uploads
- Read-only file access
- HTTPS recommended for production

### Client
- No sensitive data storage
- XSS protection (DOM sanitization)
- CSRF not applicable (no state changes)
- Content Security Policy recommended

## Scalability

### Horizontal Scaling
```
Load Balancer
    ├── Server Instance 1
    ├── Server Instance 2
    └── Server Instance N
```

### Vertical Scaling
- Increase server resources
- Enable clustering (PM2)
- Optimize caching

### CDN Integration
```
User Request
    ↓
CDN (Static Assets)
    ├── CSS
    ├── JS
    └── Images
    ↓
Origin Server (API & HTML)
```

## Deployment Architecture

### Production Setup
```
Internet
    ↓
Reverse Proxy (nginx)
    ├── SSL Termination
    ├── Load Balancing
    └── Static Caching
    ↓
Node.js Application
    ├── Express Server
    └── PM2 Process Manager
    ↓
File System
    └── Chapter HTML Files
```

## Technology Stack

### Frontend
- **HTML5**: Semantic structure
- **CSS3**: Modern styling (Grid, Flexbox, Variables)
- **JavaScript ES6+**: Modern syntax
- **MathJax 3**: Math rendering

### Backend
- **Node.js**: Runtime environment
- **Express.js**: Web framework
- **Compression**: Gzip middleware

### Development
- **npm**: Package management
- **nodemon**: Auto-reload

## File Dependencies

```
server.js
    ├── express
    ├── compression
    └── path, fs (built-in)

index.html
    ├── styles.css
    ├── app.js
    └── MathJax (CDN)

app.js
    └── (no dependencies)

styles.css
    └── (no dependencies)
```

## Browser Compatibility

### Modern Features Used
- CSS Variables
- CSS Grid
- Flexbox
- Fetch API
- LocalStorage
- History API
- ES6+ JavaScript

### Fallbacks
- Progressive enhancement
- Graceful degradation
- Polyfills (if needed)

## Monitoring Points

### Performance Metrics
- Server response time
- Page load time
- Chapter switch time
- Memory usage
- CPU usage

### User Metrics
- Page views
- Chapter views
- Search usage
- Theme preference
- Navigation patterns

## Future Architecture Considerations

### Potential Enhancements
- Service Worker (PWA)
- IndexedDB (Offline storage)
- WebSockets (Real-time updates)
- GraphQL API (Flexible queries)
- Server-Side Rendering (SSR)
- Static Site Generation (SSG)

### Scalability Improvements
- Redis caching
- CDN integration
- Database for analytics
- Microservices architecture
- Containerization (Docker/Kubernetes)
