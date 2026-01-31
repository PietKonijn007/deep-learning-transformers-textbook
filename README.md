# Deep Learning and Transformers

A comprehensive graduate-level textbook covering the theory, mathematics, and implementation of deep learning and transformer architectures.

**📖 [Read Online (HTML)](https://deeplearning.hofkensvermeulen.be/)** | **📄 [Download PDF](main_pro.pdf)**

## 📚 Book Structure

### Part I: Mathematical Foundations
- **Chapter 1:** Linear Algebra for Deep Learning
- **Chapter 2:** Calculus and Optimization
- **Chapter 3:** Probability and Information Theory

### Part II: Neural Network Fundamentals
- **Chapter 4:** Feed-Forward Neural Networks
- **Chapter 5:** Convolutional Neural Networks
- **Chapter 6:** Recurrent Neural Networks

### Part III: Attention Mechanisms
- **Chapter 7:** Attention Fundamentals
- **Chapter 8:** Self-Attention
- **Chapter 9:** Attention Variants

### Part IV: Transformer Architecture
- **Chapter 10:** Transformer Model
- **Chapter 11:** Training Transformers
- **Chapter 12:** Computational Analysis

### Part V: Modern Transformer Variants
- **Chapter 13:** BERT
- **Chapter 14:** GPT
- **Chapter 15:** T5 and BART
- **Chapter 16:** Efficient Transformers

### Part VI: Advanced Topics
- **Chapter 17:** Vision Transformers
- **Chapter 18:** Multimodal Transformers
- **Chapter 19:** Long Context
- **Chapter 20:** Pretraining Strategies

### Part VII: Practical Implementation
- **Chapter 21:** PyTorch Implementation
- **Chapter 22:** Hardware Optimization
- **Chapter 23:** Best Practices

### Part VIII: Domain Applications
- **Chapter 24:** Domain-Specific Models
- **Chapter 25:** Enterprise NLP
- **Chapter 26:** Code and Language Models
- **Chapter 27:** Video and Visual Understanding
- **Chapter 28:** Knowledge Graphs and Reasoning
- **Chapter 29:** Recommendation Systems

### Part IX: Industry Applications
- **Chapter 30:** Healthcare Applications
- **Chapter 31:** Financial Applications
- **Chapter 32:** Legal and Compliance Applications

### Part X: Production Systems
- **Chapter 33:** Observability and Monitoring
- **Chapter 34:** DSL and Agent Systems

## 🚀 Quick Start

### 🆕 Interactive Node.js Version (Recommended)
Experience the textbook in a modern, fast, and beautiful web application:

```bash
cd nodejs-version
npm install
npm start
```

Open http://localhost:3000 for:
- ⚡ Lightning-fast loading (< 1 second)
- 🎨 Beautiful UI with dark mode
- 📱 Perfect mobile experience
- 🔍 Instant chapter search
- ⌨️ Keyboard navigation
- 📑 Chapter table of contents

**Deploy to Vercel in 5 minutes:**
```bash
cd nodejs-version
./deploy-vercel.sh
```

**[See nodejs-version/README.md for details](nodejs-version/README.md)** | **[Deploy Guide](nodejs-version/DEPLOY_NOW.md)**

### Read Online
Visit the [HTML version](https://deeplearning.hofkensvermeulen.be/) for the best reading experience with:
- Beautiful math rendering via MathJax
- Responsive design for all devices
- Easy chapter navigation
- Syntax-highlighted code examples

### Download PDF
The complete book is available as a single PDF: [main_pro.pdf](main_pro.pdf) (429 pages, 1.8MB)

## 🔨 Building from Source

### PDF Version

**Recommended:** Use LuaLaTeX for best results:

```bash
lualatex main_pro.tex
lualatex main_pro.tex  # Run twice for proper ToC and references
```

**Alternative:** Use the test version:

```bash
lualatex main_pro_test.tex
lualatex main_pro_test.tex
```

### HTML Version

Generate the HTML version:

```bash
cd html-build
python3 convert_to_html.py
open output/index.html
```

The HTML files will be created in `html-build/output/` and automatically copied to `docs/` for GitHub Pages.

## 📋 Requirements

### For PDF Compilation
- **LaTeX Distribution:** TeX Live 2025, MiKTeX, or MacTeX
- **Compiler:** LuaLaTeX (recommended) or PDFLaTeX
- **Required Packages:** 
  - Math: `amsmath`, `amssymb`, `amsthm`, `mathtools`, `bm`
  - Graphics: `graphicx`, `tikz`, `pgfplots`
  - Tables: `booktabs`, `multirow`, `array`
  - Code: `listings`, `algorithm2e`
  - Other: `hyperref`, `cleveref`, `biblatex`, `framed`

### For HTML Generation
- **Python 3.x**
- No additional packages required (uses standard library)

## 📁 Repository Structure

```
.
├── app.js                      # 🚀 DEPLOYED: Main application (synced from nodejs-version)
├── index.html                  # 🚀 DEPLOYED: Main page (synced from nodejs-version)
├── styles.css                  # 🚀 DEPLOYED: Styles (synced from nodejs-version)
├── chapters/                   # 🚀 DEPLOYED: Chapter HTML files
│   ├── preface.html
│   ├── notation.html
│   ├── chapter01_*.html
│   └── ... (34 chapters)
│
├── main_pro.tex                # LaTeX source (production version)
├── main_pro.pdf                # Compiled PDF book (429 pages)
│
├── chapters/                   # LaTeX source files
│   ├── *.tex                   # Chapter source files
│   └── *.html                  # Generated HTML (copied to root)
│
├── nodejs-version/             # 🔧 DEVELOPMENT: Source of truth for web app
│   ├── public/                 # Frontend source files
│   │   ├── app.js             # Application logic (SOURCE)
│   │   ├── index.html         # Main page (SOURCE)
│   │   ├── styles.css         # Styles (SOURCE)
│   │   └── chapters/          # Chapter HTML files
│   ├── server.js              # Local development server
│   └── *.md                   # Documentation
│
├── html-build/                 # HTML generation tools
│   └── convert_to_html.py     # TEX → HTML converter
│
├── sync-to-root.sh             # 🔄 Sync script (nodejs-version → root)
├── DEPLOYMENT_ARCHITECTURE.md  # 📖 Deployment documentation
└── vercel.json                 # Vercel configuration
```

### 🚀 Deployment Architecture

**Important:** Vercel deploys from the **ROOT directory**, not from `nodejs-version/`.

- **Source files:** `nodejs-version/public/` (development)
- **Deployed files:** Root directory (production)
- **Sync command:** `./sync-to-root.sh`

See [DEPLOYMENT_ARCHITECTURE.md](DEPLOYMENT_ARCHITECTURE.md) for complete details.

## 🎓 Target Audience

This textbook is designed for:
- Graduate students in computer science, electrical engineering, and mathematics
- Researchers working with deep learning and transformers
- Industry practitioners building production ML systems
- Anyone seeking rigorous understanding of modern deep learning

### Prerequisites
- Strong foundations in linear algebra
- Solid understanding of multivariable calculus
- Basic probability theory and statistics
- Programming experience (preferably Python)
- Familiarity with machine learning concepts

## 🌟 Features

- **Mathematical Rigor:** Complete derivations with geometric intuition
- **Practical Focus:** Theory grounded in implementation details
- **Progressive Complexity:** Systematic knowledge building
- **Real Examples:** Realistic dimensions from actual models (BERT, GPT, ViT)
- **Complete Coverage:** From foundations to state-of-the-art architectures
- **Production Ready:** Hardware optimization and deployment strategies

## 📝 License

Copyright © 2026. All rights reserved.

## 🤝 Contributing

This is an academic textbook project. For questions, suggestions, or corrections:
- Open an issue on GitHub
- Submit a pull request for typos or corrections
- Contact the authors for major contributions

## 🔗 Links

- **Online Book:** https://deeplearning.hofkensvermeulen.be/
- **Repository:** https://github.com/PietKonijn007/deep-learning-transformers-textbook
- **PDF Download:** [main_pro.pdf](main_pro.pdf)

---

**Status:** ✅ Complete - All 34 chapters written and compiled (January 2026)
