# CLAUDE.md

## Project Overview

This repository contains a **graduate-level academic textbook** on deep learning and transformer architectures, published in two editions:

1. **Deep Tech Edition** ("Deep Learning and Transformers") - 34 chapters across 10 parts (429 pages)
2. **Leadership Edition** ("Deep Learning and LLMs for Technical Leaders") - 17 chapters across 5 parts

The content is authored in **LaTeX**, compiled to **PDF**, converted to **HTML**, and deployed as a static web application on **Vercel** at https://deeplearning.hofkensvermeulen.be/.

## Repository Structure

```
/
├── main_pro.tex              # Master LaTeX file (deep tech book)
├── main_pro.pdf              # Compiled PDF (429 pages)
├── references.bib            # Bibliography
├── chapters/                 # LaTeX source (.tex) + deployed HTML
│   ├── *.tex                 # 36 LaTeX source files
│   ├── deeptech/             # Generated deep tech HTML (36 files)
│   ├── leadership/           # Generated leadership HTML (21 files)
│   └── diagrams/             # Shared diagram assets (PNG + SVG)
│
├── leadership-book/          # Leadership edition LaTeX source
│   ├── main.tex
│   ├── main.pdf
│   ├── chapters/             # 21 chapter source files
│   └── compile.sh            # Build script
│
├── nodejs-version/           # Web app source (development source of truth)
│   ├── server.js             # Express.js server (local dev only)
│   ├── package.json          # Node.js dependencies
│   └── public/               # Frontend assets
│       ├── index.html        # Landing page
│       ├── deeptech.html     # Deep tech reader interface
│       ├── leadership.html   # Leadership reader interface
│       ├── deeptech-app.js   # Deep tech app logic
│       ├── leadership-app.js # Leadership app logic
│       ├── styles.css        # Shared stylesheet
│       └── chapters/         # HTML chapters (source copies)
│
├── html-build/               # LaTeX-to-HTML conversion tools
│   ├── convert_to_html.py    # Deep tech converter (Python)
│   └── convert_leadership_final.py  # Leadership converter (Python)
│
├── index.html                # Deployed: book selector (synced from nodejs-version)
├── deeptech.html             # Deployed: deep tech interface
├── leadership.html           # Deployed: leadership interface
├── deeptech-app.js           # Deployed: deep tech app logic
├── leadership-app.js         # Deployed: leadership app logic
├── styles.css                # Deployed: shared styles
├── vercel.json               # Vercel deployment config
├── sync-to-root.sh           # Syncs nodejs-version/public/ -> root
└── docs/                     # GitHub Pages (alternative deployment)
```

### Key Architectural Principle

Vercel deploys from the **root directory**, not from `nodejs-version/`. The `nodejs-version/public/` directory is the source of truth for web assets. The `sync-to-root.sh` script copies those assets to the root for deployment. The root-level HTML/JS/CSS files are **generated outputs** -- edit the versions in `nodejs-version/public/` instead.

## Development Workflows

### Local Development (Web App)

```bash
cd nodejs-version
npm install
npm run dev        # Start with nodemon (auto-reload)
# OR
npm start          # Start without auto-reload
```

Opens at http://localhost:3000. Requires Node.js >= 14.

### Compiling the PDF

```bash
lualatex main_pro.tex
lualatex main_pro.tex   # Run twice for TOC and cross-references
```

Requires TeX Live 2025, MiKTeX, or MacTeX with LuaLaTeX.

### Converting LaTeX to HTML

```bash
# Deep tech book
python3 html-build/convert_to_html.py

# Leadership book
python3 html-build/convert_leadership_final.py
```

Uses only Python standard library. Requires `pdflatex` and `pdf2svg` (or ImageMagick) for TikZ diagram conversion.

### Deploying Changes

```bash
# 1. Edit LaTeX sources in chapters/*.tex or leadership-book/chapters/*.tex
# 2. Run the appropriate HTML conversion script
# 3. Sync web assets to root for Vercel
./sync-to-root.sh
# 4. Commit and push to main -- Vercel auto-deploys
```

## Dependencies

### Node.js (nodejs-version/)

- **express** ^4.18.2 - Web framework (local dev server)
- **compression** ^1.7.4 - Gzip middleware
- **nodemon** ^3.0.2 (dev) - Auto-reload

### Python

No external packages. Standard library only.

### System Dependencies (for build)

- **LaTeX:** TeX Live / MacTeX with LuaLaTeX or PDFLaTeX
- **TikZ diagrams:** `pdf2svg` or ImageMagick `convert`

### Frontend (CDN)

- **MathJax 3** - Math rendering (loaded from CDN, no local install)
- No other frontend frameworks -- vanilla JavaScript and CSS

## Code Conventions

### LaTeX

- Chapters use standard LaTeX environments: `theorem`, `definition`, `example`, `exercise`, `proof`, `lemma`, `proposition`, `corollary`, `remark`
- Math typeset with `amsmath`, `amssymb`, `mathtools`, `bm`
- Diagrams created with TikZ/PGFPlots
- Code listings use the `listings` package
- Algorithms use `algorithm2e`

### JavaScript

- Vanilla ES6+ (no framework, no transpiler, no bundler)
- State managed via a simple object literal (`const state = { ... }`)
- Chapters loaded dynamically via `fetch()` and injected into the DOM
- MathJax re-rendered after each chapter load
- Dark/light theme persisted via `localStorage`
- Keyboard navigation with arrow keys

### CSS

- CSS custom properties for theming (e.g. `--primary-color`, `--bg-color`)
- Dark mode via `[data-theme="dark"]` selector
- Responsive design with media queries for mobile/tablet/desktop
- Styled boxes for `.theorem`, `.definition`, `.example`, `.code-block`

### HTML Chapter Format

Generated HTML chapters follow this pattern:

```html
<h1>Chapter Title</h1>
<section id="section-name">
  <h2>Section Name</h2>
  <div class="definition"><strong>Definition:</strong> ...</div>
  <div class="theorem"><strong>Theorem:</strong> <em>Statement</em></div>
  <pre><code>code here</code></pre>
  <figure>
    <img src="/chapters/diagrams/diagram.svg" />
    <figcaption>Caption</figcaption>
  </figure>
</section>
```

## API Endpoints (Express Server, Local Dev Only)

| Endpoint | Description |
|---|---|
| `GET /api/books` | List available books |
| `GET /api/chapters/:bookId` | Chapter list for a book (`deeptech` or `leadership`) |
| `GET /api/chapter/:bookId/:chapterId` | Chapter HTML content |
| `GET /api/debug/files` | Debug filesystem paths |

In production (Vercel), chapters are served as static files -- the Express server is not used.

## Testing

There is no formal test suite. Validation is done through:

- Local browser testing (`npm run dev`)
- Vercel deployment previews on pull requests
- Manual verification of MathJax rendering and navigation
- Individual chapter LaTeX compilation via `compile_chapters.sh`

## Linting and Formatting

No linting or formatting tools are configured. There is no ESLint, Prettier, or Python linter setup.

## Important Notes for AI Assistants

1. **Edit web assets in `nodejs-version/public/`**, not in the root. Root copies are generated by `sync-to-root.sh`.
2. **LaTeX source files** live in `chapters/*.tex` (deep tech) and `leadership-book/chapters/*.tex` (leadership).
3. **HTML chapter files are generated** by the Python conversion scripts -- do not hand-edit them unless making a targeted fix.
4. **No build step** for the web app itself. It is a static site with vanilla JS.
5. **Math content** uses LaTeX notation rendered by MathJax. Inline math uses `$...$`, display math uses `$$...$$`.
6. **PDFs are checked into the repo** (`.gitignore` has `*.pdf` commented out). Be mindful of large binary commits.
7. The `docs/` directory is a separate GitHub Pages deployment target and may be out of date relative to the root deployment.
