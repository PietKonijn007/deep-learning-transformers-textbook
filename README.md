# Deep Learning and Transformers

A comprehensive graduate-level textbook covering the theory, mathematics, and implementation of deep learning and transformer architectures.

**📖 [Read Online (HTML)](https://pietkonijn007.github.io/deep-learning-transformers-textbook/)** | **📄 [Download PDF](main.pdf)**

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
Visit the [HTML version](https://pietkonijn007.github.io/deep-learning-transformers-textbook/) for the best reading experience with:
- Beautiful math rendering via MathJax
- Responsive design for all devices
- Easy chapter navigation
- Syntax-highlighted code examples

### Download PDF
The complete book is available as a single PDF: [main.pdf](main.pdf) (429 pages, 1.8MB)

## 🔨 Building from Source

### PDF Version

**Recommended:** Use LuaLaTeX for best results:

```bash
lualatex main.tex
lualatex main.tex  # Run twice for proper ToC and references
```

**Alternative:** Use the simplified version:

```bash
lualatex main_simple.tex
lualatex main_simple.tex
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
├── main.tex                    # Main LaTeX file (full version)
├── main_simple.tex             # Simplified LaTeX file (minimal packages)
├── main.pdf                    # Compiled PDF book
├── chapters/                   # Individual chapter LaTeX files
│   ├── preface.tex
│   ├── notation.tex
│   ├── chapter01_linear_algebra.tex
│   └── ...
├── docs/                       # HTML version (GitHub Pages)
│   ├── index.html
│   ├── chapters/
│   ├── css/
│   └── js/
├── nodejs-version/             # 🆕 Interactive Node.js web app
│   ├── server.js              # Express server
│   ├── public/                # Frontend assets
│   └── *.md                   # Comprehensive documentation
├── html-build/                 # HTML build system
│   ├── convert_to_html.py     # Python converter script
│   ├── css/
│   └── js/
├── tasks/                      # Chapter writing tasks and guides
└── references.bib              # Bibliography

```

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

- **Online Book:** https://pietkonijn007.github.io/deep-learning-transformers-textbook/
- **Repository:** https://github.com/PietKonijn007/deep-learning-transformers-textbook
- **PDF Download:** [main.pdf](main.pdf)

---

**Status:** ✅ Complete - All 23 chapters written and compiled
